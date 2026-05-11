"""
URL Configuration for monitoring system.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from monitoring import views

router = DefaultRouter()
router.register(r'metrics', views.SystemMetricsViewSet, basename='metrics')
router.register(r'processes', views.ProcessInfoViewSet, basename='processes')
router.register(r'alerts', views.AlertViewSet, basename='alerts')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
]
