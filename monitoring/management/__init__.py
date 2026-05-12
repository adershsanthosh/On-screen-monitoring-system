from django.core.management.base import BaseCommand
from monitoring.utils import SystemMonitor, AlertManager
from monitoring.models import SystemMetrics, ProcessInfo, MonitoringConfig
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Manually collect system metrics'

    def handle(self, *args, **options):
        self.stdout.write('Collecting system metrics...')
        
        try:
            metrics = SystemMonitor.get_all_metrics()
            saved_metric = SystemMetrics.objects.create(**metrics)
            
            self.stdout.write(
                self.style.SUCCESS(f'✓ Metrics collected: CPU {metrics["cpu_percent"]:.1f}%, '
                                 f'Memory {metrics["memory_percent"]:.1f}%, '
                                 f'Disk {metrics["disk_percent"]:.1f}%')
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error: {str(e)}'))
