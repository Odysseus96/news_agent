from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.llms.ollama import Ollama
from pymilvus import connections

import os

connections.connect("milvus", host="localhost", port=19530)

milvus_vector_store = MilvusVectorStore(
    collection_name="test_collection",
    dim=1024,
    embedding_field="embedding",
    index_params={"index_type": "IVF_FLAT", "metric_type": "L2"},
    search_params={"metric_type": "L2"},
    connection_args={"uri": "http://localhost:19530"},
    overwrite=True
)

storage_context = StorageContext.from_defaults(
    vector_store=milvus_vector_store)

embed_model = HuggingFaceEmbedding(model_name='BAAI/bge-m3')

# ✅ 加载文档（可换成你自己的文本）
documents = SimpleDirectoryReader(input_files=["test/example.txt"]).load_data()

index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
    embed_model=embed_model
)

# 加载 Ollama LLM
llm = Ollama(
    model="qwen3:8b",
    base_url="http://localhost:11434",
    api_key='ollama-placeholder-key'
)

# 构建 Query Engine，指定 LLM
query_engine = index.as_query_engine(llm=llm)

response = query_engine.query("What is Milvus used for?")
print(response)
