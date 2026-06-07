#!/bin/bash
# Pre-hook script to ensure code quality before commit

echo "Running tests..."
export PYTHONPATH=$PYTHONPATH:.
pytest tests/
if [ $? -ne 0 ]; then
    echo "Tests failed. Aborting commit."
    exit 1
fi
echo "Tests passed."
