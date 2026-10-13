SHELL := /bin/bash
.DEFAULT_GOAL := help

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  %-14s %s\n", $$1, $$2}'

bootstrap:  ## Create the environment from scratch (idempotent)
	uv sync --locked
	uv run pre-commit install --install-hooks

lint:  ## Static analysis
	uv run ruff check .
	uv run ruff format --check .
	uv run mypy src

format:  ## Apply automatic fixes
	uv run ruff check --fix .
	uv run ruff format .

test:  ## Tests + coverage gate (floor lives in pyproject.toml)
	uv run pytest --cov --cov-report=term-missing --cov-report=xml

check: lint test  ## Exactly what CI runs

audit:  ## Dependency vulnerabilities against OSV.dev
	uv run pip-audit --progress-spinner off

secrets:  ## Scan the whole tree for secrets
	uv run pre-commit run detect-secrets --all-files

docker-build:  ## Build the image the same way CI does
	docker build -t $(shell basename $$PWD):local .

clean:  ## Remove local caches and build outputs
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov coverage.xml dist build *.egg-info
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
