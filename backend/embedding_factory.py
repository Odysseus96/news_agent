from config import (
    EMBEDDING_PROVIDER,
    LOCAL_EMBEDDING_MODEL,
    OPENAI_API_KEY,
    OPENAI_API_BASE,
    OLLAMA_API_BASE,
    OLLAMA_API_KEY,
)

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.ollama import OllamaEmbedding
import os


def get_embedding_model():
    if EMBEDDING_PROVIDER == "local":
        print(f"[embedding_factory] 使用本地 HuggingFace 模型: {LOCAL_EMBEDDING_MODEL}")
        return HuggingFaceEmbedding(model_name=LOCAL_EMBEDDING_MODEL)

    elif EMBEDDING_PROVIDER == "openai":
        print("[embedding_factory] 使用 OpenAI API 模型")
        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
        if OPENAI_API_BASE:
            os.environ["OPENAI_API_BASE"] = OPENAI_API_BASE
        return OpenAIEmbedding()

    elif EMBEDDING_PROVIDER == "ollama":
        print("[embedding_factory] 使用 Ollama 本地模型（OpenAI 接口兼容）")
        os.environ["OPENAI_API_KEY"] = OLLAMA_API_KEY
        os.environ["OPENAI_API_BASE"] = OLLAMA_API_BASE
        return OllamaEmbedding(
            model_name= LOCAL_EMBEDDING_MODEL,
            base_url = OLLAMA_API_BASE
        )

    else:
        raise ValueError(f"不支持的嵌入模型提供者: {EMBEDDING_PROVIDER}")
