.PHONY: help build run dev stop clean logs shell test lint

# Default target
help:
	@echo "Available commands:"
	@echo "  build     - Build the Docker image"
	@echo "  run       - Run the application in production mode"
	@echo "  dev       - Run the application in development mode"
	@echo "  stop      - Stop all containers"
	@echo "  clean     - Remove containers and images"
	@echo "  logs      - Show application logs"
	@echo "  shell     - Open shell in running container"
	@echo "  test      - Run tests"
	@echo "  lint      - Run linting"

# Build the Docker image
build:
	docker build -t llm-api-tester .

# Run in production mode
run:
	docker-compose up -d

# Run in development mode
dev:
	docker-compose -f docker-compose.dev.yml up -d

# Stop all containers
stop:
	docker-compose down
	docker-compose -f docker-compose.dev.yml down

# Clean up containers and images
clean:
	docker-compose down --rmi all --volumes --remove-orphans
	docker-compose -f docker-compose.dev.yml down --rmi all --volumes --remove-orphans
	docker system prune -f

# Show logs
logs:
	docker-compose logs -f llm-api-tester

# Development logs
logs-dev:
	docker-compose -f docker-compose.dev.yml logs -f llm-api-tester-dev

# Open shell in container
shell:
	docker-compose exec llm-api-tester /bin/bash

# Development shell
shell-dev:
	docker-compose -f docker-compose.dev.yml exec llm-api-tester-dev /bin/bash

# Run tests
test:
	docker-compose exec llm-api-tester python -m pytest

# Run linting
lint:
	docker-compose exec llm-api-tester python -m flake8 .

# Production with nginx
run-prod:
	docker-compose --profile production up -d

# Build and run in one command
build-run: build run

# Build and run dev in one command
build-dev: build dev

# Quick restart
restart:
	docker-compose restart

# Show container status
status:
	docker-compose ps

# Show resource usage
stats:
	docker stats llm-api-tester
