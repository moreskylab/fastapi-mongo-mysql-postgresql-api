from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Convert postgresql:// to postgresql+asyncpg://
postgresql_url = settings.database_url_postgresql.replace("postgresql://", "postgresql+asyncpg://")

# Create async engine
engine = create_async_engine(
    postgresql_url,
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


async def get_postgresql_session():
    """Get PostgreSQL database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


async def init_postgresql_db():
    """Initialize PostgreSQL database"""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("PostgreSQL database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing PostgreSQL database: {e}")
        # For demo purposes, we'll continue without failing
        pass