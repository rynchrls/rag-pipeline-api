from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    HOST: str = os.getenv("HOST")
    PORT: int = os.getenv("PORT")
    DEBUG: bool = os.getenv("DEBUG")
    DATABASE_URL: str = os.getenv("DATABASE_URI")
    SC: str = os.getenv("SECRET_KEY")  # type: ignore
    ALGORITHM: str = os.getenv("ALGORITHM")  # type: ignore
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30000)
    )

    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST")
    OLLAMA_API_KEY: str = os.getenv("OLLAMA_API_KEY")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL")

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL")

    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL")


settings = Settings()
