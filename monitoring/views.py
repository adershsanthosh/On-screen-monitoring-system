from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta

from .models import SystemMetrics, ProcessInfo, Alert, MonitoringConfig, ExamActivity, ExamNotification
from .serializers import (
    SystemMetricsSerializer, ProcessInfoSerializer,
    AlertSerializer, MonitoringConfigSerializer,
    ExamActivitySerializer, ExamNotificationSerializer
)
from .utils import SystemMonitor, AlertManager


def dashboard_page(request):
    return render(request, 'dashboard.html')


def exam_page(request):
    message = None
    enrolled = False
    student_id = request.session.get('student_id', '')
    exam_id = request.session.get('exam_id', 'exam1')

    if request.method == 'POST':
        student_id = request.POST.get('student_id', '').strip()
        exam_id = request.POST.get('exam_id', '').strip() or 'exam1'
        password = request.POST.get('password', '').strip()

        if student_id and exam_id:
            ExamActivity.objects.create(
                student_id=student_id,
                exam_id=exam_id,
                event_type='exam_loaded',
                details='Student enrolled and exam session initialized.'
            )
            
            # Create enrollment notification
            ExamNotification.objects.create(
                student_id=student_id,
                exam_id=exam_id,
                message=f'Welcome {student_id}! You have been enrolled for exam {exam_id}. Your activity is being monitored.',
                severity='info',
                active=True
            )
            
            request.session['student_id'] = student_id
            request.session['exam_id'] = exam_id
            enrolled = True
            message = f'Welcome {student_id}! You are enrolled for exam {exam_id}.'
        else:
            message = 'Please enter both student ID and exam ID to enroll.'
    elif student_id and exam_id:
        enrolled = True
        message = f'You are currently enrolled as {student_id} for exam {exam_id}.'

    return render(request, 'exam.html', {
        'student_id': student_id,
        'exam_id': exam_id,
        'enrolled': enrolled,
        'message': message,
    })


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
        processes = AlertManager.get_top_processes(limit)
        return Response(processes)
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current list of processes"""
        limit = int(request.query_params.get('limit', 50))
        processes = AlertManager.get_top_processes(limit * 2)
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


@method_decorator(csrf_exempt, name='dispatch')
class ExamActivityViewSet(viewsets.ModelViewSet):
    """API endpoint for exam activity events"""
    queryset = ExamActivity.objects.all().order_by('-timestamp')
    serializer_class = ExamActivitySerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def report(self, request):
        """Report a student exam event"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        activity = serializer.save()

        if activity.event_type in ['tab_hidden', 'lost_focus', 'idle', 'page_unload']:
            Alert.objects.create(
                alert_type='custom',
                severity='warning',
                title=f'Exam event: {activity.event_type.replace("_", " ").title()}',
                message=(
                    f'Student {activity.student_id} triggered {activity.event_type} '
                    f'during exam {activity.exam_id}. {activity.details}'
                )
            )

        response_serializer = self.get_serializer(activity)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent exam activity events"""
        activities = self.get_queryset()[:20]
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)


@method_decorator(csrf_exempt, name='dispatch')
class ExamNotificationViewSet(viewsets.ModelViewSet):
    """API endpoint for student exam notifications"""
    queryset = ExamNotification.objects.filter(active=True).order_by('-created_at')
    serializer_class = ExamNotificationSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = ExamNotification.objects.filter(active=True).order_by('-created_at')
        student_id = self.request.query_params.get('student_id')
        exam_id = self.request.query_params.get('exam_id')
        if student_id:
            queryset = queryset.filter(student_id__iexact=student_id)
        if exam_id:
            queryset = queryset.filter(exam_id__iexact=exam_id)
        return queryset

    @method_decorator(csrf_exempt)
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active notifications for the student exam screen"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MonitoringConfigViewSet(viewsets.ModelViewSet):
    """API endpoint for monitoring configuration"""
    queryset = MonitoringConfig.objects.all()
    serializer_class = MonitoringConfigSerializer
    permission_classes = [IsAuthenticated]