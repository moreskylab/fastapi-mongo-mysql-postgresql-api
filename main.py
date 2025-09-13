from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.core.config import get_settings
from app.db.mongodb import connect_to_mongo, close_mongo_connection
from app.db.mysql import connect_to_mysql, close_mysql_connection, create_mysql_tables
from app.db.postgresql import connect_to_postgresql, close_postgresql_connection, create_postgresql_tables
from app.api import mongodb_routes, mysql_routes, postgresql_routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown event handler"""
    try:
        # Startup
        logger.info("Starting up FastAPI application...")
        
        # Connect to databases
        logger.info("Connecting to MongoDB...")
        await connect_to_mongo()
        
        logger.info("Connecting to MySQL...")
        await connect_to_mysql()
        await create_mysql_tables()
        
        logger.info("Connecting to PostgreSQL...")
        await connect_to_postgresql()
        await create_postgresql_tables()
        
        logger.info("All databases connected successfully!")
        
        yield
        
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise
    finally:
        # Shutdown
        logger.info("Shutting down FastAPI application...")
        
        logger.info("Closing MongoDB connection...")
        await close_mongo_connection()
        
        logger.info("Closing MySQL connection...")
        await close_mysql_connection()
        
        logger.info("Closing PostgreSQL connection...")
        await close_postgresql_connection()
        
        logger.info("All database connections closed!")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A comprehensive FastAPI template supporting MongoDB, MySQL, and PostgreSQL databases",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to FastAPI Multi-Database API",
        "version": settings.app_version,
        "databases": ["MongoDB", "MySQL", "PostgreSQL"],
        "endpoints": {
            "MongoDB Users": "/mongodb/users",
            "MySQL Products": "/mysql/products", 
            "PostgreSQL Orders": "/postgresql/orders"
        },
        "health_checks": {
            "MongoDB": "/mongodb/health",
            "MySQL": "/mysql/health",
            "PostgreSQL": "/postgresql/health"
        },
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health():
    """Overall health check endpoint"""
    return {
        "status": "healthy",
        "application": settings.app_name,
        "version": settings.app_version
    }


# Include routers
app.include_router(mongodb_routes.router)
app.include_router(mysql_routes.router)
app.include_router(postgresql_routes.router)


# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Global exception: {exc}")
    return HTTPException(
        status_code=500,
        detail="Internal server error"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )