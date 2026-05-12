from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.urls import path
from django.utils import timezone
from .models import SystemMetrics, ProcessInfo, Alert, MonitoringConfig, ExamActivity, ExamNotification


def live_feed_view(request):
    return render(request, 'admin/live_feed.html')


admin.site.index_template = 'admin/custom_index.html'


@admin.register(SystemMetrics)
class SystemMetricsAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'cpu_percent', 'memory_percent', 'disk_percent')
    list_filter = ('timestamp',)
    readonly_fields = ('timestamp',)


@admin.register(ProcessInfo)
class ProcessInfoAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'pid', 'name', 'cpu_percent', 'memory_mb')
    list_filter = ('timestamp', 'name')
    readonly_fields = ('timestamp',)


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'alert_type', 'severity', 'title', 'is_resolved')
    list_filter = ('alert_type', 'severity', 'is_resolved', 'timestamp')
    readonly_fields = ('timestamp',)


@admin.register(MonitoringConfig)
class MonitoringConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'cpu_threshold', 'memory_threshold', 'disk_threshold', 'monitoring_enabled')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ExamActivity)
class ExamActivityAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'student_id', 'exam_id', 'event_type', 'details')
    list_filter = ('event_type', 'student_id', 'exam_id', 'timestamp')
    search_fields = ('student_id', 'exam_id', 'event_type', 'details')
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)


@admin.register(ExamNotification)
class ExamNotificationAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'student_id', 'exam_id', 'severity', 'active')
    list_filter = ('severity', 'active', 'student_id', 'exam_id')
    search_fields = ('student_id', 'exam_id', 'message')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)