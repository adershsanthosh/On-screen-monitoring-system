from django.core.management.base import BaseCommand
from monitoring.utils import AlertManager
from monitoring.models import MonitoringConfig


class Command(BaseCommand):
    help = 'Clean up old monitoring data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=None,
            help='Days of data to keep (default: from MonitoringConfig)'
        )

    def handle(self, *args, **options):
        days = options['days']
        
        if days is None:
            config = MonitoringConfig.objects.first()
            days = config.data_retention_days if config else 30
        
        self.stdout.write(f'Cleaning up data older than {days} days...')
        
        try:
            metrics_deleted, processes_deleted = AlertManager.cleanup_old_data(days)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Deleted {metrics_deleted} metric records and {processes_deleted} process records'
                )
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error: {str(e)}'))
