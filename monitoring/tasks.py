# Celery tasks for periodic monitoring
from celery import shared_task
from django.utils import timezone
from .models import SystemMetrics, ProcessInfo, MonitoringConfig, Alert
from .utils import SystemMonitor, AlertManager
import logging

logger = logging.getLogger(__name__)


@shared_task
def collect_system_metrics():
    """Collect system metrics periodically"""
    try:
        metrics = SystemMonitor.get_all_metrics()
        SystemMetrics.objects.create(**metrics)
        logger.info("System metrics collected successfully")
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error collecting system metrics: {str(e)}")
        return {"status": "error", "message": str(e)}


@shared_task
def collect_process_info():
    """Collect process information periodically"""
    try:
        processes = SystemMonitor.get_top_processes(limit=50)
        for proc in processes:
            ProcessInfo.objects.create(**proc)
        logger.info(f"Collected info for {len(processes)} processes")
        return {"status": "success", "count": len(processes)}
    except Exception as e:
        logger.error(f"Error collecting process info: {str(e)}")
        return {"status": "error", "message": str(e)}


@shared_task
def check_thresholds():
    """Check if metrics exceed thresholds and create alerts"""
    try:
        config = MonitoringConfig.objects.first()
        if not config or not config.monitoring_enabled:
            return {"status": "skipped", "reason": "monitoring disabled"}
        
        metrics = SystemMonitor.get_all_metrics()
        alerts = AlertManager.check_thresholds(metrics, config)
        
        if alerts:
            created_alerts = AlertManager.create_alerts(alerts)
            logger.warning(f"Created {len(created_alerts)} alerts")
            return {"status": "success", "alerts_created": len(created_alerts)}
        
        return {"status": "success", "alerts_created": 0}
    except Exception as e:
        logger.error(f"Error checking thresholds: {str(e)}")
        return {"status": "error", "message": str(e)}


@shared_task
def cleanup_old_data():
    """Clean up old monitoring data"""
    try:
        config = MonitoringConfig.objects.first()
        days_to_keep = config.data_retention_days if config else 30
        
        metrics_deleted, processes_deleted = AlertManager.cleanup_old_data(days_to_keep)
        logger.info(f"Deleted {metrics_deleted} metrics and {processes_deleted} process records")
        
        return {
            "status": "success",
            "metrics_deleted": metrics_deleted,
            "processes_deleted": processes_deleted
        }
    except Exception as e:
        logger.error(f"Error cleaning up old data: {str(e)}")
        return {"status": "error", "message": str(e)}
