#!/bin/bash

# Development environment setup with hot reload

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

# Install development dependencies
pip install -r requirements_dev.txt

# Run migrations
python manage.py migrate

# Start development server with auto-reload
watchmedo shell-command \
    --patterns="*.py" \
    --recursive \
    --command='python manage.py runserver 0.0.0.0:8000 --nothreading' \
    .
