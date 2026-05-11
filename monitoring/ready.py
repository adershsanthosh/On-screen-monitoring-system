# Python Django Monitoring System
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.conf import settings

@receiver(post_migrate)
def create_default_config(sender, **kwargs):
    """Create default monitoring configuration after migration"""
    from .models import MonitoringConfig
    
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

default_app_config = 'monitoring.apps.MonitoringConfig'
