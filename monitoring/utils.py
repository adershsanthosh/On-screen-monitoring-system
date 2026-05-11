import psutil
from datetime import datetime, timedelta
from django.utils import timezone


class SystemMonitor:
    """Utility class for collecting system metrics"""
    
    @staticmethod
    def get_cpu_metrics():
        """Get CPU metrics"""
        return {
            'cpu_percent': psutil.cpu_percent(interval=0.1),
            'cpu_count': psutil.cpu_count(logical=False),
        }
    
    @staticmethod
    def get_memory_metrics():
        """Get memory metrics"""
        mem = psutil.virtual_memory()
        return {
            'memory_total': mem.total,
            'memory_used': mem.used,
            'memory_percent': mem.percent,
        }
    
    @staticmethod
    def get_disk_metrics(path='/'):
        """Get disk metrics for specified path"""
        disk = psutil.disk_usage(path)
        return {
            'disk_total': disk.total,
            'disk_used': disk.used,
            'disk_percent': disk.percent,
        }
    
    @staticmethod
    def get_network_metrics():
        """Get network metrics"""
        net = psutil.net_io_counters()
        return {
            'network_bytes_sent': net.bytes_sent,
            'network_bytes_recv': net.bytes_recv,
        }
    
    @staticmethod
    def get_all_metrics():
        """Get all system metrics"""
        metrics = {}
        metrics.update(SystemMonitor.get_cpu_metrics())
        metrics.update(SystemMonitor.get_memory_metrics())
        metrics.update(SystemMonitor.get_disk_metrics())
        metrics.update(SystemMonitor.get_network_metrics())
        return metrics
    
    @staticmethod
    def get_top_processes(limit=10):
        """Get top processes by memory usage"""
        processes = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'status', 'memory_percent', 'cpu_percent']):
                try:
                    pinfo = proc.as_dict(attrs=['pid', 'name', 'status'])
                    pinfo['cpu_percent'] = proc.cpu_percent(interval=0.1)
                    pinfo['memory_mb'] = proc.memory_info().rss / (1024 * 1024)
                    pinfo['num_threads'] = proc.num_threads()
                    pinfo['username'] = proc.username()
                    pinfo['create_time'] = datetime.fromtimestamp(proc.create_time())
                    processes.append(pinfo)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        except psutil.AccessDenied:
            pass
        
        # Sort by memory and get top
        processes.sort(key=lambda x: x['memory_mb'], reverse=True)
        return processes[:limit]


class AlertManager:
    """Utility class for managing alerts"""
    
    @staticmethod
    def check_thresholds(metrics, config):
        """Check if metrics exceed thresholds and return alerts"""
        from .models import Alert
        
        alerts = []
        
        # CPU threshold check
        if metrics['cpu_percent'] > config.cpu_threshold:
            alert = Alert(
                alert_type='cpu_high',
                severity='warning' if metrics['cpu_percent'] < 95 else 'critical',
                title=f'High CPU Usage',
                message=f'CPU usage is at {metrics["cpu_percent"]:.1f}%',
                metric_value=metrics['cpu_percent'],
                threshold_value=config.cpu_threshold,
            )
            alerts.append(alert)
        
        # Memory threshold check
        if metrics['memory_percent'] > config.memory_threshold:
            alert = Alert(
                alert_type='memory_high',
                severity='warning' if metrics['memory_percent'] < 95 else 'critical',
                title=f'High Memory Usage',
                message=f'Memory usage is at {metrics["memory_percent"]:.1f}%',
                metric_value=metrics['memory_percent'],
                threshold_value=config.memory_threshold,
            )
            alerts.append(alert)
        
        # Disk threshold check
        if metrics['disk_percent'] > config.disk_threshold:
            alert = Alert(
                alert_type='disk_high',
                severity='warning' if metrics['disk_percent'] < 95 else 'critical',
                title=f'High Disk Usage',
                message=f'Disk usage is at {metrics["disk_percent"]:.1f}%',
                metric_value=metrics['disk_percent'],
                threshold_value=config.disk_threshold,
            )
            alerts.append(alert)
        
        return alerts
    
    @staticmethod
    def create_alerts(alerts):
        """Create new alerts in database"""
        from .models import Alert
        
        created = []
        for alert in alerts:
            new_alert = Alert.objects.create(**alert.__dict__)
            created.append(new_alert)
        
        return created
    
    @staticmethod
    def cleanup_old_data(days_to_keep=30):
        """Delete old monitoring data"""
        from .models import SystemMetrics, ProcessInfo
        
        cutoff_date = timezone.now() - timedelta(days=days_to_keep)
        metrics_deleted, _ = SystemMetrics.objects.filter(timestamp__lt=cutoff_date).delete()
        processes_deleted, _ = ProcessInfo.objects.filter(timestamp__lt=cutoff_date).delete()
        
        return metrics_deleted, processes_deleted
