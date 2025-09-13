# FastAPI Multi-Database API Template

A comprehensive FastAPI template that demonstrates how to build a robust API application with support for three different databases: **MongoDB**, **MySQL**, and **PostgreSQL**.

## Features

- ✅ **FastAPI** - Modern, fast web framework for building APIs
- ✅ **Multiple Databases** - MongoDB, MySQL, PostgreSQL support
- ✅ **Async Operations** - Fully asynchronous database operations
- ✅ **Pydantic Models** - Data validation and serialization
- ✅ **Auto-generated Documentation** - Interactive API docs with Swagger UI
- ✅ **Health Checks** - Database connectivity monitoring
- ✅ **CRUD Operations** - Complete Create, Read, Update, Delete examples
- ✅ **Docker Support** - Easy deployment with Docker Compose
- ✅ **Environment Configuration** - Flexible configuration management
- ✅ **Error Handling** - Comprehensive error handling and logging

## Project Structure

```
├── app/
│   ├── api/                    # API route handlers
│   │   ├── mongodb_routes.py   # MongoDB endpoints (Users)
│   │   ├── mysql_routes.py     # MySQL endpoints (Products)
│   │   └── postgresql_routes.py# PostgreSQL endpoints (Orders)
│   ├── core/
│   │   └── config.py           # Application configuration
│   ├── db/                     # Database connections
│   │   ├── mongodb.py          # MongoDB connection and operations
│   │   ├── mysql.py            # MySQL connection and operations
│   │   └── postgresql.py       # PostgreSQL connection and operations
│   └── models/
│       └── schemas.py          # Pydantic models for data validation
├── main.py                     # FastAPI application entry point
├── requirements.txt            # Python dependencies
├── docker-compose.yml          # Docker services configuration
├── Dockerfile                  # Application container
├── .env.example               # Environment variables template
└── README.md                  # This file
```

## Database Models

### MongoDB - Users Collection
- **id**: Unique identifier
- **name**: User's full name
- **email**: User's email address
- **age**: User's age (optional)
- **created_at**: Creation timestamp
- **updated_at**: Last update timestamp

### MySQL - Products Table
- **id**: Unique identifier
- **name**: Product name
- **description**: Product description (optional)
- **price**: Product price
- **category**: Product category
- **created_at**: Creation timestamp
- **updated_at**: Last update timestamp

### PostgreSQL - Orders Table
- **id**: Unique identifier
- **user_id**: Reference to user
- **product_id**: Reference to product
- **quantity**: Order quantity
- **total_amount**: Total order amount
- **created_at**: Creation timestamp
- **updated_at**: Last update timestamp

## Quick Start

### 1. Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd fastapi-mongo-mysql-postgresql-api

# Start all services
docker-compose up -d

# The API will be available at http://localhost:8000
```

### 2. Manual Setup

#### Prerequisites
- Python 3.11+
- MongoDB
- MySQL
- PostgreSQL

#### Installation

```bash
# Clone the repository
git clone <repository-url>
cd fastapi-mongo-mysql-postgresql-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment configuration
cp .env.example .env
# Edit .env with your database credentials

# Run the application
python main.py
```

## API Endpoints

### Root Endpoints
- `GET /` - API information and available endpoints
- `GET /health` - Application health check
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

### MongoDB Endpoints (Users)
- `GET /mongodb/health` - MongoDB health check
- `POST /mongodb/users` - Create a new user
- `GET /mongodb/users` - Get all users
- `GET /mongodb/users/{user_id}` - Get user by ID
- `PUT /mongodb/users/{user_id}` - Update user
- `DELETE /mongodb/users/{user_id}` - Delete user

### MySQL Endpoints (Products)
- `GET /mysql/health` - MySQL health check
- `POST /mysql/products` - Create a new product
- `GET /mysql/products` - Get all products
- `GET /mysql/products/{product_id}` - Get product by ID
- `PUT /mysql/products/{product_id}` - Update product
- `DELETE /mysql/products/{product_id}` - Delete product

### PostgreSQL Endpoints (Orders)
- `GET /postgresql/health` - PostgreSQL health check
- `POST /postgresql/orders` - Create a new order
- `GET /postgresql/orders` - Get all orders
- `GET /postgresql/orders/{order_id}` - Get order by ID
- `PUT /postgresql/orders/{order_id}` - Update order
- `DELETE /postgresql/orders/{order_id}` - Delete order

## Usage Examples

### Create a User (MongoDB)
```bash
curl -X POST "http://localhost:8000/mongodb/users" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Doe",
       "email": "john@example.com",
       "age": 30
     }'
```

### Create a Product (MySQL)
```bash
curl -X POST "http://localhost:8000/mysql/products" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Laptop",
       "description": "High-performance laptop",
       "price": 999.99,
       "category": "Electronics"
     }'
```

### Create an Order (PostgreSQL)
```bash
curl -X POST "http://localhost:8000/postgresql/orders" \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": "user-uuid-here",
       "product_id": "product-uuid-here",
       "quantity": 2,
       "total_amount": 1999.98
     }'
```

## Configuration

The application uses environment variables for configuration. Copy `.env.example` to `.env` and update the values:

```env
# API Settings
APP_NAME=FastAPI Multi-Database API
DEBUG=true

# MongoDB
MONGODB_URL=mongodb://localhost:27017
MONGODB_DATABASE=fastapi_db

# MySQL
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=password
MYSQL_DATABASE=fastapi_db

# PostgreSQL
POSTGRESQL_HOST=localhost
POSTGRESQL_PORT=5432
POSTGRESQL_USER=postgres
POSTGRESQL_PASSWORD=password
POSTGRESQL_DATABASE=fastapi_db
```

## Development

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Code Formatting
```bash
# Install formatting tools
pip install black isort

# Format code
black .
isort .
```

## Deployment

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

### Production Considerations
- Update database credentials and security settings
- Configure CORS settings appropriately
- Set up proper logging and monitoring
- Use environment-specific configuration files
- Implement authentication and authorization
- Set up database backups and monitoring

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you have any questions or issues, please open an issue on GitHub or contact the maintainers.
