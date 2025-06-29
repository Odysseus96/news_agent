import os, hashlib, json
from datetime import datetime
from llama_index.core import Document, VectorStoreIndex, StorageContext, load_index_from_storage
from embedding_factory import get_embedding_model

from .markdown_report import save_news_as_markdown
from .visualizer import generate_source_bar_chart
from fetcher.classifier import is_ai_related

INDEXED_LOG = "./data/indexed_news.jsonl"
VECTOR_STORE_DIR = "./vector_index"
EXCLUDE_KEYWORDS = ["抽奖", "推广", "招聘", "广告"]

def compute_hash(news: dict) -> str:
    base = news["title"] + news["link"]
    return hashlib.md5(base.encode("utf-8")).hexdigest()

def ensure_index_log_file():
    """确保索引日志文件存在"""
    os.makedirs(os.path.dirname(INDEXED_LOG), exist_ok=True)
    if not os.path.exists(INDEXED_LOG):
        with open(INDEXED_LOG, "w", encoding="utf-8") as f:
            pass  # 写入空文件

def load_indexed_hashes() -> set:
    if not os.path.exists(INDEXED_LOG):
        return set()
    with open(INDEXED_LOG, "r", encoding="utf-8") as f:
        return {json.loads(line)["hash"] for line in f}

def append_indexed(news: dict):
    hash_val = compute_hash(news)
    ensure_index_log_file()
    with open(INDEXED_LOG, "a", encoding="utf-8") as f:
        json.dump({"hash": hash_val, "link": news["link"], "title": news["title"]}, f)
        f.write("\n")

def is_valid_news(news: dict) -> bool:
    if len(news["content"]) < 300:
        return False
    if any(word in news["title"] for word in EXCLUDE_KEYWORDS):
        return False
    if not is_ai_related(news):
        return False
    return True

def save_as_documents(news_list: list[dict]) -> list[Document]:
    return [
        Document(
            text=f"【标题】{news['title']}\n\n{news['content']}",
            metadata={
                "source": news["source"],
                "link": news["link"],
                "published": news["published"]
            }
        )
        for news in news_list
    ]

def build_or_update_index(documents: list[Document]):
    os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
    embed_model = get_embedding_model()

    if os.path.exists(os.path.join(VECTOR_STORE_DIR, "docstore.json")):
        print("🧠 加载已有索引，增量更新")
        storage_context = StorageContext.from_defaults(persist_dir=VECTOR_STORE_DIR)
        index = load_index_from_storage(storage_context, embed_model=embed_model)

        index.storage_context.doc_store.add_documents(documents)
        index.storage_context.persist(persist_dir=VECTOR_STORE_DIR)
    else:
        print("📘 初次构建索引")
        index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
        index.storage_context.persist(persist_dir=VECTOR_STORE_DIR)


def ingest_news(news_list: list[dict]):
    indexed_hashes = load_indexed_hashes()
    filtered_news = []

    for news in news_list:
        if not is_valid_news(news):
            continue
        h = compute_hash(news)
        if h in indexed_hashes:
            continue
        append_indexed(news)
        filtered_news.append(news)

    if not filtered_news:
        print("⚠️ 无新增有效新闻，跳过索引和报告")
        return

    save_news_as_markdown(filtered_news)
    generate_source_bar_chart(filtered_news)
    documents = save_as_documents(filtered_news)
    build_or_update_index(documents)
    print(f"✅ 本轮新增 {len(filtered_news)} 篇新闻，已完成存储与索引")
