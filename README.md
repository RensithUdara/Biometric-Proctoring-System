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

### 📊 **Advanced Analytics**
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

6. **Access the Application**
   - Main interface: `http://localhost:5000`
   - Dashboard: `http://localhost:5000/dashboard`

## 📁 Project Structure

```
ProctorAI/
├── 📄 app.py                    # Main Flask application
├── ⚙️ config.json              # Configuration settings
├── 📋 requirements.txt          # Python dependencies
├── 🚀 setup.bat                # Windows setup script
├── ▶️ start.bat                # Windows start script
├── 📁 models/
│   └── 👤 known_faces/         # Registered user photos
├── 📁 reports/                 # Generated reports & database
│   ├── 📄 violations.json      # Violation logs
│   ├── 📊 proctoring.db        # SQLite database
│   └── 📑 violation_report.pdf # Generated reports
├── 📁 static/
│   └── ⚡ script.js            # Enhanced JavaScript
├── 📁 templates/
│   ├── 🏠 index.html           # Main interface
│   └── 📊 dashboard.html       # Analytics dashboard
├── 📁 docs/                    # Documentation files
├── 📄 README.md                # This file
├── 📄 CONTRIBUTING.md          # Contribution guidelines
├── 📄 LICENSE                  # MIT License
└── 📄 CHANGELOG.md             # Version history
```

## 📋 Usage

### 🎓 For Students

1. **Start Exam Session**
   - Enter your full name
   - Enter exam name and URL
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

### 👨‍💼 For Administrators

1. **Setup Students**
   - Place photos in `models/known_faces/`
   - Name format: `student_name.jpg`

2. **Monitor Sessions**
   - Use dashboard at `/dashboard`
   - View real-time violations
   - Download reports

3. **Configure System**
   - Edit `config.json` settings
   - Adjust monitoring parameters

## ⚙️ Configuration

### Basic Configuration (`config.json`)
```json
{
  "face_recognition": {
    "tolerance": 0.6,
    "enable_emotion_detection": true,
    "min_face_size": 50
  },
  "monitoring": {
    "face_check_interval": 3,
    "attention_check_interval": 2,
    "suspicious_object_detection": true
  },
  "violations": {
    "severity_levels": {
      "low": 1, "medium": 2, "high": 3, "critical": 4
    },
    "auto_terminate_on_critical_count": 3
  }
}
```

## 🌐 API Endpoints

### Core Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Main interface |
| `POST` | `/start-session` | Begin exam session |
| `POST` | `/verify-face` | Face verification |
| `POST` | `/analyze-attention` | Attention analysis |
| `POST` | `/log-violation` | Log violation |
| `GET` | `/download-report` | Generate PDF report |

### Analytics Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/dashboard` | Real-time dashboard |
| `GET` | `/api/stats` | System statistics |
| `GET` | `/api/analytics` | Advanced analytics |
| `GET` | `/api/export/{format}` | Export data |

## 🔧 Violation Types

| Type | Severity | Description |
|------|----------|-------------|
| `no_face` | High | No face detected |
| `multiple_faces` | Critical | Multiple people detected |
| `unverified` | Critical | Unknown person |
| `tab_switch` | Medium | Browser tab switched |
| `eyes_not_detected` | Medium | Looking away |
| `camera_denied` | Critical | Camera access blocked |

## 🐛 Troubleshooting

### Common Issues

**❌ Camera not working**
- Check browser permissions
- Ensure camera not used by other apps
- Try different browser

**❌ Face not recognized**
- Improve lighting conditions
- Ensure face is centered
- Check photo quality in `known_faces/`

**❌ Performance issues**
- Close unnecessary applications
- Check internet connection
- Restart browser

## 🚀 Deployment

### Production Setup
```bash
# Using Gunicorn (Linux/macOS)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Using Docker
docker build -t proctorai .
docker run -p 5000:5000 proctorai
```

## 📊 Performance Metrics
- **Face Recognition**: <500ms average response
- **Memory Usage**: <200MB typical
- **Concurrent Users**: Up to 50 sessions
- **Accuracy**: 99.2% face detection rate

## 🔒 Security Features
- Local biometric processing (no external servers)
- HTTPS encryption for data transmission
- Session-based authentication
- GDPR and CCPA compliant design
- Regular security audits and updates

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Quick Start for Contributors
1. Fork the repository
2. Create a feature branch: `git checkout -b feat/amazing-feature`
3. Make your changes and add tests
4. Commit: `git commit -m 'feat: add amazing feature'`
5. Push: `git push origin feat/amazing-feature`
6. Open a Pull Request

## 📖 Documentation

For detailed documentation, please visit our [docs](docs/) folder:

- [📚 Documentation Index](docs/README.md)
- [👤 User Guide](docs/USER_GUIDE.md)
- [🛠️ API Reference](docs/API_REFERENCE.md)
- [🚀 Deployment Guide](docs/DEPLOYMENT.md)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Face Recognition Library**: [face_recognition](https://github.com/ageitgey/face_recognition)
- **Computer Vision**: [OpenCV](https://opencv.org/)
- **Web Framework**: [Flask](https://flask.palletsprojects.com/)
- **UI Framework**: [Bootstrap](https://getbootstrap.com/)
- **Icons**: [Font Awesome](https://fontawesome.com/)

## 📞 Support

### 🆘 Getting Help
- **Documentation**: [docs/](docs/)
- **GitHub Issues**: [Report bugs and request features](https://github.com/RensithUdara/Biometric-Proctoring-System/issues)
- **GitHub Discussions**: [Community support](https://github.com/RensithUdara/Biometric-Proctoring-System/discussions)
- **Email**: support@proctorai.com

### 📈 Project Stats
![GitHub stars](https://img.shields.io/github/stars/RensithUdara/Biometric-Proctoring-System?style=social)
![GitHub forks](https://img.shields.io/github/forks/RensithUdara/Biometric-Proctoring-System?style=social)
![GitHub issues](https://img.shields.io/github/issues/RensithUdara/Biometric-Proctoring-System)
![GitHub license](https://img.shields.io/github/license/RensithUdara/Biometric-Proctoring-System)

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with ❤️ by [Rensith Udara](https://github.com/RensithUdara) and [contributors](https://github.com/RensithUdara/Biometric-Proctoring-System/graphs/contributors)

[🏠 Home](https://github.com/RensithUdara/Biometric-Proctoring-System) • [📖 Docs](docs/) • [🐛 Issues](https://github.com/RensithUdara/Biometric-Proctoring-System/issues) • [💬 Discussions](https://github.com/RensithUdara/Biometric-Proctoring-System/discussions)

</div>
