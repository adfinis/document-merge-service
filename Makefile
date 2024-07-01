.PHONY: help install install-dev start test
.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort -k 1,1 | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

start: ## Start the development server
	@docker-compose up -d --build

test: ## Test the project
	docker-compose exec document-merge-service poetry run sh -c "ruff format --diff --fix . && ruff check --diff . && mypy document_merge_service && pytest --no-cov-on-fail --cov --create-db"

shell: ## Shell into document merge service
	@docker-compose exec document-merge-service poetry shell

format: ## Format python code with ruff check
	@docker-compose exec document-merge-service poetry run ruff format --diff .

dmypy: ## Run mypy locally (starts a deamon for performance)
	dmypy run document_merge_service
