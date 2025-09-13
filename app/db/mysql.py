import aiomysql
from contextlib import asynccontextmanager
from app.core.config import get_settings

settings = get_settings()


class MySQL:
    pool = None


mysql = MySQL()


async def connect_to_mysql():
    """Create MySQL connection pool"""
    mysql.pool = await aiomysql.create_pool(
        host=settings.mysql_host,
        port=settings.mysql_port,
        user=settings.mysql_user,
        password=settings.mysql_password,
        db=settings.mysql_database,
        minsize=1,
        maxsize=10,
        autocommit=True
    )


async def close_mysql_connection():
    """Close MySQL connection pool"""
    if mysql.pool:
        mysql.pool.close()
        await mysql.pool.wait_closed()


@asynccontextmanager
async def get_mysql_connection():
    """Get MySQL connection from pool"""
    if not mysql.pool:
        raise Exception("MySQL connection pool is not initialized")
    
    async with mysql.pool.acquire() as connection:
        async with connection.cursor() as cursor:
            yield cursor


async def create_mysql_tables():
    """Create MySQL tables if they don't exist"""
    async with get_mysql_connection() as cursor:
        # Users table
        await cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                age INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        
        # Products table
        await cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(200) NOT NULL,
                description TEXT,
                price DECIMAL(10, 2) NOT NULL,
                category VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        
        # Orders table
        await cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id VARCHAR(36) PRIMARY KEY,
                user_id VARCHAR(36) NOT NULL,
                product_id VARCHAR(36) NOT NULL,
                quantity INT NOT NULL,
                total_amount DECIMAL(10, 2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
            )
        """)