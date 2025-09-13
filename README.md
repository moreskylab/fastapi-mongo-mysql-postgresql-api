# FastAPI Multi-Database API

A FastAPI application that demonstrates integration with three different database backends:
- **MongoDB** (NoSQL document database)
- **MySQL** (Relational database)
- **PostgreSQL** (Relational database)

## Features

- 🚀 **FastAPI** - Modern, fast web framework for building APIs with Python 3.7+
- 📊 **Three Database Support**: MongoDB, MySQL, and PostgreSQL
- 🔄 **Async Operations** - Fully asynchronous database operations
- 📝 **CRUD Operations** - Complete Create, Read, Update, Delete operations for each database
- 🧪 **Testing** - Basic test suite included
- 🐳 **Docker Support** - Docker Compose setup for easy development
- 📚 **Auto-generated API Documentation** - Swagger UI and ReDoc

## Project Structure

```
fastapi-mongo-mysql-postgresql-api/
├── app/
│   ├── database/           # Database connection modules
│   │   ├── mongodb.py     # MongoDB connection
│   │   ├── mysql.py       # MySQL connection
│   │   └── postgresql.py  # PostgreSQL connection
│   ├── models/            # Data models
│   │   ├── mongo_models.py
│   │   ├── mysql_models.py
│   │   └── postgresql_models.py
│   ├── routers/           # API route handlers
│   │   ├── mongodb_routes.py
│   │   ├── mysql_routes.py
│   │   └── postgresql_routes.py
│   └── config.py          # Application configuration
├── tests/                 # Test suite
├── main.py               # Application entry point
├── requirements.txt      # Python dependencies
├── docker-compose.yml    # Docker setup for databases
├── Dockerfile           # Application container
└── .env.example         # Environment variables template
```

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/moreskylab/fastapi-mongo-mysql-postgresql-api.git
cd fastapi-mongo-mysql-postgresql-api
```

### 2. Set up Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your database configurations
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Databases (using Docker)

```bash
# Start all databases
docker-compose up -d

# Check if containers are running
docker-compose ps
```

### 5. Run the Application

```bash
# Development mode
uvicorn main:app --reload

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 6. Access the API

- **API Documentation (Swagger)**: http://localhost:8000/docs
- **Alternative Documentation (ReDoc)**: http://localhost:8000/redoc
- **API Base URL**: http://localhost:8000

## API Endpoints

### Root Endpoints
- `GET /` - API information and available endpoints
- `GET /health` - Health check

### MongoDB Endpoints
- `POST /api/v1/mongodb/users/` - Create user
- `GET /api/v1/mongodb/users/` - Get all users
- `GET /api/v1/mongodb/users/{user_id}` - Get user by ID
- `PUT /api/v1/mongodb/users/{user_id}` - Update user
- `DELETE /api/v1/mongodb/users/{user_id}` - Delete user

### MySQL Endpoints
- `POST /api/v1/mysql/users/` - Create user
- `GET /api/v1/mysql/users/` - Get all users
- `GET /api/v1/mysql/users/{user_id}` - Get user by ID
- `PUT /api/v1/mysql/users/{user_id}` - Update user
- `DELETE /api/v1/mysql/users/{user_id}` - Delete user

### PostgreSQL Endpoints
- `POST /api/v1/postgresql/users/` - Create user
- `GET /api/v1/postgresql/users/` - Get all users
- `GET /api/v1/postgresql/users/{user_id}` - Get user by ID
- `PUT /api/v1/postgresql/users/{user_id}` - Update user
- `DELETE /api/v1/postgresql/users/{user_id}` - Delete user

## Example Usage

### Create a User in MongoDB

```bash
curl -X POST "http://localhost:8000/api/v1/mongodb/users/" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Doe",
       "email": "john@example.com",
       "age": 30
     }'
```

### Get All Users from MySQL

```bash
curl -X GET "http://localhost:8000/api/v1/mysql/users/"
```

### Update a User in PostgreSQL

```bash
curl -X PUT "http://localhost:8000/api/v1/postgresql/users/1" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Jane Doe",
       "age": 25
     }'
```

## Database Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Database URLs
DATABASE_URL_MONGODB=mongodb://localhost:27017/fastapi_app
DATABASE_URL_MYSQL=mysql://user:password@localhost:3306/fastapi_app
DATABASE_URL_POSTGRESQL=postgresql://user:password@localhost:5432/fastapi_app

# Application Settings
APP_NAME=FastAPI Multi-Database API
APP_VERSION=1.0.0
DEBUG=True
```

### Database Schemas

#### User Model (Common structure across all databases)

```json
{
  "name": "string",
  "email": "string",
  "age": "integer",
  "created_at": "datetime" (auto-generated)
}
```

## Testing

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=app
```

## Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up --build

# Start in background
docker-compose up -d --build

# Stop services
docker-compose down
```

### Manual Docker Build

```bash
# Build the application image
docker build -t fastapi-multi-db .

# Run the container
docker run -p 8000:8000 fastapi-multi-db
```

## Technologies Used

- **FastAPI** - Web framework
- **MongoDB** with **Motor** - Async MongoDB driver
- **MySQL** with **aiomysql** + **SQLAlchemy** - Async MySQL driver
- **PostgreSQL** with **asyncpg** + **SQLAlchemy** - Async PostgreSQL driver
- **Pydantic** - Data validation and settings management
- **Uvicorn** - ASGI server
- **pytest** - Testing framework

## Development

### Adding New Endpoints

1. Create new model in appropriate `models/` file
2. Add database operations in corresponding `database/` module
3. Create route handlers in appropriate `routers/` file
4. Include router in `main.py`

### Database Migration

For SQL databases (MySQL/PostgreSQL), you can use Alembic for migrations:

```bash
# Initialize migrations
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Create users table"

# Apply migrations
alembic upgrade head
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
