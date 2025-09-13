# FastAPI Multi-Database API

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

FastAPI application with SQLAlchemy, Alembic, pytest, Black, and Docker support. Uses SQLite by default but designed to support MongoDB, MySQL, and PostgreSQL.

## Working Effectively

### Local Development (Recommended for Development)
- Install dependencies: `pip3 install -r requirements.txt` -- takes 30 seconds. NEVER CANCEL.
- Navigate to app directory: `cd app`
- Start the development server: `uvicorn main:app --host 0.0.0.0 --port 8000 --reload`
- Run tests: `python3 -m pytest -vvs` -- takes <1 second (4 tests pass)
- Format code: `python3 -m black .` -- takes <1 second. NEVER CANCEL.
- Import the application: `python3 -c "import main; print('App imported successfully')"`

### Docker Development (Production-like Environment)
- Build the container: `DOCKER_BUILDKIT=0 make build` -- takes 25 seconds. NEVER CANCEL. Set timeout to 60+ seconds.
- Start the application: `DOCKER_BUILDKIT=0 make up` -- starts server with auto-reload
- Run tests in container: `DOCKER_BUILDKIT=0 make test` -- takes 2 seconds. NEVER CANCEL.
- Format code in container: `DOCKER_BUILDKIT=0 make lint` -- takes <1 second. NEVER CANCEL.
- Stop the application: `make down` or Ctrl+C
- Access container shell: `make bash`

### Database Migrations
- Initialize migrations (already done): `alembic init migrations`
- Create migration: `make migrate msg="your_migration_message"`
- Apply migrations: `make exec-migration`
- Migrations are automatically applied when using `make up`

## Critical Build Requirements

### NEVER CANCEL - Docker Build Issues
- ALWAYS use `DOCKER_BUILDKIT=0` prefix for Docker commands to avoid SSL certificate issues
- Docker build takes 25 seconds on first run, subsequent builds are faster with caching
- If Docker build fails with SSL errors, use `DOCKER_BUILDKIT=0` and try again
- Set timeouts to 60+ seconds for all Docker build commands

### Local vs Docker Development
- **Local development** is FASTER for iteration: 30s setup, instant server restart
- **Docker development** ensures production parity: 25s build, slower iteration
- ALWAYS test both local and Docker environments before committing changes

## Validation

### Required Manual Testing After Changes
- ALWAYS test the complete API workflow after making changes:
  1. Start the server (local or Docker)
  2. Create an item: `curl -X POST http://localhost:8000/items/ -H "Content-Type: application/json" -d '{"name": "Test Item", "description": "Testing"}'`
  3. Retrieve the item: `curl http://localhost:8000/items/1`
  4. Verify the API documentation: `curl http://localhost:8000/` (should show Swagger UI)
  5. Check OpenAPI spec: `curl http://localhost:8000/openapi.json`

### Pre-commit Validation
- ALWAYS run `python3 -m black .` before committing (or `make lint` for Docker)
- ALWAYS run `python3 -m pytest -vvs` before committing (or `make test` for Docker)
- ALWAYS manually test API endpoints after making changes to routers or models

## Common Issues and Solutions

### Import Errors
- All imports in `routers/` should use `core.database` not `database`
- All imports in `services/` should use `models.item` not `models.item_service`
- The main application imports are in `main.py` with proper error handling

### Database Schema Issues
- The model uses `id` as primary key, not `{model_name}_id`
- Service base class assumes `id` field for all operations
- SQLite database file is `database.sqlite` in app directory

### Docker Issues
- Use `DOCKER_BUILDKIT=0` for all Docker commands to avoid SSL issues
- Makefile uses `docker compose` (not `docker-compose`) syntax
- Alembic configuration uses `sqlite:///database.sqlite` format

### API Routing Issues
- Router prefixes are defined once in `main.py` when including routers
- Individual routers should NOT define their own prefix to avoid duplication
- Routes are: `POST /items/` and `GET /items/{item_id}`

## Architecture Overview

### Key Directories
```
app/
├── main.py              # FastAPI application entry point
├── core/
│   ├── database.py      # Database configuration and session management
│   └── logger.py        # Logging configuration
├── models/
│   └── item.py          # SQLAlchemy models
├── schemas/
│   └── item.py          # Pydantic schemas for API contracts
├── routers/
│   └── item.py          # API route handlers
├── services/
│   ├── base.py          # Base service class with CRUD operations
│   └── item.py          # Item-specific service implementation
├── tests/
│   ├── conftest.py      # Test configuration
│   └── test_items.py    # API endpoint tests
└── migrations/          # Alembic database migrations
```

### Current API Endpoints
- `GET /` - Swagger UI documentation
- `GET /openapi.json` - OpenAPI specification
- `POST /items/` - Create a new item
- `GET /items/{item_id}` - Retrieve an item by ID

### Database Configuration
- **Default**: SQLite (`database.sqlite`)
- **Supported**: MongoDB, MySQL, PostgreSQL (configuration in `core/database.py`)
- **ORM**: SQLAlchemy with declarative base
- **Migrations**: Alembic for schema versioning

## Common Commands Reference

### Development Workflow
```bash
# Setup
pip3 install -r requirements.txt
cd app

# Start development
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# In another terminal
curl -X POST http://localhost:8000/items/ -H "Content-Type: application/json" -d '{"name": "Test", "description": "Test item"}'
curl http://localhost:8000/items/1

# Format and test
python3 -m black .
python3 -m pytest -vvs
```

### Docker Workflow
```bash
# Build and start
DOCKER_BUILDKIT=0 make build
DOCKER_BUILDKIT=0 make up

# In another terminal
curl -X POST http://localhost:8000/items/ -H "Content-Type: application/json" -d '{"name": "Docker Test", "description": "Via container"}'

# Test and lint
DOCKER_BUILDKIT=0 make test
DOCKER_BUILDKIT=0 make lint

# Stop
make down
```

### Troubleshooting Commands
```bash
# Check if app imports correctly
cd app && python3 -c "import main; print('OK')"

# Check database file
ls -la app/database.sqlite

# Check Docker container status
docker ps

# View container logs
docker logs app
```