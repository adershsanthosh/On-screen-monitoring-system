# On-screen Monitoring System

A comprehensive real-time system monitoring solution built with Python Django. Monitor CPU, memory, disk usage, running processes, and set up alerts based on custom thresholds.

## Table of Contents
- [Features](#features)
- [Quick Start](#quick-start)
- [Fork & Setup](#fork--setup)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
- [Contributing](#contributing)

## Features

🔍 **Real-time Monitoring**
- CPU usage tracking and history
- Memory usage monitoring
- Disk space tracking
- Network statistics
- Process information and resource usage

📊 **Interactive Dashboard**
- Real-time visualization with charts
- Historical data analysis
- Top processes by memory/CPU
- System metrics overview

🚨 **Alert System**
- Threshold-based automatic alerts
- Severity levels (Info, Warning, Critical)
- Alert history and tracking
- Manual alert resolution

📈 **REST API**
- RESTful API for all metrics
- Real-time data endpoints  
- Process information endpoints
- Alert management endpoints

⚙️ **Background Tasks**
- Periodic metric collection
- Process monitoring
- Threshold checking
- Automatic data cleanup

## Quick Start

### Prerequisites
- Python 3.8+
- Git
- pip (Python package manager)
- Redis (optional, for background tasks)

### 5-Minute Setup

```bash
# 1. Clone the repository
git clone https://github.com/adershsanthosh/On-screen-monitoring-system.git
cd On-screen-monitoring-system

# 2. Virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment
cp .env.example .env

# 5. Initialize database
python manage.py migrate
python manage.py createsuperuser

# 6. Run
python manage.py runserver 0.0.0.0:8000
```

**Access:**
- Dashboard: http://localhost:8000
- Admin: http://localhost:8000/admin
- API: http://localhost:8000/api/

## Fork & Setup

### For Contributors

#### Step 1: Fork the Repository
1. Visit https://github.com/adershsanthosh/On-screen-monitoring-system
2. Click **Fork** button (top-right)
3. This creates a copy under your GitHub account

#### Step 2: Clone Your Fork
```bash
# Clone your forked repository
git clone https://github.com/YOUR-USERNAME/On-screen-monitoring-system.git
cd On-screen-monitoring-system

# Add upstream (original repo)
git remote add upstream https://github.com/adershsanthosh/On-screen-monitoring-system.git

# Verify remotes
git remote -v
```

#### Step 3: Setup Development Environment
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies + dev tools
pip install -r requirements.txt
pip install -r requirements_dev.txt

# Copy environment file
cp .env.example .env
```

#### Step 4: Initialize Database
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Create default config (optional)
python manage.py shell << END
from monitoring.models import MonitoringConfig
if not MonitoringConfig.objects.exists():
    MonitoringConfig.objects.create(name='Default')
END
```

#### Step 5: Start Development Server
```bash
# Option 1: Simple server
python manage.py runserver 0.0.0.0:8000

# Option 2: With hot-reload
./dev.sh

# Option 3: With Celery background tasks
# Terminal 1
celery -A config worker -l info

# Terminal 2
celery -A config beat -l info

# Terminal 3
python manage.py runserver
```

#### Step 6: Make Changes
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and test
python manage.py test
pytest --cov=monitoring

# Format code
black .
isort .
flake8 .

# Commit changes
git add .
git commit -m "feat: Add your feature"

# Push to your fork
git push origin feature/your-feature-name
```

#### Step 7: Keep Fork Updated
```bash
# Fetch upstream changes
git fetch upstream

# Rebase your branch
git rebase upstream/main

# Push updated branch
git push origin feature/your-feature-name -f
```

#### Step 8: Create Pull Request
1. Go to your forked repo on GitHub
2. Click **Compare & pull request**
3. Add title and description
4. Click **Create pull request**

### Automated Setup Script

```bash
# Make executable
chmod +x setup.sh run.sh test.sh

# Run setup
./setup.sh

# Run server
./run.sh

# Run tests  
./test.sh
```

### Docker Setup

```bash
# Start all services
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# View logs
docker-compose logs -f web

# Stop services
docker-compose down
```

## Project Structure

```
├── config/                 # Django config
│   ├── settings.py        # Main settings
│   ├── urls.py            # URL routing
│   └── celery.py          # Task scheduler
├── monitoring/             # Main app
│   ├── models.py          # Database models
│   ├── views.py           # API viewsets
│   ├── utils.py           # Utilities
│   ├── tasks.py           # Background tasks
│   ├── templates/
│   │   └── dashboard.html # Dashboard UI
│   └── management/
│       └── commands/      # CLI commands
├── manage.py              # Django CLI
├── requirements.txt       # Dependencies
├── docker-compose.yml     # Docker config
├── README.md              # This file
├── QUICKSTART.md          # Quick start
└── API_DOCUMENTATION.md   # API reference
```

## Technology Stack

- **Framework**: Django 4.2
- **API**: Django REST Framework
- **Tasks**: Celery + Redis
- **Frontend**: Bootstrap 5, Chart.js
- **Database**: SQLite (dev), PostgreSQL (prod)
- **Monitoring**: psutil
- **Deployment**: Docker, Gunicorn

## API Endpoints

**Metrics:**
- `GET /api/metrics/` - All metrics
- `GET /api/metrics/current/` - Real-time
- `GET /api/metrics/history/?hours=24` - History

**Processes:**
- `GET /api/processes/top_processes/?limit=10` - Top processes
- `GET /api/processes/current/` - All processes

**Alerts:**
- `GET /api/alerts/` - All alerts
- `GET /api/alerts/unresolved/` - Active alerts
- `POST /api/alerts/{id}/resolve/` - Resolve alert

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for full reference.

## Configuration

### Environment Variables (.env)

```bash
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_ENGINE=django.db.backends.sqlite3

# Redis
REDIS_URL=redis://localhost:6379/0

# Monitoring
MONITOR_INTERVAL=5
MONITOR_HISTORY_RETENTION=86400
```

### Alert Thresholds

Configure via Django Admin (`/admin/`):
- CPU threshold (default 80%)
- Memory threshold (default 85%)
- Disk threshold (default 90%)

## Running Tests

```bash
# Django tests
python manage.py test

# Pytest
pytest
pytest --cov=monitoring --cov-report=html

# Code quality
flake8 .
black . --check
isort . --check-only
```

## Contributing

### Workflow
1. Fork repository
2. Clone your fork
3. Create feature branch: `git checkout -b feature/amazing-feature`
4. Make changes
5. Add tests
6. Run tests: `pytest`
7. Commit: `git commit -m "Add amazing feature"`
8. Push: `git push origin feature/amazing-feature`
9. Open Pull Request

### Code Style
- Follow PEP 8
- Use `black` for formatting
- Use `isort` for imports
- Write docstrings

### Commit Format
```
type: description

feat: Add feature
fix: Fix bug
docs: Update documentation
```

## Issues

### Report Bug
- Check [existing issues](https://github.com/adershsanthosh/On-screen-monitoring-system/issues)
- Create issue with:
  - Steps to reproduce
  - Expected behavior
  - Actual behavior
  - Python/Django version

### Request Feature
- Use issue tracker with `enhancement` label
- Describe use case clearly

## Troubleshooting

**Port 8000 in use:**
```bash
python manage.py runserver 8001
```

**Database locked:**
```bash
rm db.sqlite3
python manage.py migrate
```

**Redis not available:**
```bash
redis-server  # Install if needed
```

**Permission denied:**
```bash
sudo python manage.py runserver  # For system processes
```

## License

MIT License - See LICENSE file

## Acknowledgments

- Django & DRF
- psutil for system monitoring
- Celery for task scheduling
- Bootstrap & Chart.js for UI

---

**⭐ Star this repo if you find it helpful!**

For more details, see [QUICKSTART.md](QUICKSTART.md) and [API_DOCUMENTATION.md](API_DOCUMENTATION.md).
