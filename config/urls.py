"""
URL Configuration for monitoring system.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from monitoring import views
from monitoring.admin import live_feed_view

router = DefaultRouter()
router.register(r'metrics', views.SystemMetricsViewSet, basename='metrics')
router.register(r'processes', views.ProcessInfoViewSet, basename='processes')
router.register(r'alerts', views.AlertViewSet, basename='alerts')
router.register(r'exam-activity', views.ExamActivityViewSet, basename='exam-activity')
router.register(r'exam-notifications', views.ExamNotificationViewSet, basename='exam-notifications')

urlpatterns = [
    path('admin/live-feed/', admin.site.admin_view(live_feed_view), name='live-feed'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('exam/', views.exam_page, name='exam'),
    path('', views.dashboard_page, name='dashboard'),
]
