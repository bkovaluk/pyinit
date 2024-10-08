# Variables
PACKAGE = potara

.PHONY: help install init format lint test coverage clean build run pre-commit

# Default target
help:
	@echo "Usage:"
	@echo "  make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  install     Install dependencies using Poetry"
	@echo "  init        Initialize the project (install, pre-commit)"
	@echo "  format      Format code using Ruff"
	@echo "  lint        Lint code using Ruff"
	@echo "  test        Run tests using Pytest"
	@echo "  coverage    Run tests with coverage report"
	@echo "  clean       Clean up build artifacts"
	@echo "  build       Build the package"
	@echo "  run         Run the application"
	@echo "  pre-commit  Install pre-commit hooks"
	@echo "  help        Show this help message"

# Install dependencies using Poetry
install:
	poetry install

# Initialize the project
init: install pre-commit

# Format code using Ruff
format:
	poetry run ruff check . --fix

# Lint code using Ruff
lint:
	poetry run ruff check .

# Run tests using Pytest
test:
	poetry run pytest

# Run tests with coverage report
coverage:
	poetry run pytest --cov=$(PACKAGE) tests/
	poetry run coverage html
	@echo "Open htmlcov/index.html in your browser to view the coverage report."

# Clean up build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf htmlcov/
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type d -name '*.egg-info' -exec rm -rf {} +

# Build the package
build:
	poetry build

# Run the application
run:
	poetry run python $(PACKAGE)/cli.py

# Install pre-commit hooks
pre-commit:
	poetry run pre-commit install
