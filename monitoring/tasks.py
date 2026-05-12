from celery import shared_task
from .utils import SystemMonitor
from .models import SystemMetrics


@shared_task
def collect_system_metrics():
    """Collect and store system metrics"""
    metrics = SystemMonitor.get_all_metrics()
    
    # Create SystemMetrics object
    SystemMetrics.objects.create(
        cpu_percent=metrics['cpu']['percent'],
        memory_percent=metrics['memory']['percent'],
        disk_percent=metrics['disk']['percent'],
    )
    
    return metrics