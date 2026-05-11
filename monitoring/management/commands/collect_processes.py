from django.core.management.base import BaseCommand
from monitoring.utils import SystemMonitor
from monitoring.models import SystemMetrics, ProcessInfo


class Command(BaseCommand):
    help = 'Manually collect process information'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=50,
            help='Number of processes to collect'
        )

    def handle(self, *args, **options):
        limit = options['limit']
        self.stdout.write(f'Collecting process information (limit: {limit})...')
        
        try:
            processes = SystemMonitor.get_top_processes(limit)
            for proc in processes:
                ProcessInfo.objects.create(**proc)
            
            self.stdout.write(
                self.style.SUCCESS(f'✓ Collected information for {len(processes)} processes')
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error: {str(e)}'))
