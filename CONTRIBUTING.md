# 🤝 Contributing to ProctorAI

Thank you for your interest in contributing to ProctorAI! We welcome contributions from everyone, whether you're a beginner or an experienced developer.

## 🌟 Ways to Contribute

### 🐛 **Bug Reports**
- Report bugs through [GitHub Issues](https://github.com/RensithUdara/Biometric-Proctoring-System/issues)
- Use the bug report template
- Include system information and steps to reproduce

### 💡 **Feature Requests**
- Suggest new features via [GitHub Issues](https://github.com/RensithUdara/Biometric-Proctoring-System/issues)
- Use the feature request template
- Explain the use case and expected behavior

### 🔧 **Code Contributions**
- Bug fixes
- New features
- Performance improvements
- Documentation updates
- Test coverage improvements

### 📚 **Documentation**
- README improvements
- API documentation
- Code comments
- User guides
- Tutorial videos

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Git
- Basic knowledge of Flask and OpenCV
- Understanding of computer vision concepts

### Development Setup

1. **Fork the Repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/your-username/Biometric-Proctoring-System.git
   cd Biometric-Proctoring-System
   ```

2. **Setup Development Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # Linux/macOS:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Install development dependencies
   pip install -r requirements-dev.txt
   ```

3. **Setup Pre-commit Hooks**
   ```bash
   # Install pre-commit
   pip install pre-commit
   
   # Setup hooks
   pre-commit install
   ```

4. **Run Tests**
   ```bash
   # Run all tests
   pytest
   
   # Run with coverage
   pytest --cov=app --cov-report=html
   ```

## 📋 Development Guidelines

### 🎯 **Code Style**

We follow PEP 8 Python style guidelines with some modifications:

```python
# Good
def analyze_face_detection(image_data, confidence_threshold=0.6):
    """
    Analyze face detection results with confidence scoring.
    
    Args:
        image_data (bytes): Input image data
        confidence_threshold (float): Minimum confidence for valid detection
        
    Returns:
        dict: Detection results with confidence scores
    """
    pass

# Bad
def analyzeFace(img,thresh):
    pass
```

### 🏗️ **Code Structure**

```
app.py                    # Main application logic
├── routes/              # API route handlers
├── models/              # Data models and database
├── services/            # Business logic services
├── utils/               # Utility functions
├── static/              # Frontend assets
└── templates/           # HTML templates
```

### 🧪 **Testing Requirements**

- **Unit Tests**: All new functions must have unit tests
- **Integration Tests**: API endpoints need integration tests
- **Coverage**: Maintain minimum 80% code coverage
- **Documentation**: All public functions need docstrings

```python
# Example test
def test_face_verification_success():
    """Test successful face verification."""
    with app.test_client() as client:
        response = client.post('/verify-face', data={'image': test_image})
        assert response.status_code == 200
        assert response.json['status'] == 'verified'
```

### 📝 **Commit Message Format**

We use conventional commit format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code formatting
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**
```bash
feat(face-recognition): add emotion detection capability
fix(api): resolve camera initialization timeout issue
docs(readme): update installation instructions
test(face-detection): add unit tests for face verification
```

## 🔄 Pull Request Process

### 1. **Create Feature Branch**
```bash
# Create and switch to feature branch
git checkout -b feat/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

### 2. **Make Changes**
- Write clean, readable code
- Add tests for new functionality
- Update documentation as needed
- Follow coding standards

### 3. **Test Your Changes**
```bash
# Run tests
pytest

# Run linting
flake8 app.py

# Check formatting
black --check app.py

# Type checking
mypy app.py
```

### 4. **Commit Changes**
```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat(monitoring): add suspicious object detection"
```

### 5. **Push and Create PR**
```bash
# Push to your fork
git push origin feat/your-feature-name

# Create pull request on GitHub
```

### 6. **PR Requirements**

Your pull request should include:

- [ ] Clear description of changes
- [ ] Link to related issue (if applicable)
- [ ] Tests for new functionality
- [ ] Updated documentation
- [ ] No breaking changes (or clearly documented)
- [ ] All tests passing
- [ ] Code review from maintainers

## 🏷️ **Pull Request Template**

```markdown
## Description
Brief description of changes and motivation.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added new tests for functionality
- [ ] Manual testing completed

## Screenshots/Demo
If applicable, add screenshots or demo links.

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed the code
- [ ] Added comments for complex logic
- [ ] Updated documentation
- [ ] No new warnings introduced
```

## 📊 Development Workflow

### 🔄 **Branching Strategy**

We use GitFlow branching model:

- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: New feature branches
- `fix/*`: Bug fix branches
- `hotfix/*`: Critical production fixes

### 🚀 **Release Process**

1. Create release branch from `develop`
2. Update version numbers
3. Update CHANGELOG.md
4. Test thoroughly
5. Merge to `main` and tag
6. Deploy to production

## 🎨 Frontend Development

### 🖼️ **UI Guidelines**

- Follow Material Design principles
- Ensure responsive design (mobile-first)
- Maintain accessibility standards (WCAG 2.1)
- Use consistent color scheme and typography

### ⚡ **JavaScript Standards**

```javascript
// Use modern JavaScript features
class ProctoringSystem {
    constructor() {
        this.init();
    }
    
    async init() {
        try {
            await this.setupCamera();
        } catch (error) {
            console.error('Initialization failed:', error);
        }
    }
}
```

### 🎨 **CSS Guidelines**

```css
/* Use CSS custom properties */
:root {
    --primary-color: #3b82f6;
    --success-color: #10b981;
}

/* BEM methodology for class names */
.status-card {}
.status-card__icon {}
.status-card--verified {}
```

## 🏗️ Backend Development

### 🐍 **Python Guidelines**

```python
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

def process_face_detection(
    image: bytes, 
    threshold: float = 0.6
) -> Dict[str, Any]:
    """Process face detection with proper error handling."""
    try:
        # Implementation
        pass
    except Exception as e:
        logger.error(f"Face detection failed: {e}")
        raise
```

### 🗄️ **Database Guidelines**

- Use SQLAlchemy ORM for database operations
- Write migrations for schema changes
- Index frequently queried columns
- Use transactions for data consistency

```python
# Good
def create_violation_record(session_id: str, violation_data: dict) -> None:
    """Create violation record with transaction."""
    try:
        with db.transaction():
            violation = Violation(
                session_id=session_id,
                **violation_data
            )
            db.session.add(violation)
            db.session.commit()
    except Exception:
        db.session.rollback()
        raise
```

## 🧪 Testing Guidelines

### 🔍 **Test Categories**

1. **Unit Tests**: Test individual functions
2. **Integration Tests**: Test API endpoints
3. **System Tests**: End-to-end testing
4. **Performance Tests**: Load and stress testing

### 📝 **Writing Tests**

```python
import pytest
from unittest.mock import patch, MagicMock

class TestFaceVerification:
    
    def setup_method(self):
        """Setup test environment."""
        self.app = create_test_app()
        self.client = self.app.test_client()
    
    @patch('app.face_recognition.face_encodings')
    def test_face_verification_success(self, mock_encodings):
        """Test successful face verification."""
        # Arrange
        mock_encodings.return_value = [test_encoding]
        
        # Act
        response = self.client.post('/verify-face', 
                                  data={'image': test_image})
        
        # Assert
        assert response.status_code == 200
        assert response.json['status'] == 'verified'
```

## 📖 Documentation Standards

### 📚 **API Documentation**

Use OpenAPI/Swagger format:

```python
@app.route('/api/verify-face', methods=['POST'])
def verify_face():
    """
    Verify face in uploaded image.
    
    ---
    tags:
      - Face Recognition
    consumes:
      - multipart/form-data
    parameters:
      - name: image
        in: formData
        type: file
        required: true
        description: Image file to analyze
    responses:
      200:
        description: Face verification result
        schema:
          type: object
          properties:
            status:
              type: string
              enum: [verified, unverified, no_face, multiple_faces]
            confidence:
              type: number
              format: float
    """
    pass
```

### 📝 **Code Documentation**

```python
def analyze_attention(image_data: bytes) -> Dict[str, Any]:
    """
    Analyze student attention level from image.
    
    This function uses computer vision techniques to determine
    if a student is paying attention during an exam by analyzing
    eye gaze direction and head pose.
    
    Args:
        image_data: Raw image bytes from camera
        
    Returns:
        Dictionary containing:
            - status: 'focused', 'distracted', or 'unknown'
            - confidence: Float between 0.0 and 1.0
            - details: Additional analysis information
            
    Raises:
        ValueError: If image_data is invalid
        OpenCVError: If image processing fails
        
    Example:
        >>> result = analyze_attention(camera_image)
        >>> print(result['status'])
        'focused'
    """
    pass
```

## 🚨 Issue Management

### 🐛 **Bug Reports**

When reporting bugs, include:

- Operating system and version
- Python version
- Browser (if applicable)
- Steps to reproduce
- Expected vs actual behavior
- Error messages and stack traces
- Screenshots or videos

### 💡 **Feature Requests**

For feature requests, provide:

- Problem statement
- Proposed solution
- Use cases and examples
- Potential alternatives
- Implementation complexity estimate

### 🏷️ **Issue Labels**

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements to docs
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention needed
- `priority-high`: Critical issues
- `priority-low`: Nice to have

## 🎯 Development Priorities

### 🚀 **High Priority**
- Security vulnerabilities
- Performance improvements
- Critical bug fixes
- Core feature stability

### 📈 **Medium Priority**
- New monitoring features
- UI/UX improvements
- API enhancements
- Documentation updates

### 💡 **Low Priority**
- Nice-to-have features
- Code refactoring
- Development tooling
- Experimental features

## 👥 Community Guidelines

### 🤝 **Code of Conduct**

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on what's best for the community
- Show empathy towards other community members

### 💬 **Communication**

- Use GitHub Issues for bug reports and features
- Join our Discord server for discussions
- Follow up on your contributions
- Be patient with code reviews

### 🏆 **Recognition**

Contributors are recognized through:

- GitHub contributor graphs
- CONTRIBUTORS.md file
- Release notes mentions
- Community spotlight posts

## 📞 Getting Help

### 💬 **Communication Channels**

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Discord**: Real-time chat and community support
- **Email**: [maintainer@proctorai.com](mailto:maintainer@proctorai.com)

### 📚 **Resources**

- [Python Documentation](https://docs.python.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [OpenCV Tutorials](https://docs.opencv.org/master/d9/df8/tutorial_root.html)
- [Face Recognition Library](https://face-recognition.readthedocs.io/)

---

## 🎉 Thank You!

Your contributions make ProctorAI better for everyone. Whether you're fixing a typo or adding a major feature, every contribution is valued and appreciated.

**Happy Coding!** 🚀

---

*This contributing guide is a living document. Please suggest improvements via pull requests.*
