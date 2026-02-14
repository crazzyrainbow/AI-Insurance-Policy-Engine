import torch
from sentence_transformers import SentenceTransformer
from app.core.config import settings


device = "mps" if torch.backends.mps.is_available() else "cpu"

model = SentenceTransformer(
    settings.EMBEDDING_MODEL,
    device=device
)


def generate_embedding(text: str):
    return model.encode(text).tolist()
