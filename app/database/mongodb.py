from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class MongoDB:
    client: AsyncIOMotorClient = None
    database = None


mongodb = MongoDB()


async def connect_to_mongo():
    """Create database connection"""
    try:
        mongodb.client = AsyncIOMotorClient(settings.database_url_mongodb)
        mongodb.database = mongodb.client.get_default_database()
        
        # Test connection
        await mongodb.client.admin.command('ping')
        logger.info("Connected to MongoDB successfully")
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")
        # For demo purposes, we'll continue without failing
        pass


async def close_mongo_connection():
    """Close database connection"""
    if mongodb.client:
        mongodb.client.close()
        logger.info("Disconnected from MongoDB")


async def get_database():
    """Get database instance"""
    return mongodb.database