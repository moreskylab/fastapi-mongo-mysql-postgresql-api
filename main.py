from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.config import settings
from app.database.mongodb import connect_to_mongo, close_mongo_connection
from app.database.mysql import init_mysql_db
from app.database.postgresql import init_postgresql_db
from app.routers import mongodb_routes, mysql_routes, postgresql_routes
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events"""
    # Startup
    logger.info("Starting up FastAPI Multi-Database API")
    
    # Initialize databases
    await connect_to_mongo()
    await init_mysql_db()
    await init_postgresql_db()
    
    logger.info("Database connections established")
    
    yield
    
    # Shutdown
    logger.info("Shutting down FastAPI Multi-Database API")
    await close_mongo_connection()
    logger.info("Database connections closed")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A FastAPI application demonstrating integration with MongoDB, MySQL, and PostgreSQL databases",
    lifespan=lifespan,
)

# Include routers
app.include_router(mongodb_routes.router, prefix="/api/v1")
app.include_router(mysql_routes.router, prefix="/api/v1")
app.include_router(postgresql_routes.router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to FastAPI Multi-Database API",
        "version": settings.app_version,
        "databases": ["MongoDB", "MySQL", "PostgreSQL"],
        "endpoints": {
            "MongoDB": "/api/v1/mongodb/users/",
            "MySQL": "/api/v1/mysql/users/",
            "PostgreSQL": "/api/v1/postgresql/users/"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info"
    )