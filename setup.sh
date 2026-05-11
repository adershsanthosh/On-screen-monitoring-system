#!/bin/bash

# On-screen Monitoring System Setup Script

set -e

echo "================================"
echo "System Monitoring Setup Script"
echo "================================"
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🐍 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📚 Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Copy environment file
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "   Please edit .env with your configuration"
fi

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

# Create superuser
echo "👤 Creating superuser..."
echo "   (You can skip this by pressing Ctrl+C and run manually with:)"
echo "   python manage.py createsuperuser"
python manage.py createsuperuser --noinput || true

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "================================"
echo "✅ Setup complete!"
echo "================================"
echo ""
echo "To start the development server, run:"
echo "  python manage.py runserver 0.0.0.0:8000"
echo ""
echo "To start with Celery (background tasks), run:"
echo "  1. celery -A config worker -l info"
echo "  2. celery -A config beat -l info"
echo "  3. python manage.py runserver"
echo ""
echo "Access:"
echo "  Dashboard: http://localhost:8000"
echo "  Admin:     http://localhost:8000/admin"
echo "  API:       http://localhost:8000/api/"
echo ""
