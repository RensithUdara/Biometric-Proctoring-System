# 🛡️ ProctorAI - Advanced Biometric Proctoring System

<div align="center">

![ProctorAI Logo](https://img.shields.io/badge/ProctorAI-v2.0-blue?style=for-the-badge&logo=shield-alt)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0+-red?style=for-the-badge&logo=flask)
![OpenCV](https://img.shields.io/badge/OpenCV-4.10+-orange?style=for-the-badge&logo=opencv)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

*A comprehensive AI-powered proctoring solution with real-time biometric verification, intelligent monitoring, and advanced analytics for secure online examinations.*

[🚀 Quick Start](#-installation) • [📖 Documentation](#-documentation) • [🤝 Contributing](#-contributing) • [🐛 Issues](https://github.com/RensithUdara/Biometric-Proctoring-System/issues)

</div>

---

## ✨ What's New in v2.0

### 🔥 **Enhanced AI Detection**
- **Gaze Direction Analysis** - Advanced eye tracking with attention scoring
- **Suspicious Object Detection** - Automatic detection of phones, books, papers
- **Emotion Recognition** - Monitor stress levels and behavioral patterns
- **Image Quality Assessment** - Real-time feedback on lighting and camera positioning

### 🎨 **Modern UI/UX**
- **Completely Redesigned Interface** - Professional, intuitive design
- **Real-time Animations** - Smooth transitions and visual feedback
- **Mobile-Responsive** - Perfect experience across all devices
- **Accessibility Features** - WCAG 2.1 compliant design

### � **Advanced Analytics**
- **Live Dashboard** - Real-time monitoring of all sessions
- **Violation Trends** - Comprehensive analytics with charts
- **Export Capabilities** - JSON/CSV data export
- **Performance Metrics** - System health monitoring

## 🚀 Features

### 🔐 **Biometric Security**
- **Face Recognition**: State-of-the-art face detection and verification
- **Identity Verification**: Continuous monitoring with confidence scoring
- **Multi-face Detection**: Alerts when multiple people are present
- **Liveness Detection**: Prevents photo/video spoofing attempts

### 👁️ **Intelligent Monitoring**
- **Attention Tracking**: Real-time gaze direction analysis
- **Behavior Analysis**: Suspicious activity detection
- **Environmental Monitoring**: Audio and visual distraction detection
- **Screen Activity**: Tab switching and window change detection

### 🛡️ **Security Enforcement**
- **Keyboard Shortcuts**: Prevention of Alt+Tab, Ctrl+C, etc.
- **Context Menus**: Right-click blocking
- **Fullscreen Mode**: Optional fullscreen enforcement
- **Copy Protection**: Prevention of content copying

### 📈 **Comprehensive Reporting**
- **Real-time Violations**: Instant alerts and logging
- **PDF Reports**: Professional violation summaries
- **Analytics Dashboard**: Trends and insights
- **Data Export**: Multiple format support

## 🛠️ Installation

### 🚀 **Quick Start (Recommended)**

#### Windows
```bash
# Clone the repository
git clone https://github.com/RensithUdara/Biometric-Proctoring-System.git
cd Biometric-Proctoring-System

# Run the setup script
setup.bat

# Start the application
start.bat
```

#### Linux/macOS
```bash
# Clone the repository
git clone https://github.com/RensithUdara/Biometric-Proctoring-System.git
cd Biometric-Proctoring-System

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### 🔧 **Manual Installation**

1. **Clone Repository**
```bash
git clone https://github.com/RensithUdara/Biometric-Proctoring-System.git
cd Biometric-Proctoring-System
```

2. **Setup Virtual Environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Application**
```bash
# Create necessary directories
mkdir models\known_faces
mkdir reports

# Optional: Configure settings in config.json
```

5. **Run Application**
```bash
python app.py
```
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create directories**
```bash
mkdir -p models/known_faces reports static templates
```

5. **Add known faces**
   - Place student face images in `models/known_faces/`
   - Name format: `student_name.jpg`
   - Ensure good lighting and clear face visibility

6. **Run the application**
```bash
python app.py
```

7. **Access the system**
   - Open browser to `http://localhost:5000`
   - Dashboard: `http://localhost:5000/dashboard`

## 📋 Usage

### For Students

1. **Start Exam Session**
   - Enter your full name
   - Enter exam name
   - Provide exam URL
   - Click "Start Exam"

2. **During Exam**
   - Keep face visible to camera
   - Avoid multiple people in frame
   - Stay focused on exam window
   - Don't switch tabs or applications

3. **Monitoring Indicators**
   - 🟢 Green: All systems normal
   - 🟡 Yellow: Warning - attention needed
   - 🔴 Red: Violation detected

### For Administrators

1. **Dashboard Access**
   - Visit `/dashboard` for real-time monitoring
   - View active sessions and statistics
   - Monitor violations across all sessions

2. **Face Management**
   - Add new student faces via API
   - Update existing face recognition models
   - Remove outdated face data

3. **Report Generation**
   - Download individual session reports
   - Export violation data for analysis
   - Generate summary statistics

## ⚙️ Configuration

### Face Recognition Settings
```json
{
  "face_recognition": {
    "tolerance": 0.6,
    "model": "large",
    "jitters": 1
  }
}
```

### Monitoring Intervals
```json
{
  "monitoring": {
    "face_check_interval": 5,
    "attention_check_interval": 3,
    "violation_threshold": {
      "consecutive_no_face": 3,
      "max_tab_switches": 5
    }
  }
}
```

### Security Options
```json
{
  "security": {
    "prevent_right_click": true,
    "prevent_keyboard_shortcuts": true,
    "require_fullscreen": false,
    "block_multiple_tabs": true
  }
}
```

## 📊 API Endpoints

### Session Management
- `POST /start-session` - Start new exam session
- `POST /end-session` - End current session
- `GET /api/sessions` - Get all sessions with pagination

### Face Recognition
- `POST /verify-face` - Verify face against known faces
- `POST /analyze-attention` - Analyze attention level
- `POST /api/upload-face` - Upload new known face

### Violations & Reports
- `POST /log-violation` - Log a new violation
- `GET /get-violations` - Get violations for current session
- `GET /download-report` - Download PDF report
- `GET /api/stats` - Get system statistics

### Configuration
- `GET /api/config` - Get current configuration
- `POST /api/config` - Update configuration

## 🔧 Violation Types

| Type | Severity | Description |
|------|----------|-------------|
| `no_face` | High | No face detected in camera |
| `multiple_faces` | Critical | Multiple people detected |
| `unverified` | Critical | Unknown person detected |
| `tab_switch` | Medium | Student switched browser tabs |
| `eyes_not_detected` | Medium | Looking away from screen |
| `camera_denied` | Critical | Camera access blocked |
| `keyboard_shortcut` | Low | Attempted keyboard shortcut |
| `right_click` | Low | Attempted right-click |
| `window_resize` | Low | Browser window resized |
| `exit_fullscreen` | Medium | Exited fullscreen mode |

## 📈 Performance Optimization

### Recommended Hardware
- **CPU**: Multi-core processor (Intel i5+ or AMD Ryzen 5+)
- **RAM**: 8GB minimum, 16GB recommended
- **Camera**: 720p or higher resolution webcam
- **Network**: Stable internet connection (10 Mbps+)

### Browser Optimization
- Use latest version of Chrome or Firefox
- Enable hardware acceleration
- Close unnecessary browser tabs
- Disable browser extensions during exams

### Server Optimization
- Use production WSGI server (Gunicorn, uWSGI)
- Configure reverse proxy (Nginx, Apache)
- Enable database connection pooling
- Implement caching for static assets

## 🛡️ Security Considerations

### Data Privacy
- Face recognition data stored locally
- Session data encrypted at rest
- HTTPS encryption for data transmission
- GDPR compliance for European users

### Access Control
- Session-based authentication
- IP address validation
- Rate limiting on API endpoints
- Cross-origin request protection

### Data Retention
- Configurable data retention periods
- Automatic cleanup of old sessions
- Secure deletion of sensitive data
- Audit logging for data access

## 🐛 Troubleshooting

### Common Issues

#### Camera Not Working
- Check browser permissions for camera access
- Ensure no other applications are using the camera
- Try refreshing the browser page
- Check if camera drivers are properly installed

#### Face Recognition Fails
- Ensure good lighting conditions
- Position face clearly in camera frame
- Check if known face images are properly formatted
- Verify face recognition model is loaded correctly

#### High CPU Usage
- Reduce face recognition frequency in config
- Lower video resolution if needed
- Close other resource-intensive applications
- Check for memory leaks in long-running sessions

#### Database Errors
- Check SQLite file permissions
- Verify database file integrity
- Clear browser cache and cookies
- Restart the application

### Debug Mode
```bash
# Enable debug logging
export FLASK_DEBUG=1
python app.py
```

### Log Files
- Application logs: Check console output
- Database logs: SQLite query logs
- Face recognition logs: OpenCV debug info

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open Pull Request**

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Code formatting
black app.py static/script.js

# Linting
flake8 app.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenCV** for computer vision capabilities
- **face_recognition** library by Adam Geitgey
- **Flask** web framework
- **Bootstrap** for UI components
- **Chart.js** for data visualization

## 📞 Support

For support and questions:
- 📧 Email: support@proctorai.com
- 📱 GitHub Issues: Create an issue in this repository
- 📖 Documentation: Check the wiki for detailed guides
- 💬 Community: Join our Discord server

## 🔮 Future Enhancements

- [ ] Machine learning-based anomaly detection
- [ ] Integration with popular LMS platforms
- [ ] Mobile application for iOS/Android
- [ ] Multi-language support
- [ ] Advanced analytics and AI insights
- [ ] Cloud deployment options
- [ ] Integration with identity verification services
- [ ] Support for multiple camera angles
- [ ] Voice pattern recognition
- [ ] Behavioral analysis algorithms

---

**Made with ❤️ by the ProctorAI Team**

*Ensuring academic integrity through advanced biometric technology*
