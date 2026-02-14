from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Insurance Platform"
    CHROMA_PERSIST_DIR: str = "./chroma"
    DEFAULT_COLLECTION: str = "policies"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"


settings = Settings()
