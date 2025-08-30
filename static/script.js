// Enhanced Proctoring System JavaScript
class ProctoringSystem {
    constructor() {
        this.video = document.getElementById('webcam');
        this.examFrame = document.getElementById('examFrame');
        this.sessionId = null;
        this.isExamActive = false;
        this.monitoringInterval = null;
        this.attentionInterval = null;
        this.violationCount = 0;
        this.lastFaceStatus = null;
        this.consecutiveNoFace = 0;
        this.tabSwitchCount = 0;
        this.isRecording = false;
        this.analytics = {
            faceVerifications: 0,
            attentionChecks: 0,
            totalViolations: 0,
            sessionStartTime: null
        };
        
        this.initializeCamera();
        this.setupEventListeners();
        this.loadSavedData();
        this.initializeAnalytics();
    }

    initializeAnalytics() {
        this.analytics.sessionStartTime = new Date();
        this.updateAnalyticsDisplay();
    }

    updateAnalyticsDisplay() {
        // Update analytics in the UI if elements exist
        const elements = {
            faceVerifications: document.getElementById('faceVerifications'),
            attentionChecks: document.getElementById('attentionChecks'),
            sessionDuration: document.getElementById('sessionDuration')
        };

        if (elements.faceVerifications) {
            elements.faceVerifications.textContent = this.analytics.faceVerifications;
        }
        if (elements.attentionChecks) {
            elements.attentionChecks.textContent = this.analytics.attentionChecks;
        }
        if (elements.sessionDuration && this.analytics.sessionStartTime) {
            const duration = new Date() - this.analytics.sessionStartTime;
            const minutes = Math.floor(duration / 60000);
            elements.sessionDuration.textContent = `${minutes} minutes`;
        }
    }

    async initializeCamera() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ 
                video: { 
                    width: { ideal: 1280 },
                    height: { ideal: 720 },
                    frameRate: { ideal: 30 }
                },
                audio: true 
            });
            
            this.video.srcObject = stream;
            this.updateStatus('faceStatus', 'Camera initialized', 'success');
            this.showNotification('Camera access granted', 'success');
        } catch (err) {
            console.error('Camera access error:', err);
            this.updateStatus('faceStatus', 'Camera access denied', 'danger');
            this.showNotification('Camera access denied. Please enable camera permissions.', 'danger');
            this.logViolation("camera_denied", "User denied camera access", 4);
        }
    }

    setupEventListeners() {
        // Tab visibility change detection
        document.addEventListener("visibilitychange", () => {
            if (document.hidden && this.isExamActive) {
                this.tabSwitchCount++;
                this.logViolation("tab_switch", `User left the exam tab (${this.tabSwitchCount} times)`, 3);
                this.updateStatus('activityStatus', `Tab switches: ${this.tabSwitchCount}`, 'warning');
                this.playAlert();
            }
        });

        // Keyboard shortcuts prevention
        document.addEventListener('keydown', (e) => {
            if (this.isExamActive) {
                // Prevent Alt+Tab, Ctrl+T, Ctrl+N, etc.
                if ((e.altKey && e.code === 'Tab') || 
                    (e.ctrlKey && (e.code === 'KeyT' || e.code === 'KeyN' || e.code === 'KeyW'))) {
                    e.preventDefault();
                    this.logViolation("keyboard_shortcut", `Attempted to use ${e.code} shortcut`, 2);
                }
            }
        });

        // Right-click prevention
        document.addEventListener('contextmenu', (e) => {
            if (this.isExamActive) {
                e.preventDefault();
                this.logViolation("right_click", "Attempted to open context menu", 1);
            }
        });

        // Window resize detection
        window.addEventListener('resize', () => {
            if (this.isExamActive) {
                this.logViolation("window_resize", "Window was resized during exam", 1);
            }
        });

        // Fullscreen detection
        document.addEventListener('fullscreenchange', () => {
            if (!document.fullscreenElement && this.isExamActive) {
                this.logViolation("exit_fullscreen", "Exited fullscreen mode", 2);
            }
        });
    }

    loadSavedData() {
        const savedSession = localStorage.getItem('proctoringSession');
        if (savedSession) {
            const sessionData = JSON.parse(savedSession);
            document.getElementById('studentName').value = sessionData.studentName || '';
            document.getElementById('examName').value = sessionData.examName || '';
        }
    }

    async startExam() {
        const studentName = document.getElementById('studentName').value.trim();
        const examName = document.getElementById('examName').value.trim();
        const examUrl = document.getElementById('examUrl').value.trim();

        if (!studentName || !examName || !examUrl) {
            this.showNotification('Please fill in all fields before starting the exam.', 'warning');
            return;
        }

        try {
            // Start session
            const response = await fetch('/start-session', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ student_name: studentName, exam_name: examName })
            });

            const data = await response.json();
            if (data.status === 'success') {
                this.sessionId = data.session_id;
                this.isExamActive = true;

                // Save session data
                localStorage.setItem('proctoringSession', JSON.stringify({
                    sessionId: this.sessionId,
                    studentName: studentName,
                    examName: examName,
                    startTime: new Date().toISOString()
                }));

                // Update UI
                document.getElementById('sessionId').textContent = this.sessionId;
                document.getElementById('setupSection').style.display = 'none';
                document.getElementById('monitoringSection').style.display = 'block';
                document.getElementById('recordingIndicator').style.display = 'block';

                // Load exam
                this.examFrame.src = examUrl;
                this.examFrame.style.display = 'block';
                document.getElementById('examPlaceholder').style.display = 'none';

                // Start monitoring
                this.startMonitoring();
                this.startAttentionTracking();
                
                this.showNotification(`Exam started successfully! Session: ${this.sessionId}`, 'success');
                
                // Initial face verification
                setTimeout(() => this.verifyFace(), 2000);
            }
        } catch (error) {
            console.error('Error starting exam:', error);
            this.showNotification('Error starting exam. Please try again.', 'danger');
        }
    }

    startMonitoring() {
        this.monitoringInterval = setInterval(() => {
            this.verifyFace();
            this.updateViolationDisplay();
        }, 5000); // Check every 5 seconds
    }

    startAttentionTracking() {
        this.attentionInterval = setInterval(() => {
            this.analyzeAttention();
        }, 3000); // Check attention every 3 seconds
    }

    async verifyFace() {
        if (!this.video.videoWidth || !this.video.videoHeight) return;

        try {
            const canvas = document.createElement('canvas');
            canvas.width = this.video.videoWidth;
            canvas.height = this.video.videoHeight;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(this.video, 0, 0);

            canvas.toBlob(async (blob) => {
                const formData = new FormData();
                formData.append('image', blob);

                try {
                    const response = await fetch('/verify-face', {
                        method: 'POST',
                        body: formData
                    });

                    const data = await response.json();
                    this.analytics.faceVerifications++;
                    this.handleFaceVerificationResult(data);
                    this.updateAnalyticsDisplay();
                } catch (error) {
                    console.error('Face verification error:', error);
                    this.updateStatus('faceStatus', 'Verification error', 'danger');
                    this.addSystemLog('Face verification failed', 'error');
                }
            }, 'image/jpeg', 0.8);
        } catch (error) {
            console.error('Face capture error:', error);
            this.addSystemLog('Face capture error', 'error');
        }
    }

    async analyzeAttention() {
        if (!this.video.videoWidth || !this.video.videoHeight) return;

        try {
            const canvas = document.createElement('canvas');
            canvas.width = this.video.videoWidth;
            canvas.height = this.video.videoHeight;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(this.video, 0, 0);

            canvas.toBlob(async (blob) => {
                const formData = new FormData();
                formData.append('image', blob);

                try {
                    const response = await fetch('/analyze-attention', {
                        method: 'POST',
                        body: formData
                    });

                    const data = await response.json();
                    this.analytics.attentionChecks++;
                    this.handleAttentionResult(data);
                    this.updateAnalyticsDisplay();
                } catch (error) {
                    console.error('Attention analysis error:', error);
                    this.addSystemLog('Attention analysis failed', 'error');
                }
            }, 'image/jpeg', 0.8);
        } catch (error) {
            console.error('Attention capture error:', error);
        }
    }

    handleFaceVerificationResult(data) {
        const faceCard = document.getElementById('faceStatusCard');
        const faceStatus = document.getElementById('faceStatus');

        // Handle enhanced analysis data
        if (data.analysis) {
            this.handleAnalysisData(data.analysis);
        }

        switch (data.status) {
            case 'verified':
                this.updateStatus('faceStatus', 
                    `✓ Verified: ${data.name} (${data.confidence}%)`, 'success');
                faceCard.className = 'status-card verified fade-in';
                this.consecutiveNoFace = 0;
                this.addSystemLog(`Face verified: ${data.name} with ${data.confidence}% confidence`, 'success');
                break;
            case 'no_face':
                this.consecutiveNoFace++;
                this.updateStatus('faceStatus', '⚠ No face detected', 'danger');
                faceCard.className = 'status-card danger fade-in';
                if (this.consecutiveNoFace >= 3) {
                    this.playAlert();
                    this.showNotification('⚠ Please ensure your face is visible to the camera!', 'warning');
                    this.addSystemLog('Multiple consecutive no-face detections', 'warning');
                }
                break;
            case 'multiple_faces':
                this.updateStatus('faceStatus', `🚫 Multiple faces (${data.face_count})`, 'danger');
                faceCard.className = 'status-card danger fade-in';
                this.playAlert();
                this.showNotification('🚫 Multiple people detected! Only the student should be visible.', 'danger');
                this.addSystemLog(`Multiple faces detected: ${data.face_count}`, 'danger');
                break;
            case 'unverified':
                this.updateStatus('faceStatus', '❌ Face not recognized', 'danger');
                faceCard.className = 'status-card danger fade-in';
                this.playAlert();
                this.showNotification('❌ Unrecognized person detected!', 'danger');
                this.addSystemLog('Unrecognized person detected', 'danger');
                break;
            default:
                this.updateStatus('faceStatus', '🔍 Checking...', 'warning');
                faceCard.className = 'status-card warning fade-in';
        }
    }

    handleAnalysisData(analysis) {
        // Handle image quality feedback
        if (analysis.image_quality) {
            const quality = analysis.image_quality;
            if (quality.score < 50) {
                this.showNotification(`Image quality issues: ${quality.issues.join(', ')}`, 'info');
            }
        }

        // Handle suspicious objects
        if (analysis.suspicious_objects && analysis.suspicious_objects.length > 0) {
            analysis.suspicious_objects.forEach(obj => {
                this.showNotification(`⚠ Suspicious object detected: ${obj}`, 'warning');
                this.addSystemLog(`Suspicious object: ${obj}`, 'warning');
            });
        }

        // Handle gaze analysis
        if (analysis.gaze_analysis) {
            const gaze = analysis.gaze_analysis;
            this.updateGazeDisplay(gaze);
        }
    }

    updateGazeDisplay(gazeData) {
        const gazeElement = document.getElementById('gazeScore');
        if (gazeElement) {
            gazeElement.textContent = `Attention Score: ${gazeData.score || 0}%`;
        }
    }

    handleAttentionResult(data) {
        const attentionCard = document.getElementById('attentionStatusCard');
        const attentionStatus = document.getElementById('attentionStatus');

        // Handle enhanced analysis data
        if (data.analysis) {
            const score = data.analysis.attention_score || 0;
            const details = data.details || [];
            
            switch (data.status) {
                case 'attentive':
                    this.updateStatus('attentionStatus', `👁 Focused (Score: ${score}%)`, 'success');
                    attentionCard.className = 'status-card verified fade-in';
                    break;
                case 'attention_warning':
                    this.updateStatus('attentionStatus', `⚠ Attention Warning (Score: ${score}%)`, 'warning');
                    attentionCard.className = 'status-card warning fade-in';
                    this.showNotification('Please focus on the exam', 'warning');
                    break;
                case 'distracted':
                    this.updateStatus('attentionStatus', `❌ Distracted (Score: ${score}%)`, 'danger');
                    attentionCard.className = 'status-card danger fade-in';
                    this.showNotification('Student appears distracted', 'danger');
                    break;
                default:
                    this.updateStatus('attentionStatus', '🔍 Monitoring...', 'warning');
                    attentionCard.className = 'status-card warning fade-in';
            }
        }
    }

    addSystemLog(message, type) {
        const timestamp = new Date().toLocaleTimeString();
        console.log(`[${timestamp}] ${type.toUpperCase()}: ${message}`);
        
        // You could also add to a visual log panel if it exists
        const logPanel = document.getElementById('systemLogs');
        if (logPanel) {
            const logEntry = document.createElement('div');
            logEntry.className = `log-entry log-${type}`;
            logEntry.innerHTML = `
                <span class="log-time">${timestamp}</span>
                <span class="log-message">${message}</span>
            `;
            logPanel.prepend(logEntry);
            
            // Keep only last 10 entries
            while (logPanel.children.length > 10) {
                logPanel.removeChild(logPanel.lastChild);
            }
        }
    }

    handleAttentionResult(data) {
        const attentionCard = document.getElementById('attentionStatusCard');
        const attentionStatus = document.getElementById('attentionStatus');

        switch (data.status) {
            case 'attentive':
                this.updateStatus('attentionStatus', `Focused (${data.eyes_detected} eyes)`, 'success');
                attentionCard.className = 'status-card verified';
                break;
            case 'attention_warning':
                this.updateStatus('attentionStatus', 'Looking away detected', 'warning');
                attentionCard.className = 'status-card warning';
                break;
            default:
                this.updateStatus('attentionStatus', 'Monitoring...', 'warning');
                attentionCard.className = 'status-card warning';
        }
    }

    async updateViolationDisplay() {
        try {
            const response = await fetch('/get-violations');
            const data = await response.json();
            
            this.violationCount = data.violations.length;
            this.updateStatus('violationCount', `${this.violationCount} violations`, 
                this.violationCount > 0 ? 'danger' : 'success');

            const panel = document.getElementById('violationsPanel');
            if (data.violations.length === 0) {
                panel.innerHTML = `
                    <div class="text-center py-4 text-muted">
                        <i class="fas fa-check-circle fa-2x mb-2"></i>
                        <p class="mb-0">No violations detected</p>
                    </div>`;
            } else {
                panel.innerHTML = data.violations.slice(0, 10).map(violation => `
                    <div class="violation-item">
                        <div class="violation-severity severity-${violation.severity}"></div>
                        <div>
                            <strong>${this.formatViolationType(violation.type)}</strong>
                            <br>
                            <small class="text-muted">${new Date(violation.timestamp).toLocaleTimeString()}</small>
                            <br>
                            <small>${violation.details}</small>
                        </div>
                    </div>
                `).join('');
            }

            // Update violation status card
            const violationCard = document.getElementById('violationStatusCard');
            if (this.violationCount === 0) {
                violationCard.className = 'status-card verified';
            } else if (this.violationCount < 3) {
                violationCard.className = 'status-card warning';
            } else {
                violationCard.className = 'status-card danger';
            }

        } catch (error) {
            console.error('Error updating violations:', error);
        }
    }

    formatViolationType(type) {
        const typeMap = {
            'no_face': 'No Face Detected',
            'multiple_faces': 'Multiple People',
            'unverified': 'Unauthorized Person',
            'tab_switch': 'Tab Switch',
            'camera_denied': 'Camera Blocked',
            'eyes_not_detected': 'Looking Away',
            'keyboard_shortcut': 'Shortcut Key',
            'right_click': 'Right Click',
            'window_resize': 'Window Resized',
            'exit_fullscreen': 'Exited Fullscreen'
        };
        return typeMap[type] || type.charAt(0).toUpperCase() + type.slice(1);
    }

    async logViolation(type, details, severity = 1) {
        try {
            await fetch('/log-violation', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ type, details, severity })
            });
        } catch (error) {
            console.error('Error logging violation:', error);
        }
    }

    updateStatus(elementId, text, type = 'muted') {
        const element = document.getElementById(elementId);
        if (element) {
            element.textContent = text;
            element.className = `text-${type}`;
        }
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; left: 50%; transform: translateX(-50%); z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
        `;

        document.body.appendChild(notification);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }

    playAlert() {
        const alertSound = document.getElementById('alertSound');
        if (alertSound) {
            alertSound.currentTime = 0;
            alertSound.play().catch(e => console.log('Audio play failed:', e));
        }
    }

    async endExam() {
        if (!this.isExamActive) return;

        try {
            const response = await fetch('/end-session', { method: 'POST' });
            const data = await response.json();

            if (data.status === 'success') {
                this.isExamActive = false;
                
                // Clear intervals
                if (this.monitoringInterval) clearInterval(this.monitoringInterval);
                if (this.attentionInterval) clearInterval(this.attentionInterval);

                // Update UI
                document.getElementById('setupSection').style.display = 'block';
                document.getElementById('monitoringSection').style.display = 'none';
                document.getElementById('recordingIndicator').style.display = 'none';

                // Clear session data
                localStorage.removeItem('proctoringSession');

                this.showNotification('Exam session ended successfully!', 'success');
            }
        } catch (error) {
            console.error('Error ending exam:', error);
            this.showNotification('Error ending exam session.', 'danger');
        }
    }

    downloadReport() {
        window.open('/download-report', '_blank');
    }
}

// Initialize the proctoring system when the page loads
let proctoringSystem;

document.addEventListener('DOMContentLoaded', () => {
    proctoringSystem = new ProctoringSystem();
});

// Global functions for HTML onclick events
function startExam() {
    proctoringSystem.startExam();
}

function endExam() {
    proctoringSystem.endExam();
}

function downloadReport() {
    proctoringSystem.downloadReport();
}

// Legacy function for compatibility
function loadExam() {
    startExam();
}
