.PHONY: help install install-dev test test-cov clean build publish publish-test quick-test format lint

help:
	@echo "tflink - Makefile Commands"
	@echo ""
	@echo "Available commands:"
	@echo "  make install        - Install library"
	@echo "  make install-dev    - Install library with development dependencies"
	@echo "  make test           - Run tests"
	@echo "  make test-cov       - Run tests with coverage report"
	@echo "  make quick-test     - Run quick functionality test"
	@echo "  make format         - Format code"
	@echo "  make lint           - Run code checks"
	@echo "  make clean          - Clean build files"
	@echo "  make build          - Build distribution packages"
	@echo "  make publish-test   - Publish to TestPyPI"
	@echo "  make publish        - Publish to PyPI"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

test:
	pytest

test-cov:
	pytest --cov=tflink --cov-report=html --cov-report=term-missing

quick-test:
	python quick_test.py

format:
	black tflink tests examples

lint:
	flake8 tflink tests
	mypy tflink

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

publish-test: build
	twine check dist/*
	twine upload --repository testpypi dist/*

publish: build
	twine check dist/*
	twine upload dist/*
