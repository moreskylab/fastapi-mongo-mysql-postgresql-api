from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # API Settings
    app_name: str = "FastAPI Multi-Database API"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # MongoDB Settings
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_database: str = "fastapi_db"
    
    # MySQL Settings
    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_user: str = "root"
    mysql_password: str = "password"
    mysql_database: str = "fastapi_db"
    
    # PostgreSQL Settings
    postgresql_host: str = "localhost"
    postgresql_port: int = 5432
    postgresql_user: str = "postgres"
    postgresql_password: str = "password"
    postgresql_database: str = "fastapi_db"
    
    # Security
    secret_key: str = "your-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()