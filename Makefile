.PHONY: setup prebuild test lint format clean help test-app

# Default target
help:
	@echo "Available targets:"
	@echo "  setup     - Complete setup (install dependencies and run prebuild)"
	@echo "  prebuild  - Run prebuild for all packages"
	@echo "  test      - Run all tests"
	@echo "  test-app  - Run test application (interactive)"
	@echo "  lint      - Run linting checks"
	@echo "  format    - Format code with black"
	@echo "  clean     - Clean generated files"

# Complete setup process
setup:
	@echo "Setting up Cypherock SDK..."
	@echo "1. Installing dependencies..."
	@HOMEBREW_PREFIX=$$([ -d "/opt/homebrew" ] && echo "/opt/homebrew" || echo "/usr/local") && \
	 export LIBRARY_PATH="$$HOMEBREW_PREFIX/lib:$$LIBRARY_PATH" && \
	 export CPPFLAGS="-I$$HOMEBREW_PREFIX/include $$CPPFLAGS" && \
	 export LDFLAGS="-L$$HOMEBREW_PREFIX/lib $$LDFLAGS" && \
	 poetry install
	@echo "2. Running prebuild..."
	$(MAKE) prebuild
	@echo "Setup complete!"

# Run prebuild for all packages
prebuild:
	@echo "Running prebuild for all packages..."
	@echo "Core package..."
	poetry run packages/core/scripts/prebuild.sh
	@echo "App Manager package..."
	poetry run packages/app_manager/scripts/prebuild.sh
	@echo "BTC App package..."
	poetry run packages/app_btc/scripts/prebuild.sh
	@echo "Prebuild complete!"

# Run all tests (runs each package individually)
test: prebuild
	@echo "Running all tests..."
	@echo "Running core package tests..."
	poetry run pytest packages/core/tests/ -v
	@echo "Running app_manager package tests..."
	poetry run pytest packages/app_manager/tests/ -v
	@echo "Running app_btc package tests..."
	poetry run pytest packages/app_btc/tests/ -v
	@echo "Running util package tests..."
	poetry run pytest packages/util/tests/ -v

# Run test application (for testing with actual firmware)
test-app: prebuild
	@echo "Running test application..."
	@echo "Use 'poetry run python test_app/main.py --help' for usage"
	@HOMEBREW_PREFIX=$$([ -d "/opt/homebrew" ] && echo "/opt/homebrew" || echo "/usr/local") && \
	 export DYLD_LIBRARY_PATH="$$HOMEBREW_PREFIX/lib:$$DYLD_LIBRARY_PATH" && \
	 export LD_LIBRARY_PATH="$$HOMEBREW_PREFIX/lib:$$LD_LIBRARY_PATH" && \
	 poetry run python test_app/main.py --list-devices || true

# Run linting
lint:
	@echo "Running linting checks..."
	poetry run ruff check .

# Format code
format:
	@echo "Formatting code..."
	poetry run black .

# Clean generated files
clean:
	@echo "Cleaning generated files..."
	@echo "Cleaning Python cache files..."
	find . -name "*.pyc" -not -path "./.git/*" -not -path "./*/.git/*" -not -path "./submodules/*" -delete
	find . -name "__pycache__" -type d -not -path "./.git/*" -not -path "./*/.git/*" -not -path "./submodules/*" -exec rm -rf {} +
	@echo "Cleaning build artifacts..."
	find . -name "*.egg-info" -type d -not -path "./.git/*" -not -path "./*/.git/*" -not -path "./submodules/*" -exec rm -rf {} +
	find . -name "dist" -type d -not -path "./.git/*" -not -path "./*/.git/*" -not -path "./submodules/*" -exec rm -rf {} +
	find . -name "build" -type d -not -path "./.git/*" -not -path "./*/.git/*" -not -path "./submodules/*" -exec rm -rf {} +
	@echo "Cleaning generated proto files..."
	find packages -path "*/src/*/proto/generated" -type d -exec rm -rf {} +
	find packages -path "*/src/*/encoders/proto/generated" -type d -exec rm -rf {} +
	@echo "Clean complete!"
