#!/bin/bash
# Helper script to run the test app with proper library paths set

# Detect Homebrew prefix
if [ -d "/opt/homebrew" ]; then
    HOMEBREW_PREFIX="/opt/homebrew"
else
    HOMEBREW_PREFIX="/usr/local"
fi

# Set library paths for macOS
export DYLD_LIBRARY_PATH="$HOMEBREW_PREFIX/lib:$DYLD_LIBRARY_PATH"
export LD_LIBRARY_PATH="$HOMEBREW_PREFIX/lib:$LD_LIBRARY_PATH"

# Run the test app with all arguments passed through
poetry run python test_app/main.py "$@"
