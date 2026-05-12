from django.core.management.base import BaseCommand
from monitoring.models import MonitoringConfig, Alert
from monitoring.utils import SystemMonitor, AlertManager
from django.utils import timezone


class Command(BaseCommand):
    help = 'Check system metrics against thresholds and create alerts'

    def handle(self, *args, **options):
        self.stdout.write('Checking thresholds...')
        
        try:
            config = MonitoringConfig.objects.first()
            if not config or not config.monitoring_enabled:
                self.stdout.write(self.style.WARNING('⚠ Monitoring disabled'))
                return
            
            metrics = SystemMonitor.get_all_metrics()
            alerts = AlertManager.check_thresholds(metrics, config)
            
            if alerts:
                created_alerts = AlertManager.create_alerts(alerts)
                self.stdout.write(
                    self.style.WARNING(f'⚠ Created {len(created_alerts)} alerts')
                )
                for alert in created_alerts:
                    self.stdout.write(f'  - {alert.title}: {alert.message}')
            else:
                self.stdout.write(
                    self.style.SUCCESS('✓ All metrics within thresholds')
                )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error: {str(e)}'))
