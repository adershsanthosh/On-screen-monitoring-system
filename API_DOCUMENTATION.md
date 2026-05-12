"""
API Documentation for System Monitoring Dashboard

This document provides comprehensive API documentation for all endpoints.

## Authentication
Most endpoints require authentication. Use session auth or token auth.

## Pagination
Responses are paginated with 100 items per page by default.

## Response Format
All responses are in JSON format.
"""

# SYSTEM METRICS ENDPOINTS

"""
GET /api/metrics/
List all system metrics with pagination
Query Parameters:
  - page: int (default: 1)
  - ordering: string (default: '-timestamp')

Response:
{
  "count": 1234,
  "next": "http://...?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "timestamp": "2024-05-11T10:30:45Z",
      "cpu_percent": 45.5,
      "cpu_count": 4,
      "memory_total": 8589934592,
      "memory_used": 4294967296,
      "memory_percent": 50.0,
      "disk_total": 107374182400,
      "disk_used": 53687091200,
      "disk_percent": 50.0,
      "network_bytes_sent": 1000000,
      "network_bytes_recv": 2000000
    }
  ]
}
"""

"""
GET /api/metrics/latest/
Get the most recent system metrics
Response: Single metric object
"""

"""
GET /api/metrics/current/
Get real-time system metrics (no database lookup)
Response: Current metrics snapshot
{
  "cpu_percent": 44.2,
  "cpu_count": 4,
  "memory_total": 8589934592,
  "memory_used": 4000000000,
  "memory_percent": 46.6,
  "disk_total": 107374182400,
  "disk_used": 60000000000,
  "disk_percent": 55.8,
  "network_bytes_sent": 1050000,
  "network_bytes_recv": 2100000
}
"""

"""
GET /api/metrics/history/?hours=24
Get metrics history for specified hours
Query Parameters:
  - hours: int (default: 24)

Response: Array of metric objects ordered by timestamp
"""


# PROCESS ENDPOINTS

"""
GET /api/processes/
List all recorded processes with pagination

Response: Paginated list of process records
"""

"""
GET /api/processes/top_processes/?limit=10
Get current top processes by memory usage
Query Parameters:
  - limit: int (default: 10)

Response: Array of process objects
[
  {
    "pid": 1234,
    "name": "python",
    "status": "running",
    "cpu_percent": 15.5,
    "memory_mb": 256.3,
    "num_threads": 8,
    "username": "user",
    "create_time": "2024-05-11T08:00:00Z"
  }
]
"""

"""
GET /api/processes/current/?limit=50
Get current process list
Query Parameters:
  - limit: int (default: 50)

Response: Array of process objects
"""

"""
GET /api/processes/latest/
Get latest recorded process snapshots

Response: Array of process objects from latest timestamp
"""


# ALERTS ENDPOINTS

"""
GET /api/alerts/
List all alerts with pagination

Response: Paginated list of alert objects
"""

"""
GET /api/alerts/unresolved/
Get all unresolved alerts

Response:
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "timestamp": "2024-05-11T10:30:45Z",
      "alert_type": "cpu_high",
      "alert_type_display": "High CPU Usage",
      "severity": "warning",
      "severity_display": "Warning",
      "title": "High CPU Usage",
      "message": "CPU usage is at 92.5%",
      "metric_value": 92.5,
      "threshold_value": 80.0,
      "is_resolved": false,
      "resolved_at": null
    }
  ]
}
"""

"""
GET /api/alerts/critical/
Get critical unresolved alerts

Response: Array of critical alert objects
"""

"""
GET /api/alerts/{id}/
Get specific alert details

Response: Single alert object
"""

"""
POST /api/alerts/{id}/resolve/
Mark an alert as resolved

Request: Empty body
Response: Updated alert object with is_resolved=true
"""

"""
POST /api/alerts/resolve_all/
Resolve all unresolved alerts

Request: Empty body
Response:
{
  "resolved_count": 5
}
"""

"""
POST /api/alerts/
Create a new custom alert (Requires Authentication)

Request:
{
  "alert_type": "custom",
  "severity": "warning",
  "title": "Custom Alert",
  "message": "This is a custom alert",
  "metric_value": 75.0,
  "threshold_value": 80.0
}

Response: Created alert object
"""


# MONITORING CONFIG ENDPOINTS

"""
GET /api/monitoring-config/
List all monitoring configurations (Requires Authentication)

Response: Array of config objects
"""

"""
GET /api/monitoring-config/{id}/
Get specific monitoring configuration (Requires Authentication)

Response: Single config object
"""

"""
PUT /api/monitoring-config/{id}/
Update monitoring configuration (Requires Authentication)

Request:
{
  "name": "Default",
  "cpu_threshold": 80.0,
  "memory_threshold": 85.0,
  "disk_threshold": 90.0,
  "monitoring_enabled": true,
  "check_interval": 5,
  "data_retention_days": 30
}

Response: Updated config object
"""


# ERROR RESPONSES

"""
400 Bad Request
{
  "detail": "Invalid parameters",
  "code": "invalid_request"
}

401 Unauthorized
{
  "detail": "Authentication credentials were not provided."
}

403 Forbidden
{
  "detail": "You do not have permission to perform this action."
}

404 Not Found
{
  "detail": "Not found."
}

500 Server Error
{
  "detail": "Internal server error"
}
"""

# EXAMPLE CURL REQUESTS

"""
# Get current metrics
curl http://localhost:8000/api/metrics/current/

# Get metrics from last hour
curl 'http://localhost:8000/api/metrics/history/?hours=1'

# Get top 5 processes
curl 'http://localhost:8000/api/processes/top_processes/?limit=5'

# Get all unresolved alerts
curl http://localhost:8000/api/alerts/unresolved/

# Resolve an alert
curl -X POST http://localhost:8000/api/alerts/1/resolve/

# Resolve all alerts
curl -X POST http://localhost:8000/api/alerts/resolve_all/

# Get dashboard
curl http://localhost:8000/

# Access admin panel
curl http://localhost:8000/admin/
"""
