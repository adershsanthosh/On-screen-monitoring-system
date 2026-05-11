from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from datetime import timedelta

from .models import SystemMetrics, ProcessInfo, Alert, MonitoringConfig
from .serializers import (
    SystemMetricsSerializer, ProcessInfoSerializer,
    AlertSerializer, MonitoringConfigSerializer
)
from .utils import SystemMonitor, AlertManager


class SystemMetricsViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for system metrics"""
    queryset = SystemMetrics.objects.all()
    serializer_class = SystemMetricsSerializer
    permission_classes = [AllowAny]  # Can be changed to [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Get latest system metrics"""
        latest_metric = SystemMetrics.objects.first()
        if latest_metric:
            serializer = self.get_serializer(latest_metric)
            return Response(serializer.data)
        return Response({'detail': 'No metrics available'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current system metrics (real-time scan)"""
        metrics = SystemMonitor.get_all_metrics()
        return Response(metrics)
    
    @action(detail=False, methods=['get'])
    def history(self, request):
        """Get metrics history (last hours specified in query parameter)"""
        hours = int(request.query_params.get('hours', 24))
        cutoff_time = timezone.now() - timedelta(hours=hours)
        
        metrics = SystemMetrics.objects.filter(timestamp__gte=cutoff_time)
        serializer = self.get_serializer(metrics, many=True)
        return Response(serializer.data)


class ProcessInfoViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for process information"""
    queryset = ProcessInfo.objects.all()
    serializer_class = ProcessInfoSerializer
    permission_classes = [AllowAny]  # Can be changed to [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def top_processes(self, request):
        """Get top processes by memory usage"""
        limit = int(request.query_params.get('limit', 10))
        processes = SystemMonitor.get_top_processes(limit)
        return Response(processes)
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current list of processes"""
        limit = int(request.query_params.get('limit', 50))
        processes = SystemMonitor.get_top_processes(limit * 2)
        return Response(processes)
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Get latest process snapshots"""
        latest_processes = ProcessInfo.objects.filter(
            timestamp=ProcessInfo.objects.latest('timestamp').timestamp
        )
        serializer = self.get_serializer(latest_processes, many=True)
        return Response(serializer.data)


class AlertViewSet(viewsets.ModelViewSet):
    """API endpoint for alerts"""
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [AllowAny]  # Can be changed to [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Mark an alert as resolved"""
        alert = self.get_object()
        alert.resolve()
        serializer = self.get_serializer(alert)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def unresolved(self, request):
        """Get all unresolved alerts"""
        unresolved = Alert.objects.filter(is_resolved=False)
        serializer = self.get_serializer(unresolved, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def critical(self, request):
        """Get critical alerts"""
        critical_alerts = Alert.objects.filter(
            severity='critical',
            is_resolved=False
        )
        serializer = self.get_serializer(critical_alerts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def resolve_all(self, request):
        """Resolve all unresolved alerts"""
        unresolved = Alert.objects.filter(is_resolved=False)
        count = unresolved.update(is_resolved=True, resolved_at=timezone.now())
        return Response({'resolved_count': count})


class MonitoringConfigViewSet(viewsets.ModelViewSet):
    """API endpoint for monitoring configuration"""
    queryset = MonitoringConfig.objects.all()
    serializer_class = MonitoringConfigSerializer
    permission_classes = [IsAuthenticated]
