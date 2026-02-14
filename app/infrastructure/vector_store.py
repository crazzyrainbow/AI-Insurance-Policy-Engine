import chromadb
from chromadb.config import Settings as ChromaSettings
from app.core.config import settings

client = chromadb.Client(
    ChromaSettings(
        persist_directory=settings.CHROMA_PERSIST_DIR,
        anonymized_telemetry=False
    )
)

collection = client.get_or_create_collection(
    name=settings.DEFAULT_COLLECTION
)
