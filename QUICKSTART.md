# Quick Start Guide

## 1. Installation

### Using Virtual Environment (Recommended)
```bash
# Clone repository
git clone <repo-url>
cd On-screen-monitoring-system

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
```

### Using setup.sh
```bash
chmod +x setup.sh
./setup.sh
```

## 2. Database Setup
```bash
# Run migrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser

# (Optional) Create initial monitoring configuration
python manage.py shell << END
from monitoring.models import MonitoringConfig
MonitoringConfig.objects.create(
    name='Default',
    cpu_threshold=80.0,
    memory_threshold=85.0,
    disk_threshold=90.0
)
END
```

## 3. Run the Server

### Development Server (Simple)
```bash
python manage.py runserver 0.0.0.0:8000
```

### Development Server with Celery
```bash
# Terminal 1: Main server
python manage.py runserver 0.0.0.0:8000

# Terminal 2: Celery worker (in a new terminal)
celery -A config worker -l info

# Terminal 3: Celery beat scheduler (in another new terminal)
celery -A config beat -l info
```

### Using Docker
```bash
# Build and run containers
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# View logs
docker-compose logs -f web
```

## 4. Access the Application

- **Dashboard**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **API Docs**: http://localhost:8000/api/

## 5. Key Features to Try

### View Real-time Metrics
- Visit http://localhost:8000
- Metrics auto-refresh every 5 seconds
- Charts show historical data

### Configure Monitoring
- Go to Django Admin: http://localhost:8000/admin
- Navigate to "Monitoring configs"
- Set custom thresholds for CPU, Memory, Disk

### Manage Processes
- Main dashboard shows top processes by memory
- Click on any process row for more details
- API available at `/api/processes/`

### Check Alerts
- Alerts automatically created when thresholds exceeded
- View in Dashboard alerts section
- Resolve alerts individually or in bulk
- Filter by severity level

### Use REST API
```bash
# Get current metrics
curl http://localhost:8000/api/metrics/current/

# Get top processes
curl http://localhost:8000/api/processes/top_processes/?limit=5

# Get unresolved alerts
curl http://localhost:8000/api/alerts/unresolved/

# Resolve specific alert
curl -X POST http://localhost:8000/api/alerts/1/resolve/
```

## 6. Management Commands

### Manual Metric Collection
```bash
python manage.py collect_metrics
```

### Manual Process Collection
```bash
python manage.py collect_processes --limit 50
```

### Check Thresholds
```bash
python manage.py check_thresholds
```

### Clean Up Old Data
```bash
python manage.py cleanup_data --days 30
```

## Troubleshooting

### Issue: "No module named 'monitoring'"
**Solution**: Run migrations and ensure app is in INSTALLED_APPS
```bash
python manage.py migrate
```

### Issue: Metrics not updating
**Solution**: Check if Celery is running or reload page
```bash
# For development, you can also manually run:
python manage.py collect_metrics
```

### Issue: Permission denied (processes)
**Solution**: Run with sudo or configure specific processes
```bash
sudo python manage.py runserver 0.0.0.0:8000
```

### Issue: Redis connection error
**Solution**: Install and start Redis
```bash
# macOS
brew install redis
brew services start redis

# Ubuntu
sudo apt-get install redis-server
sudo systemctl start redis-server

# Windows
# Download from: https://github.com/microsoftarchive/redis/releases
```

### Issue: Database locked (SQLite)
**Solution**: Delete db.sqlite3 and re-migrate
```bash
rm db.sqlite3
python manage.py migrate
```

## Performance Tips

1. **Use PostgreSQL in Production**
   - Better concurrency than SQLite
   - Recommended for production deployments

2. **Enable Celery**
   - Improves responsiveness
   - Enables background metric collection
   - Allows scheduled cleanup tasks

3. **Configure Data Retention**
   - Set appropriate retention days in admin
   - Prevents database from growing too large

4. **Use Gunicorn + Nginx**
   - Better performance than Django runserver
   - Handles concurrent connections better

5. **Monitor from Multiple Machines**
   - Run monitoring app on separate server
   - Use PostgreSQL for centralized data
   - Scale with load balancers

## Next Steps

- [ ] Configure custom alert thresholds
- [ ] Set up email notifications (optional)
- [ ] Deploy to production
- [ ] Set up automated backups
- [ ] Configure log rotation
- [ ] Set up SSL/HTTPS
- [ ] Configure monitoring for specific applications
- [ ] Create custom dashboards

## Support & Documentation

- **Django Docs**: https://docs.djangoproject.com/
- **DRF Docs**: https://www.django-rest-framework.org/
- **Celery Docs**: https://docs.celeryproject.org/
- **psutil Docs**: https://psutil.readthedocs.io/

## License
MIT License
