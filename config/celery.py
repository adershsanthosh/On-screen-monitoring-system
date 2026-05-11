"""
Celery configuration for the monitoring system
"""
import os
from celery import Celery
from celery.schedules import schedule

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('monitoring')

# Load configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all registered Django apps
app.autodiscover_tasks()

# Configure periodic tasks
from celery.schedules import crontab

app.conf.beat_schedule = {
    'collect-system-metrics': {
        'task': 'monitoring.tasks.collect_system_metrics',
        'schedule': 5.0,  # Every 5 seconds
    },
    'collect-process-info': {
        'task': 'monitoring.tasks.collect_process_info',
        'schedule': 10.0,  # Every 10 seconds
    },
    'check-thresholds': {
        'task': 'monitoring.tasks.check_thresholds',
        'schedule': 10.0,  # Every 10 seconds
    },
    'cleanup-old-data': {
        'task': 'monitoring.tasks.cleanup_old_data',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM
    },
}
