# Exam Notifications System Guide

## Overview

The On-Screen Monitoring System includes a comprehensive notification system that:

- **Automatically notifies students** when they enroll for an exam
- **Monitors suspicious activities** during exams (tab hidden, lost focus, etc.)
- **Sends system notifications** from your browser (if permitted)
- **Displays in-app notifications** on the exam page
- **Creates alerts for threshold violations** and system issues

## Features

### 1. Enrollment Notifications

When a student successfully enrolls for an exam, they receive:

- A welcome notification on the exam page
- System browser notification (if permissions granted)
- The notification indicates that their activity will be monitored

### 2. Activity Monitoring Notifications

The system automatically sends notifications when:

- **Tab is hidden or minimized** → Warning notification
- **Window loses focus** → Warning notification
- **Page is unloaded or refreshed** → Critical notification
- **System alerts occur** → Warning or Critical notification

### 3. Notification Types

#### Information (Info)

- General informational messages
- Auto-closes after 8 seconds

#### Warning

- Suspicious activities detected
- Auto-closes after 8 seconds

#### Critical

- Serious violations or errors
- Requires manual dismissal
- May include system alerts

## API Endpoints

### Get Active Notifications

**Endpoint:** `GET /api/exam-notifications/active/`

**Query Parameters:**

- `student_id` (optional) - Filter by student ID
- `exam_id` (optional) - Filter by exam ID

**Example Request:**

```bash
curl "http://localhost:8000/api/exam-notifications/active/?student_id=STUDENT001&exam_id=exam1"
```

**Response:**

```json
[
  {
    "id": 1,
    "created_at": "2024-05-12T10:30:45Z",
    "student_id": "STUDENT001",
    "exam_id": "exam1",
    "message": "Welcome STUDENT001! You have been enrolled for exam exam1. Your activity is being monitored.",
    "severity": "info",
    "active": true
  },
  {
    "id": 2,
    "created_at": "2024-05-12T10:31:15Z",
    "student_id": "STUDENT001",
    "exam_id": "exam1",
    "message": "Alert: Tab Hidden detected during exam. Ensure you remain focused on the exam.",
    "severity": "warning",
    "active": true
  }
]
```

### List All Notifications

**Endpoint:** `GET /api/exam-notifications/`

**Response:** Paginated list of all notifications (only active ones by default)

### Create Notification

**Endpoint:** `POST /api/exam-notifications/`

**Request Body:**

```json
{
  "student_id": "STUDENT001",
  "exam_id": "exam1",
  "message": "Custom notification message",
  "severity": "warning",
  "active": true
}
```

**Response:** Created notification object

### Update Notification

**Endpoint:** `PATCH /api/exam-notifications/{id}/`

**Request Body:**

```json
{
  "active": false
}
```

### Delete Notification

**Endpoint:** `DELETE /api/exam-notifications/{id}/`

## Frontend Display

### Notification Container

Notifications appear in the top-right corner of the exam page in a fixed container.

### Visual Indicators

- **Info** notifications: Blue border
- **Warning** notifications: Orange border
- **Critical** notifications: Red border

### Auto-close Behavior

- **Info & Warning**: Auto-close after 8 seconds
- **Critical**: Require manual dismissal by clicking the × button

## Browser Notifications

### Permission Request

The system automatically requests browser notification permissions when the exam page loads.

### What You'll See

When notifications are enabled, you'll see:

1. Browser notification badge (usually in the top corner or system tray)
2. Notification popup with the message
3. The notification persists until clicked or dismissed by the browser

### Enabling Notifications

1. When the exam page loads, you'll see a permission prompt
2. Click **"Allow"** to enable notifications
3. Click **"Deny"** to disable (you can re-enable later in browser settings)

**Browser Settings:**

- **Chrome**: Settings → Privacy and security → Site settings → Notifications
- **Firefox**: Preferences → Privacy & Security → Permissions → Notifications
- **Safari**: Settings → Websites → Notifications
- **Edge**: Settings → Privacy, search, and services → Site permissions → Notifications

## Automated Tasks

The system runs the following Celery tasks:

### Notify Suspicious Activity

- **Schedule:** Every 30 seconds
- **Function:** Checks for suspicious activities (tab_hidden, lost_focus, page_unload)
- **Action:** Creates warning or critical notifications

### Notify System Alerts

- **Schedule:** Every 60 seconds
- **Function:** Monitors system alerts and CPU/Memory/Disk thresholds
- **Action:** Creates notifications for active exam students

### Cleanup Old Notifications

- **Schedule:** Daily at 3:00 AM
- **Function:** Deletes inactive notifications older than 7 days
- **Action:** Keeps database clean and performant

## Example Usage Scenarios

### Scenario 1: Student Enrolls for Exam

1. Student enters Student ID and Exam ID
2. Clicks "Login & Enroll"
3. **System Action:**
   - Creates enrollment record in ExamActivity
   - **Creates welcome notification**
   - Fetches notification from API
   - **Displays notification in top-right**
   - Shows **browser notification** (if enabled)

### Scenario 2: Suspicious Activity Detected

1. Student minimizes or hides the exam tab
2. **System Action:**
   - Frontend detects visibility change
   - Sends exam event to server
   - Celery task detects the event
   - **Creates warning notification**
   - Frontend fetches new notifications (every 3 seconds)
   - **Displays warning on page**
   - Shows **browser notification**

### Scenario 3: High CPU Usage Alert

1. System monitor detects CPU > 80%
2. **System Action:**
   - Alert is created in database
   - Celery task runs every 60 seconds
   - **Creates critical notification for exam students**
   - Frontend fetches notification
   - **Displays critical notification** (requires manual close)

## Configuration

### Notification Check Interval

Default: Every 3 seconds
Location: [exam.html](monitoring/templates/exam.html) (line: `setInterval(fetchAndDisplayNotifications, 3000)`)
To change: Edit the interval value (in milliseconds)

### Notification Auto-close Duration

Default: 8 seconds for Info/Warning
Location: [exam.html](monitoring/templates/exam.html) (line: `setTimeout(..., 8000)`)
To change: Edit the timeout value (in milliseconds)

### Suspicious Activity Events

Default: `tab_hidden`, `lost_focus`, `page_unload`
Location: [tasks.py](monitoring/tasks.py)
To add more: Edit the `EVENT_CHOICES` in the `ExamActivity` model and the `event_type__in` filter

### Task Schedule

All tasks are configured in [config/celery.py](config/celery.py)

- To change frequency: Edit the `schedule` value
- To disable: Remove from `beat_schedule`
- To add new tasks: Add entry to `beat_schedule`

## Troubleshooting

### Notifications Not Appearing on Page

1. Check browser console for errors (F12 → Console)
2. Verify API endpoint is accessible: `curl http://localhost:8000/api/exam-notifications/`
3. Check if notifications are being created: Login to admin → ExamNotification

### Browser Notifications Not Showing

1. Check notification permissions in browser settings
2. Ensure Notification API is supported by browser
3. Check if "Do Not Disturb" is enabled on your system
4. Verify browser notifications are enabled for the site

### Celery Tasks Not Running

1. Ensure Celery worker is running: `celery -A config worker -l info`
2. Ensure Celery Beat is running: `celery -A config beat -l info`
3. Check task logs for errors
4. Verify tasks are registered: `celery -A config inspect registered`

### Notifications Not Creating Automatically

1. Verify task is scheduled in `config/celery.py`
2. Check Celery logs for task execution
3. Verify exam activities are being recorded
4. Check database permissions for ExamNotification model

## Database Schema

### ExamNotification Model

```python
- id: AutoField (Primary Key)
- created_at: DateTimeField (Auto-created)
- student_id: CharField (max_length=255)
- exam_id: CharField (max_length=255)
- message: TextField
- severity: CharField (choices: 'info', 'warning', 'critical')
- active: BooleanField (default=True)
- created_at: DateTimeField (indexed)
- active: BooleanField (indexed)
- student_id: CharField (indexed)
- exam_id: CharField (indexed)
```

## Performance Considerations

- Notifications are fetched every 3 seconds (configurable)
- Only active notifications are returned by default
- Notifications older than 7 days are automatically cleaned up
- Database indexes optimize queries by student_id and exam_id
- Celery tasks run asynchronously to avoid blocking the web server

## Security Notes

- All exam-related notifications are CSRF-protected
- API endpoints use AllowAny permissions (can be restricted)
- Student IDs and Exam IDs are validated on the server
- Notifications contain no sensitive user data by default
- System notifications are browser-managed (not stored on server)

## Future Enhancements

Possible improvements:

1. Email notifications for critical alerts
2. SMS notifications for high-priority events
3. Notification history/archive for review
4. Custom notification templates
5. Real-time WebSocket updates instead of polling
6. Notification preferences per student/exam
7. Bulk notification creation for events
8. Notification delivery confirmation tracking
