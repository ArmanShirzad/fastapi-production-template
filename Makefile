.PHONY: help install dev test test-integration lint format docker-build docker-run docker-compose-up clean

# Default target
help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

dev: ## Run development server
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test: ## Run tests with coverage
	pytest tests/ -v --cov=app --cov-report=html --cov-report=term

test-integration: ## Run integration tests (expects DATABASE_URL); skips cleanly if not set
	@if [ -z "$$DATABASE_URL" ]; then \
		echo "Skipping integration tests: DATABASE_URL is not set."; \
	else \
		pytest tests/ -v -m integration --cov=app --cov-report=term; \
		rc=$$?; \
		if [ $$rc -eq 5 ]; then \
			echo "No integration tests collected; treating as success."; \
			exit 0; \
		else \
			exit $$rc; \
		fi; \
	fi

lint: ## Run linting
	ruff check app/ tests/
	ruff format --check app/ tests/

format: ## Format code
	ruff format app/ tests/

docker-build: ## Build Docker image
	docker build -t fastapi-template .

docker-run: ## Run Docker container locally
	docker run -p 8000:8000 --env-file .env fastapi-template

docker-compose-up: ## Start full stack with Docker Compose
	docker-compose up --build

docker-compose-down: ## Stop Docker Compose services
	docker-compose down

clean: ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
