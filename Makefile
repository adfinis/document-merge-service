.PHONY: help start test shell format dmypy
.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort -k 1,1 | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

start: ## Start the development server
	@docker compose up -d --build

test: ## Test the project
	@docker compose exec document-merge-service sh -c "ruff format --diff . && ruff check --diff . && mypy document_merge_service && pytest --no-cov-on-fail --cov --create-db"

shell: ## Shell into document merge service
	@docker compose exec document-merge-service bash

format: ## Format python code with ruff check
	@docker compose exec document-merge-service ruff format --diff .

dmypy: ## Run mypy locally (starts a deamon for performance)
	dmypy run document_merge_service
