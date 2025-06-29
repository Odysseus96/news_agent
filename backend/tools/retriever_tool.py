from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from langchain.tools import tool
from typing import List

@tool("news_retriever")
def retrieve_news(state) -> dict:
    """ 从本地向量索引检索新闻数据 """
    query = state["user_query"]
    # 读取本地文档（或改为 SimpleWebPageReader）
    documents = SimpleDirectoryReader("data/").load_data()
    index = VectorStoreIndex.from_documents(documents)

    retriever = index.as_retriever(similarity_top_k=3)
    results = retriever.retrieve(query)

    return {
        "user_query": query,
        "news_data": [r.text for r in results]
    }
