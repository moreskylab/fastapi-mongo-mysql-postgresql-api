.PHONY: help install install-dev run test test-basic clean format lint docker-up docker-down

help:	## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:	## Install production dependencies
	pip install -r requirements.txt

install-dev:	## Install development dependencies
	pip install -r requirements-dev.txt

run:	## Run the FastAPI application
	python main.py

test-basic:	## Run basic structure validation
	python test_basic.py

test:	## Run full test suite (requires dev dependencies)
	pytest

format:	## Format code with black and isort
	black .
	isort .

lint:	## Run linting with flake8
	flake8 .

clean:	## Clean up Python cache files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

docker-up:	## Start all services with Docker Compose
	docker-compose up -d

docker-down:	## Stop all Docker services
	docker-compose down

docker-logs:	## View Docker logs
	docker-compose logs -f

# Database specific commands
db-mongo:	## Start only MongoDB
	docker-compose up -d mongodb

db-mysql:	## Start only MySQL
	docker-compose up -d mysql

db-postgres:	## Start only PostgreSQL
	docker-compose up -d postgresql