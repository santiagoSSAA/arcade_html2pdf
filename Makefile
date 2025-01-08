.PHONY: help

help:
	@echo "🛠️ html2pdf Commands:\n"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ## Install the poetry environment and install the pre-commit hooks
	@echo "📦 Checking if Poetry is installed"
	@if ! command -v poetry &> /dev/null; then \
		echo "📦 Installing Poetry with pip"; \
		pip install poetry; \
	else \
		echo "📦 Poetry is already installed"; \
	fi
	@echo "📦 Checking for poetry.lock file"
	@if [ ! -f poetry.lock ]; then \
		echo "📦 Creating poetry.lock file"; \
		poetry lock; \
	fi
	@echo "🚀 Installing package in development mode with all extras"
	poetry install --all-extras

.PHONY: build
build: clean-build ## Build wheel file using poetry
	@echo "🚀 Creating wheel file"
	poetry build

.PHONY: clean-build
clean-build: ## clean build artifacts
	rm -rf dist

.PHONY: clean-dist
clean-dist: ## Clean all built distributions
	@echo "🗑️ Cleaning dist directory"
	@rm -rf dist

.PHONY: test
test: ## Test the code with pytest
	@echo "🚀 Testing code: Running pytest"
	@poetry run pytest -W ignore -v --cov --cov-config=pyproject.toml --cov-report=xml

.PHONY: coverage
coverage: ## Generate coverage report
	@echo "coverage report"
	coverage report
	@echo "Generating coverage report"
	coverage html

.PHONY: bump-version
bump-version: ## Bump the version in the pyproject.toml file
	@echo "🚀 Bumping version in pyproject.toml"
	poetry version patch

.PHONY: check
check: ## Run code quality tools.
	@echo "🚀 Checking Poetry lock file consistency with 'pyproject.toml': Running poetry check --lock"
	@poetry check --lock
	@echo "🚀 Linting code: Running pre-commit"
	@poetry run pre-commit run -a
	@echo "🚀 Static type checking: Running mypy"
	@poetry run mypy $(git ls-files '*.py')