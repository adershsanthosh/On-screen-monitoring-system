from rest_framework import serializers
from .models import SystemMetrics, ProcessInfo, Alert, MonitoringConfig


class SystemMetricsSerializer(serializers.ModelSerializer):
    """Serializer for SystemMetrics model"""
    
    class Meta:
        model = SystemMetrics
        fields = [
            'id', 'timestamp', 'cpu_percent', 'cpu_count',
            'memory_total', 'memory_used', 'memory_percent',
            'disk_total', 'disk_used', 'disk_percent',
            'network_bytes_sent', 'network_bytes_recv'
        ]
        read_only_fields = ['id', 'timestamp']


class ProcessInfoSerializer(serializers.ModelSerializer):
    """Serializer for ProcessInfo model"""
    
    class Meta:
        model = ProcessInfo
        fields = [
            'id', 'timestamp', 'pid', 'name', 'status',
            'cpu_percent', 'memory_mb', 'num_threads',
            'username', 'create_time'
        ]
        read_only_fields = ['id', 'timestamp']


class AlertSerializer(serializers.ModelSerializer):
    """Serializer for Alert model"""
    alert_type_display = serializers.CharField(source='get_alert_type_display', read_only=True)
    severity_display = serializers.CharField(source='get_severity_display', read_only=True)
    
    class Meta:
        model = Alert
        fields = [
            'id', 'timestamp', 'alert_type', 'alert_type_display',
            'severity', 'severity_display', 'title', 'message',
            'metric_value', 'threshold_value', 'is_resolved', 'resolved_at'
        ]
        read_only_fields = ['id', 'timestamp']


class MonitoringConfigSerializer(serializers.ModelSerializer):
    """Serializer for MonitoringConfig model"""
    
    class Meta:
        model = MonitoringConfig
        fields = [
            'id', 'name', 'cpu_threshold', 'memory_threshold',
            'disk_threshold', 'monitoring_enabled', 'check_interval',
            'data_retention_days', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
