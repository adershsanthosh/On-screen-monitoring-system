from django.contrib import admin
from django.utils import timezone
from .models import SystemMetrics, ProcessInfo, Alert, MonitoringConfig


@admin.register(SystemMetrics)
class SystemMetricsAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'cpu_percent', 'memory_percent', 'disk_percent')
    list_filter = ('timestamp',)
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)


@admin.register(ProcessInfo)
class ProcessInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'pid', 'status', 'memory_mb', 'cpu_percent', 'timestamp')
    list_filter = ('status', 'timestamp')
    search_fields = ('name', 'pid')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp', '-memory_mb')


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('title', 'alert_type', 'severity', 'is_resolved', 'timestamp')
    list_filter = ('alert_type', 'severity', 'is_resolved', 'timestamp')
    search_fields = ('title', 'message')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)
    actions = ['resolve_alerts']
    
    def resolve_alerts(self, request, queryset):
        """Admin action to resolve selected alerts"""
        updated = queryset.update(is_resolved=True, resolved_at=timezone.now())
        self.message_user(request, f'{updated} alerts resolved.')
    resolve_alerts.short_description = "Mark selected alerts as resolved"


@admin.register(MonitoringConfig)
class MonitoringConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'monitoring_enabled', 'cpu_threshold', 'memory_threshold', 'disk_threshold')
    list_filter = ('monitoring_enabled',)
    fieldsets = (
        ('Configuration', {
            'fields': ('name', 'monitoring_enabled', 'check_interval', 'data_retention_days')
        }),
        ('Thresholds', {
            'fields': ('cpu_threshold', 'memory_threshold', 'disk_threshold')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
