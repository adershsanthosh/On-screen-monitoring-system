import pytest
from django.test import TestCase, Client
from django.contrib.auth.models import User
from monitoring.models import SystemMetrics, Alert, MonitoringConfig
from monitoring.utils import SystemMonitor, AlertManager
from datetime import datetime


class SystemMetricsTestCase(TestCase):
    """Test cases for system metrics"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.metric_data = {
            'cpu_percent': 45.5,
            'cpu_count': 4,
            'memory_total': 8589934592,
            'memory_used': 4294967296,
            'memory_percent': 50.0,
            'disk_total': 107374182400,
            'disk_used': 53687091200,
            'disk_percent': 50.0,
            'network_bytes_sent': 1000000,
            'network_bytes_recv': 2000000,
        }
    
    def test_create_system_metrics(self):
        """Test creating system metrics"""
        metric = SystemMetrics.objects.create(**self.metric_data)
        self.assertEqual(metric.cpu_percent, 45.5)
        self.assertEqual(metric.memory_percent, 50.0)
    
    def test_metrics_api_endpoint(self):
        """Test API endpoint for metrics"""
        response = self.client.get('/api/metrics/')
        self.assertEqual(response.status_code, 200)
    
    def test_latest_metrics_endpoint(self):
        """Test latest metrics endpoint"""
        SystemMetrics.objects.create(**self.metric_data)
        response = self.client.get('/api/metrics/latest/')
        self.assertEqual(response.status_code, 200)


class AlertTestCase(TestCase):
    """Test cases for alerts"""
    
    def setUp(self):
        """Set up test data"""
        self.alert_data = {
            'alert_type': 'cpu_high',
            'severity': 'warning',
            'title': 'High CPU Usage',
            'message': 'CPU is at 95%',
            'metric_value': 95.0,
            'threshold_value': 80.0,
        }
    
    def test_create_alert(self):
        """Test creating an alert"""
        alert = Alert.objects.create(**self.alert_data)
        self.assertEqual(alert.title, 'High CPU Usage')
        self.assertFalse(alert.is_resolved)
    
    def test_resolve_alert(self):
        """Test resolving an alert"""
        alert = Alert.objects.create(**self.alert_data)
        alert.resolve()
        self.assertTrue(alert.is_resolved)
        self.assertIsNotNone(alert.resolved_at)


class SystemMonitorTestCase(TestCase):
    """Test cases for system monitoring utilities"""
    
    def test_get_cpu_metrics(self):
        """Test getting CPU metrics"""
        metrics = SystemMonitor.get_cpu_metrics()
        self.assertIn('cpu_percent', metrics)
        self.assertIn('cpu_count', metrics)
        self.assertGreaterEqual(metrics['cpu_percent'], 0)
    
    def test_get_memory_metrics(self):
        """Test getting memory metrics"""
        metrics = SystemMonitor.get_memory_metrics()
        self.assertIn('memory_total', metrics)
        self.assertIn('memory_used', metrics)
        self.assertIn('memory_percent', metrics)
    
    def test_get_all_metrics(self):
        """Test getting all metrics"""
        metrics = SystemMonitor.get_all_metrics()
        self.assertIn('cpu_percent', metrics)
        self.assertIn('memory_percent', metrics)
        self.assertIn('disk_percent', metrics)


class MonitoringConfigTestCase(TestCase):
    """Test cases for monitoring configuration"""
    
    def test_create_config(self):
        """Test creating monitoring configuration"""
        config = MonitoringConfig.objects.create(
            name='Test Config',
            cpu_threshold=80.0,
            memory_threshold=85.0,
            disk_threshold=90.0,
        )
        self.assertEqual(config.cpu_threshold, 80.0)
        self.assertTrue(config.monitoring_enabled)
    
    def test_config_defaults(self):
        """Test default configuration values"""
        config = MonitoringConfig.objects.create(name='Default')
        self.assertEqual(config.cpu_threshold, 80.0)
        self.assertEqual(config.memory_threshold, 85.0)
        self.assertEqual(config.disk_threshold, 90.0)
        self.assertEqual(config.check_interval, 5)
        self.assertEqual(config.data_retention_days, 30)
