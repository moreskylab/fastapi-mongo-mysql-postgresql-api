# FastAPI Multi-Database Template

## Development Setup

### Prerequisites
- Python 3.11+
- Docker and Docker Compose (for database services)

### Quick Start
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Copy environment variables: `cp .env.example .env`
4. Start databases: `docker-compose up -d mongodb mysql postgresql`
5. Run the application: `python main.py`

### Testing the Template
Run the basic validation test: `python test_basic.py`

### API Documentation
Once running, visit:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

### Database Models

#### MongoDB (Users)
- Create user: `POST /mongodb/users`
- Get users: `GET /mongodb/users`
- Get user: `GET /mongodb/users/{id}`
- Update user: `PUT /mongodb/users/{id}`
- Delete user: `DELETE /mongodb/users/{id}`

#### MySQL (Products)
- Create product: `POST /mysql/products`
- Get products: `GET /mysql/products`
- Get product: `GET /mysql/products/{id}`
- Update product: `PUT /mysql/products/{id}`
- Delete product: `DELETE /mysql/products/{id}`

#### PostgreSQL (Orders)
- Create order: `POST /postgresql/orders`
- Get orders: `GET /postgresql/orders`
- Get order: `GET /postgresql/orders/{id}`
- Update order: `PUT /postgresql/orders/{id}`
- Delete order: `DELETE /postgresql/orders/{id}`

### Health Checks
- Overall: `GET /health`
- MongoDB: `GET /mongodb/health`
- MySQL: `GET /mysql/health`
- PostgreSQL: `GET /postgresql/health`