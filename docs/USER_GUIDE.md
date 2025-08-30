# 📖 User Guide - ProctorAI

This comprehensive guide covers everything you need to know about using ProctorAI for online examinations.

## 👥 User Roles

### 👨‍🎓 Students
Learn how to take exams with ProctorAI monitoring

### 👨‍💼 Administrators  
Manage the system, configure settings, and oversee operations

### 👨‍🏫 Instructors
Monitor active exams and review violation reports

---

## 👨‍🎓 Student Guide

### 🚀 Getting Started

#### System Requirements
- **Browser**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Camera**: Webcam with 720p resolution (1080p recommended)
- **Internet**: Stable connection with 5 Mbps+ upload speed
- **Lighting**: Well-lit environment with face clearly visible
- **Environment**: Quiet, private space free from distractions

#### Before Your Exam

1. **Test Your Setup**
   - Visit the test page at `/test-setup`
   - Ensure camera and microphone permissions are granted
   - Verify your face is properly detected
   - Check internet connection stability

2. **Prepare Your Environment**
   - Remove distracting items from your workspace
   - Ensure good lighting (face should be clearly visible)
   - Position camera at eye level
   - Clear your desk of unauthorized materials

3. **Browser Preparation**
   - Close unnecessary tabs and applications
   - Disable browser extensions (except required ones)
   - Enable full-screen mode if required
   - Clear browser cache if experiencing issues

### 📝 Taking an Exam

#### Step 1: Starting Your Exam Session

1. **Navigate to Exam URL**
   ```
   https://your-exam-portal.com
   ```

2. **Enter Required Information**
   - **Student Name**: Your full legal name
   - **Exam Name**: Course code or exam identifier  
   - **Exam URL**: Link provided by your instructor

3. **Grant Permissions**
   - Click "Allow" when prompted for camera access
   - Grant microphone access if required
   - Enable screen sharing if requested

#### Step 2: Identity Verification

1. **Face Recognition Setup**
   - Look directly at the camera
   - Ensure your face is well-lit and clearly visible
   - Wait for green checkmark indicating successful verification
   - If verification fails, adjust lighting and try again

2. **ID Verification** (if required)
   - Hold your student ID card next to your face
   - Ensure both face and ID are clearly visible
   - Wait for verification confirmation

#### Step 3: Pre-Exam Checklist

✅ **System Status Indicators**
- 🟢 **Face Verified**: Your identity has been confirmed
- 🟢 **Camera Active**: Video monitoring is functioning
- 🟢 **Attention Tracked**: Gaze monitoring is active
- 🟢 **Environment Clear**: No violations detected

#### Step 4: During the Exam

**✅ DO:**
- Keep your face visible to the camera at all times
- Look at the screen and maintain focus
- Sit upright and avoid excessive movement
- Keep your hands visible when typing
- Stay within the camera frame

**❌ DON'T:**
- Look away from the screen for extended periods
- Cover your face or camera
- Have other people in the room
- Use unauthorized materials or devices
- Switch tabs or leave the exam window
- Use keyboard shortcuts (Alt+Tab, Ctrl+C, etc.)
- Right-click or access browser menus

### 🚨 Understanding Violations

#### Violation Types and Severity

**🟡 Level 1 - Minor** (Warnings)
- Brief glances away from screen
- Minor head movements
- Temporary hand obstruction

**🟠 Level 2 - Moderate** (Cautions)
- Extended looking away (>5 seconds)
- Repeated minor violations
- Suspicious hand movements

**🔴 Level 3 - Serious** (Major Concerns)
- Multiple people detected
- Unauthorized objects visible
- Covering camera or face
- Tab switching attempts

**⚫ Level 4 - Critical** (Immediate Action)
- Unrecognized person detected
- Cheating materials visible
- System tampering attempts
- Repeated serious violations

#### What Happens When Violations Occur

1. **Real-time Alerts**
   - Visual warning appears on screen
   - Audio alert may sound (if enabled)
   - Violation is logged with timestamp

2. **Corrective Action**
   - Warning message explains the issue
   - Instructions for resolution provided
   - Countdown timer for compliance

3. **Escalation**
   - Instructor may be notified immediately
   - Exam may be paused for review
   - Multiple violations may result in termination

### 🛠️ Troubleshooting Common Issues

#### Camera Issues

**Problem**: Camera not detected
```
Solution:
1. Check camera permissions in browser
2. Close other applications using camera
3. Restart browser
4. Try different browser
```

**Problem**: Poor image quality
```
Solution:
1. Improve lighting (face toward light source)
2. Clean camera lens
3. Adjust camera position
4. Check camera resolution settings
```

#### Face Recognition Issues

**Problem**: Face not recognized
```
Solution:
1. Ensure face is centered in camera
2. Remove glasses or hats if possible
3. Improve lighting conditions
4. Contact administrator if issues persist
```

**Problem**: Multiple faces detected
```
Solution:
1. Ensure you're alone in the room
2. Check for reflective surfaces
3. Adjust camera angle
4. Remove photos or posters with faces
```

#### Performance Issues

**Problem**: System running slowly
```
Solution:
1. Close unnecessary browser tabs
2. Restart browser
3. Check internet connection speed
4. Close other applications
5. Clear browser cache
```

**Problem**: Frequent disconnections
```
Solution:
1. Check internet stability
2. Move closer to WiFi router
3. Use ethernet connection if possible
4. Disable bandwidth-heavy applications
```

---

## 👨‍💼 Administrator Guide

### 🏗️ System Setup

#### Initial Configuration

1. **Install ProctorAI**
   ```bash
   git clone https://github.com/RensithUdara/Biometric-Proctoring-System.git
   cd Biometric-Proctoring-System
   ./setup.bat
   ```

2. **Configure Settings**
   - Edit `config.json` for custom settings
   - Set up database connections
   - Configure email notifications
   - Customize violation thresholds

3. **Add Student Photos**
   - Place student photos in `models/known_faces/`
   - Use format: `StudentName.jpg`
   - Ensure high-quality, well-lit photos
   - One face per photo, looking directly at camera

#### User Management

**Adding Students**
```python
# Via API
POST /api/students
{
  "name": "John Doe",
  "student_id": "12345",
  "email": "john@university.edu",
  "photo": "base64_encoded_image"
}
```

**Managing Instructors**
```python
# Via API
POST /api/instructors
{
  "name": "Prof. Smith",
  "email": "smith@university.edu",
  "permissions": ["monitor", "reports"]
}
```

### 📊 Monitoring Dashboard

Access the admin dashboard at: `http://your-server/dashboard`

#### Real-time Monitoring

**Active Sessions Panel**
- Live count of active exam sessions
- Student names and exam details
- Real-time violation alerts
- Session duration and status

**System Health**
- Server resource usage (CPU, Memory)
- Database connection status
- Camera service availability
- Network performance metrics

**Violation Alerts**
- Real-time violation notifications
- Severity level indicators
- Quick action buttons (pause/terminate exam)
- Automatic escalation rules

#### Reports and Analytics

**Session Reports**
- Detailed exam session summaries
- Individual student performance
- Violation timeline and evidence
- PDF export capabilities

**Trend Analysis**
- Violation patterns over time
- Peak usage periods
- System performance trends
- Student behavior analytics

**Compliance Reports**
- Audit trail of all activities
- Data retention compliance
- Privacy policy adherence
- Security incident reports

### ⚙️ Configuration Management

#### Core Settings (`config.json`)

```json
{
  "monitoring": {
    "face_check_interval": 3,
    "attention_check_interval": 2,
    "violation_threshold": {
      "minor": 5,
      "moderate": 3,
      "serious": 2,
      "critical": 1
    }
  },
  "security": {
    "session_timeout": 7200,
    "max_concurrent_sessions": 100,
    "require_student_id": true,
    "enable_screenshot_capture": true
  },
  "notifications": {
    "email_alerts": true,
    "sms_alerts": false,
    "webhook_url": "https://your-webhook.com/alerts"
  }
}
```

#### Advanced Configuration

**Database Settings**
```json
{
  "database": {
    "type": "sqlite",
    "path": "reports/proctoring.db",
    "backup_enabled": true,
    "backup_interval": "24h"
  }
}
```

**Performance Tuning**
```json
{
  "performance": {
    "max_concurrent_sessions": 50,
    "image_processing_threads": 4,
    "cache_duration": 300,
    "cleanup_interval": 3600
  }
}
```

### 🔐 Security Management

#### Access Control

**Role-Based Permissions**
- **Super Admin**: Full system access
- **Admin**: User management and configuration  
- **Instructor**: Exam monitoring and reports
- **Student**: Exam taking only

**API Key Management**
```bash
# Generate new API key
python manage.py generate-api-key --role admin --expires 30d

# Revoke API key
python manage.py revoke-api-key --key abc123...
```

#### Data Protection

**Encryption Settings**
- All biometric data encrypted at rest
- TLS 1.3 for data in transit
- Regular security audits and updates
- GDPR compliance features

**Privacy Controls**
- Automatic data retention policies
- Student consent management
- Right to deletion implementation
- Data anonymization options

---

## 👨‍🏫 Instructor Guide

### 📺 Live Exam Monitoring

#### Accessing the Monitor Dashboard

1. **Login to Instructor Portal**
   ```
   https://your-server/instructor-login
   ```

2. **Select Active Exam**
   - Choose from list of ongoing exams
   - View exam details and participant count
   - Access monitoring tools

#### Real-time Monitoring Features

**Student Grid View**
- Live camera feeds from all students
- Status indicators for each student
- Quick access to individual student details
- Violation alerts and notifications

**Violation Management**
- Real-time violation alerts
- Severity level classification
- Evidence capture (screenshots)
- Action buttons (warn, pause, terminate)

**Communication Tools**
- Send messages to individual students
- Broadcast announcements to all
- Audio communication (if enabled)
- Chat functionality

### 📊 Post-Exam Analysis

#### Violation Reports

**Individual Student Reports**
- Complete violation timeline
- Evidence images and details
- Severity analysis and recommendations
- Export options (PDF, CSV)

**Exam Summary Reports**
- Overall exam statistics
- Violation distribution by type
- Student performance comparison
- Integrity assessment scores

**Trend Analysis**
- Compare with historical data
- Identify patterns and anomalies
- Student behavior insights
- System performance metrics

#### Export and Sharing

**Report Generation**
```bash
# Generate exam report
GET /api/reports/exam/{exam_id}

# Export student data
GET /api/reports/student/{student_id}/violations
```

**Integration with LMS**
- Canvas integration support
- Moodle compatibility
- Blackboard export formats
- Custom API integrations

### 🎯 Best Practices for Instructors

#### Pre-Exam Preparation

1. **Communicate Requirements**
   - Send setup instructions to students
   - Provide test links for system checks
   - Set clear expectations and rules
   - Share violation consequences

2. **Configure Exam Settings**
   - Adjust sensitivity levels if needed
   - Set violation thresholds appropriately  
   - Enable necessary monitoring features
   - Test system functionality

#### During Exam Monitoring

1. **Active Supervision**
   - Monitor violation alerts actively
   - Respond to student questions quickly
   - Make fair and consistent decisions
   - Document any interventions

2. **Violation Response**
   - Review evidence before taking action
   - Consider context and circumstances
   - Provide clear communication to students
   - Follow institutional policies

#### Post-Exam Review

1. **Analyze Results**
   - Review all violation reports
   - Identify any false positives
   - Consider student explanations
   - Make final integrity determinations

2. **Continuous Improvement**
   - Gather student feedback
   - Adjust settings for future exams
   - Update procedures based on experience
   - Share insights with colleagues

---

## 📞 Support and Resources

### 🆘 Getting Help

**Technical Support**
- Email: support@proctorai.com
- Phone: 1-800-PROCTOR
- Live Chat: Available on website
- GitHub Issues: For bug reports

**Training Resources**
- Video tutorials
- Webinar sessions
- User documentation
- Best practices guides

**Community Support**
- User forums
- Discord server
- Reddit community
- Facebook groups

### 📚 Additional Resources

**Educational Resources**
- Academic integrity guidelines
- Remote proctoring research
- Privacy and ethics considerations
- Technology adoption strategies

**Technical Documentation**
- API documentation
- Integration guides
- Customization tutorials
- Security best practices

---

*This user guide is continuously updated. For the latest version, visit our [documentation portal](https://docs.proctorai.com).*
