from django.db import models
from django.utils import timezone


class SystemMetrics(models.Model):
    """Store system-wide metrics (CPU, Memory, Disk)"""
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    # CPU metrics
    cpu_percent = models.FloatField(help_text="CPU usage percentage")
    cpu_count = models.IntegerField(help_text="Number of CPU cores")
    
    # Memory metrics
    memory_total = models.BigIntegerField(help_text="Total memory in bytes")
    memory_used = models.BigIntegerField(help_text="Used memory in bytes")
    memory_percent = models.FloatField(help_text="Memory usage percentage")
    
    # Disk metrics
    disk_total = models.BigIntegerField(help_text="Total disk space in bytes")
    disk_used = models.BigIntegerField(help_text="Used disk space in bytes")
    disk_percent = models.FloatField(help_text="Disk usage percentage")
    
    # Network metrics
    network_bytes_sent = models.BigIntegerField(default=0)
    network_bytes_recv = models.BigIntegerField(default=0)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
        ]
    
    def __str__(self):
        return f"System Metrics - {self.timestamp}"


class ProcessInfo(models.Model):
    """Store process information"""
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    pid = models.IntegerField(help_text="Process ID")
    name = models.CharField(max_length=255, help_text="Process name")
    status = models.CharField(max_length=50, help_text="Process status")
    
    # Resource usage
    cpu_percent = models.FloatField(help_text="CPU usage percentage")
    memory_mb = models.FloatField(help_text="Memory usage in MB")
    num_threads = models.IntegerField(help_text="Number of threads")
    
    # Process info
    username = models.CharField(max_length=255, blank=True)
    create_time = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-timestamp', '-memory_mb']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['pid']),
        ]
    
    def __str__(self):
        return f"{self.name} (PID: {self.pid})"


class Alert(models.Model):
    """Store system alerts and anomalies"""
    ALERT_TYPES = [
        ('cpu_high', 'High CPU Usage'),
        ('memory_high', 'High Memory Usage'),
        ('disk_high', 'High Disk Usage'),
        ('process_crash', 'Process Crash'),
        ('network_issue', 'Network Issue'),
        ('custom', 'Custom Alert'),
    ]
    
    SEVERITY_LEVELS = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
    ]
    
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    alert_type = models.CharField(max_length=50, choices=ALERT_TYPES)
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS, default='warning')
    
    title = models.CharField(max_length=255)
    message = models.TextField()
    
    # Reference data
    metric_value = models.FloatField(null=True, blank=True)
    threshold_value = models.FloatField(null=True, blank=True)
    
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['is_resolved']),
        ]
    
    def __str__(self):
        return f"{self.get_alert_type_display()} - {self.title}"
    
    def resolve(self):
        """Mark alert as resolved"""
        self.is_resolved = True
        self.resolved_at = timezone.now()
        self.save()


class ExamActivity(models.Model):
    """Store student exam activity events"""
    EVENT_CHOICES = [
        ('tab_hidden', 'Tab Hidden'),
        ('tab_visible', 'Tab Visible'),
        ('lost_focus', 'Window Lost Focus'),
        ('gained_focus', 'Window Gained Focus'),
        ('idle', 'Idle'),
        ('active', 'Active'),
        ('page_unload', 'Page Unload'),
        ('exam_loaded', 'Exam Loaded'),
    ]

    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    student_id = models.CharField(max_length=255, default='unknown', help_text='Student identifier')
    exam_id = models.CharField(max_length=255, default='exam1', help_text='Exam identifier')
    event_type = models.CharField(max_length=50, choices=EVENT_CHOICES)
    details = models.TextField(blank=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['student_id']),
            models.Index(fields=['exam_id']),
        ]

    def __str__(self):
        return f"ExamActivity({self.student_id}, {self.event_type}, {self.timestamp})"


class ExamNotification(models.Model):
    """Store notifications that should appear on the student exam screen"""
    SEVERITY_LEVELS = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    student_id = models.CharField(max_length=255, blank=True, help_text='Optional student identifier')
    exam_id = models.CharField(max_length=255, blank=True, help_text='Optional exam identifier')
    message = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS, default='info')
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['active']),
            models.Index(fields=['student_id']),
            models.Index(fields=['exam_id']),
        ]

    def __str__(self):
        return f"{self.get_severity_display()} notification: {self.message[:50]}"


class MonitoringConfig(models.Model):
    """Store monitoring configuration and thresholds"""
    name = models.CharField(max_length=255, unique=True)
    
    # Thresholds
    cpu_threshold = models.FloatField(default=80.0, help_text="CPU usage threshold %")
    memory_threshold = models.FloatField(default=85.0, help_text="Memory usage threshold %")
    disk_threshold = models.FloatField(default=90.0, help_text="Disk usage threshold %")
    
    # Monitoring settings
    monitoring_enabled = models.BooleanField(default=True)
    check_interval = models.IntegerField(default=5, help_text="Check interval in seconds")
    data_retention_days = models.IntegerField(default=30, help_text="Days to retain historical data")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Monitoring Configs"
    
    def __str__(self):
        return self.name