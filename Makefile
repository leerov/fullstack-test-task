.PHONY: help up down migrate logs build

help: ## Show this help message
	@echo "Available commands:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

up: ## Start the project in detached mode
	docker compose -f docker-compose.dev.yml up -d

down: ## Stop and remove containers
	docker compose -f docker-compose.dev.yml down

migrate: ## Run database migrations
	docker compose -f docker-compose.dev.yml exec backend alembic upgrade head

logs: ## Follow logs of all services
	docker compose -f docker-compose.dev.yml logs -f

build: ## Build or rebuild services
	docker compose -f docker-compose.dev.yml build