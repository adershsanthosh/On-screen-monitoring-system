# Django & Development Server Configuration
# Install dependencies first: pip install -r requirements.txt

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up Environment
```bash
cp .env.example .env
# Edit .env with your configuration if needed
```

### 3. Initialize Database
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 5. Run Development Server
```bash
# For basic development:
python manage.py runserver 0.0.0.0:8000

# For real-time updates with WebSockets (requires daphne):
daphne -b 0.0.0.0 -p 8000 config.asgi:application
```

### 6. (Optional) Run Celery Worker for Background Tasks
```bash
celery -A config worker -l info
```

### 7. (Optional) Run Celery Beat Scheduler
```bash
celery -A config beat -l info
```

## API Endpoints

### System Metrics
- `GET /api/metrics/` - List all metrics
- `GET /api/metrics/latest/` - Get latest metrics
- `GET /api/metrics/current/` - Get real-time metrics
- `GET /api/metrics/history/?hours=24` - Get metrics history

### Processes
- `GET /api/processes/` - List processes
- `GET /api/processes/top_processes/?limit=10` - Get top processes
- `GET /api/processes/current/` - Get current processes

### Alerts
- `GET /api/alerts/` - List all alerts
- `GET /api/alerts/unresolved/` - Get unresolved alerts
- `GET /api/alerts/critical/` - Get critical alerts
- `POST /api/alerts/{id}/resolve/` - Resolve an alert
- `POST /api/alerts/resolve_all/` - Resolve all alerts

## Dashboard URL
- http://localhost:8000

## Admin Dashboard
- http://localhost:8000/admin

## Directory Structure
```
.
├── README.md
├── manage.py
├── requirements.txt
├── .env.example
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── celery.py
├── monitoring/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── admin.py
│   ├── apps.py
│   ├── utils.py
│   ├── tasks.py
│   ├── templates/
│   │   └── dashboard.html
│   └── static/
└── db.sqlite3
```

## Features
- ✅ Real-time CPU, Memory, and Disk monitoring
- ✅ Process tracking and resource usage
- ✅ Alert system with thresholds
- ✅ Historical data storage and analysis
- ✅ Responsive web dashboard
- ✅ REST API for integration
- ✅ Django admin interface
- ✅ Background task scheduling with Celery

## Configuration

### Thresholds (via Django Admin)
Set custom thresholds for:
- CPU usage
- Memory usage
- Disk usage
- Check interval
- Data retention period

### Environment Variables (.env)
```
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
MONITOR_INTERVAL=5
MONITOR_HISTORY_RETENTION=86400
REDIS_URL=redis://localhost:6379/0
```

## Production Deployment

### Using Gunicorn + Nginx
```bash
gunicorn -w 4 -b 0.0.0.0:8000 config.wsgi:application
```

### Using Docker (optional)
```bash
docker build -t monitoring-system .
docker run -p 8000:8000 monitoring-system
```

## Troubleshooting

### Database Issues
```bash
python manage.py flush  # Warning: Deletes all data
python manage.py migrate --run-syncdb
```

### Missing Static Files
```bash
python manage.py collectstatic --clear --noinput
```

### Celery Connection Issues
- Ensure Redis is running: `redis-cli ping`
- Check Redis connection in settings

## License
MIT License
