#!/bin/bash

# Run tests with coverage

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

pip install -r requirements_dev_full.txt

# Run tests with coverage
pytest --cov=monitoring --cov-report=html --cov-report=term

echo ""
echo "Coverage report generated in htmlcov/index.html"
