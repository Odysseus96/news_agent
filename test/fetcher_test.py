# fetcher/ingest_demo.py
from llama_index.core import Document, VectorStoreIndex, StorageContext, load_index_from_storage
import os
from datetime import datetime

import sys
from pathlib import Path
backend_path = Path(__file__).parent.parent / "backend"
print(backend_path)
sys.path.insert(0, str(backend_path))

from fetcher.parser import parse_news_from_rss
from fetcher.fetch_news import fetch_all_news
from embedding_factory import get_embedding_model

# === 可自定义多个 RSS 源 ===
rss_sources = [
    {"url": "https://www.sciencedaily.com/rss/top/technology.xml", "source": "ScienceDaily"},
    {"url": "https://36kr.com/feed", "source": "36Kr"},
]

VECTOR_INDEX_PATH = "./vector_index"

def save_as_documents(news_list) -> list[Document]:
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
    os.makedirs(VECTOR_INDEX_PATH, exist_ok=True)
    embed_model = get_embedding_model()

    if os.path.exists(os.path.join(VECTOR_INDEX_PATH, "docstore.json")):
        # 加载已有 index
        storage_context = StorageContext.from_defaults(persist_dir=VECTOR_INDEX_PATH)
        index = load_index_from_storage(storage_context)
        index.insert_documents(documents)  # type: ignore # 增量插入
    else:
        # 首次构建
        index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
        index.storage_context.persist(persist_dir=VECTOR_INDEX_PATH)

    print("✅ 向量索引已更新，共插入文档：", len(documents))

if __name__ == "__main__":
    fetch_all_news()
