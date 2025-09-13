from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "FastAPI Multi-Database API"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Database URLs
    database_url_mongodb: str = "mongodb://localhost:27017/fastapi_app"
    database_url_mysql: str = "mysql://user:password@localhost:3306/fastapi_app"
    database_url_postgresql: str = "postgresql://user:password@localhost:5432/fastapi_app"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()