import sys
from pathlib import Path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from embedding_factory import get_embedding_model

embed_model = get_embedding_model()

embeddings = embed_model.get_text_embedding("Hello World!")

print(len(embeddings))
print(embeddings[:5])
