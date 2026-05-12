import psutil
import platform
from datetime import datetime
from django.utils import timezone


class SystemMonitor:
    """Monitor system resources"""
    
    @staticmethod
    def get_cpu_info():
        """Get CPU information"""
        return {
            'percent': psutil.cpu_percent(interval=1),
            'count': psutil.cpu_count(),
            'count_logical': psutil.cpu_count(logical=True),
        }
    
    @staticmethod
    def get_memory_info():
        """Get memory information"""
        mem = psutil.virtual_memory()
        return {
            'total': mem.total,
            'available': mem.available,
            'percent': mem.percent,
            'used': mem.used,
        }
    
    @staticmethod
    def get_disk_info():
        """Get disk information"""
        disk = psutil.disk_usage('/')
        return {
            'total': disk.total,
            'used': disk.used,
            'free': disk.free,
            'percent': disk.percent,
        }
    
    @staticmethod
    def get_all_metrics():
        """Get all system metrics"""
        return {
            'cpu': SystemMonitor.get_cpu_info(),
            'memory': SystemMonitor.get_memory_info(),
            'disk': SystemMonitor.get_disk_info(),
            'timestamp': timezone.now().isoformat(),
        }


class AlertManager:
    """Manage system alerts"""
    
    @staticmethod
    def check_thresholds(metrics):
        """Check if metrics exceed thresholds"""
        alerts = []
        
        if metrics['cpu']['percent'] > 90:
            alerts.append({
                'type': 'cpu',
                'message': f'CPU usage is {metrics["cpu"]["percent"]:.1f}%',
                'severity': 'high'
            })
        
        if metrics['memory']['percent'] > 90:
            alerts.append({
                'type': 'memory',
                'message': f'Memory usage is {metrics["memory"]["percent"]:.1f}%',
                'severity': 'high'
            })
        
        if metrics['disk']['percent'] > 90:
            alerts.append({
                'type': 'disk',
                'message': f'Disk usage is {metrics["disk"]["percent"]:.1f}%',
                'severity': 'high'
            })
        
    @staticmethod
    def get_top_processes(limit=10):
        """Get top processes by memory usage"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_info', 'num_threads', 'username', 'create_time']):
            try:
                mem_mb = proc.info['memory_info'].rss / 1024 / 1024 if proc.info['memory_info'] else 0
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'status': proc.info['status'],
                    'cpu_percent': proc.info['cpu_percent'] or 0,
                    'memory_mb': mem_mb,
                    'num_threads': proc.info['num_threads'] or 0,
                    'username': proc.info['username'] or '',
                    'create_time': proc.info['create_time'],
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Sort by memory usage descending
        processes.sort(key=lambda x: x['memory_mb'], reverse=True)
        return processes[:limit]