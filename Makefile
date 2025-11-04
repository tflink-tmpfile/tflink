.PHONY: help install install-dev test test-cov clean build publish publish-test quick-test format lint version-patch version-minor version-major

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
	@echo ""
	@echo "Version management:"
	@echo "  make version-patch  - Bump patch version (0.1.0 -> 0.1.1)"
	@echo "  make version-minor  - Bump minor version (0.1.0 -> 0.2.0)"
	@echo "  make version-major  - Bump major version (0.1.0 -> 1.0.0)"
	@echo "  make release        - Complete release process (push tags + create release)"

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

# Version management
version-patch:
	python bump_version.py patch

version-minor:
	python bump_version.py minor

version-major:
	python bump_version.py major

release:
	@echo "🚀 Starting release process..."
	@echo ""
	@git push
	@echo "✓ Code pushed"
	@TAG=$$(git describe --tags --abbrev=0 2>/dev/null || echo "none"); \
	if [ "$$TAG" != "none" ]; then \
		echo "✓ Pushing tag $$TAG..."; \
		git push origin $$TAG; \
		echo ""; \
		echo "✅ Release ready!"; \
		echo ""; \
		echo "📋 Next: Create GitHub Release at:"; \
		echo "   https://github.com/tflink-tmpfile/tflink/releases/new?tag=$$TAG"; \
	else \
		echo "❌ No tag found. Run 'make version-patch/minor/major' first"; \
	fi
