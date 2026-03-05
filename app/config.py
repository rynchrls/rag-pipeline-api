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
    MODEL: str = os.getenv("model")


settings = Settings()
