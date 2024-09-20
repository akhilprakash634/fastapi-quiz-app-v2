from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    APP_NAME: str = "Quiz App"
    MONGO_URL: str
    MONGO_DB_NAME: str

    class Config:
        env_file = ".env"

settings = Settings()

