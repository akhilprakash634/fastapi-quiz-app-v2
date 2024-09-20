from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Quiz App"
    MONGO_URL: str
    MONGO_DB_NAME: str

    class Config:
        env_file = ".env"

settings = Settings()