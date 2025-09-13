from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import get_settings

settings = get_settings()


class MongoDB:
    client: AsyncIOMotorClient = None
    database = None


mongodb = MongoDB()


async def connect_to_mongo():
    """Create database connection"""
    mongodb.client = AsyncIOMotorClient(settings.mongodb_url)
    mongodb.database = mongodb.client[settings.mongodb_database]


async def close_mongo_connection():
    """Close database connection"""
    if mongodb.client:
        mongodb.client.close()


def get_mongo_database():
    return mongodb.database