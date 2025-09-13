from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import StaticPool
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Convert mysql:// to mysql+aiomysql://
mysql_url = settings.database_url_mysql.replace("mysql://", "mysql+aiomysql://")

# Create async engine
engine = create_async_engine(
    mysql_url,
    poolclass=StaticPool,
    connect_args={
        "check_same_thread": False,  # Only needed for SQLite
    } if "sqlite" in mysql_url else {},
    echo=True if settings.debug else False,
)

# Create session factory
AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
)

# Create declarative base
Base = declarative_base()


async def get_mysql_session():
    """Get MySQL database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


async def init_mysql_db():
    """Initialize MySQL database"""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("MySQL database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing MySQL database: {e}")
        # For demo purposes, we'll continue without failing
        pass