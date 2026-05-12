from celery import shared_task
from .utils import SystemMonitor
from .models import SystemMetrics, ExamActivity, ExamNotification, Alert
from django.utils import timezone
from datetime import timedelta


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


@shared_task
def notify_suspicious_exam_activity():
    """
    Check for suspicious exam activities and create notifications.
    Suspicious activities include: tab_hidden, lost_focus, page_unload
    """
    # Get activities from the last 2 minutes
    cutoff_time = timezone.now() - timedelta(minutes=2)
    suspicious_events = ExamActivity.objects.filter(
        timestamp__gte=cutoff_time,
        event_type__in=['tab_hidden', 'lost_focus', 'page_unload']
    ).order_by('-timestamp')

    for activity in suspicious_events:
        # Check if notification already exists for this event
        existing_notif = ExamNotification.objects.filter(
            student_id=activity.student_id,
            exam_id=activity.exam_id,
            message__contains=activity.event_type,
            created_at__gte=cutoff_time
        ).exists()

        if not existing_notif:
            event_name = activity.get_event_type_display()
            severity = 'warning' if activity.event_type != 'page_unload' else 'critical'
            
            ExamNotification.objects.create(
                student_id=activity.student_id,
                exam_id=activity.exam_id,
                message=f'Alert: {event_name} detected during exam. Ensure you remain focused on the exam.',
                severity=severity,
                active=True
            )

    return f"Checked {suspicious_events.count()} suspicious activities"


@shared_task
def notify_system_alerts():
    """
    Create exam notifications for any unresolved system alerts.
    """
    # Get unresolved alerts from the last 5 minutes
    cutoff_time = timezone.now() - timedelta(minutes=5)
    alerts = Alert.objects.filter(
        timestamp__gte=cutoff_time,
        is_resolved=False,
        severity__in=['warning', 'critical']
    ).order_by('-timestamp')

    for alert in alerts[:5]:  # Limit to 5 most recent alerts
        # Create a notification for all active exam students
        recent_exams = ExamActivity.objects.filter(
            timestamp__gte=cutoff_time
        ).values('student_id', 'exam_id').distinct()

        for exam_ref in recent_exams:
            existing_notif = ExamNotification.objects.filter(
                student_id=exam_ref['student_id'],
                exam_id=exam_ref['exam_id'],
                message__contains=alert.title,
                created_at__gte=cutoff_time
            ).exists()

            if not existing_notif:
                ExamNotification.objects.create(
                    student_id=exam_ref['student_id'],
                    exam_id=exam_ref['exam_id'],
                    message=f'System Alert: {alert.title} - {alert.message}',
                    severity=alert.severity,
                    active=True
                )

    return f"Created notifications for {alerts.count()} alerts"


@shared_task
def cleanup_old_notifications():
    """
    Clean up old notifications (older than 7 days) from the database.
    """
    cutoff_time = timezone.now() - timedelta(days=7)
    deleted_count, _ = ExamNotification.objects.filter(
        created_at__lt=cutoff_time,
        active=False
    ).delete()
    
    return f"Deleted {deleted_count} old notifications"