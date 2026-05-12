#!/bin/bash

# Run development server

set -e

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Create default config
echo "Setting up default configuration..."
python manage.py shell << END
from monitoring.models import MonitoringConfig
if not MonitoringConfig.objects.exists():
    MonitoringConfig.objects.create(
        name='Default',
        cpu_threshold=80.0,
        memory_threshold=85.0,
        disk_threshold=90.0,
        monitoring_enabled=True,
        check_interval=5,
        data_retention_days=30
    )
    print("✓ Default configuration created")
END

# Start server
echo "Starting development server..."
python manage.py runserver 0.0.0.0:8000
