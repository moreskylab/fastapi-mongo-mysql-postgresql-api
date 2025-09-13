import asyncpg
from contextlib import asynccontextmanager
from app.core.config import get_settings

settings = get_settings()


class PostgreSQL:
    pool = None


postgresql = PostgreSQL()


async def connect_to_postgresql():
    """Create PostgreSQL connection pool"""
    postgresql.pool = await asyncpg.create_pool(
        host=settings.postgresql_host,
        port=settings.postgresql_port,
        user=settings.postgresql_user,
        password=settings.postgresql_password,
        database=settings.postgresql_database,
        min_size=1,
        max_size=10
    )


async def close_postgresql_connection():
    """Close PostgreSQL connection pool"""
    if postgresql.pool:
        await postgresql.pool.close()


@asynccontextmanager
async def get_postgresql_connection():
    """Get PostgreSQL connection from pool"""
    if not postgresql.pool:
        raise Exception("PostgreSQL connection pool is not initialized")
    
    async with postgresql.pool.acquire() as connection:
        yield connection


async def create_postgresql_tables():
    """Create PostgreSQL tables if they don't exist"""
    async with get_postgresql_connection() as connection:
        # Users table
        await connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                age INTEGER CHECK (age >= 0 AND age <= 150),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Products table
        await connection.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(200) NOT NULL,
                description TEXT,
                price DECIMAL(10, 2) NOT NULL CHECK (price > 0),
                category VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Orders table
        await connection.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id VARCHAR(36) PRIMARY KEY,
                user_id VARCHAR(36) NOT NULL,
                product_id VARCHAR(36) NOT NULL,
                quantity INTEGER NOT NULL CHECK (quantity > 0),
                total_amount DECIMAL(10, 2) NOT NULL CHECK (total_amount > 0),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
            )
        """)
        
        # Create updated_at trigger function
        await connection.execute("""
            CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated_at = CURRENT_TIMESTAMP;
                RETURN NEW;
            END;
            $$ language 'plpgsql';
        """)
        
        # Create triggers for updated_at
        for table in ['users', 'products', 'orders']:
            await connection.execute(f"""
                DROP TRIGGER IF EXISTS update_{table}_updated_at ON {table};
                CREATE TRIGGER update_{table}_updated_at 
                BEFORE UPDATE ON {table} 
                FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
            """)