from flask import Flask, render_template, request, jsonify, send_file, session
import face_recognition
import numpy as np
import cv2
import os
from flask_cors import CORS
import datetime
import json
from fpdf import FPDF
import sqlite3
import base64
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import threading
import time
import logging
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import io

app = Flask(__name__)
CORS(app)
app.secret_key = secrets.token_hex(16)

KNOWN_FACES_DIR = 'models/known_faces'
REPORTS_FILE = 'reports/violations.json'
PDF_REPORT_PATH = 'reports/violation_report.pdf'
DATABASE_PATH = 'reports/proctoring.db'
known_face_encodings = []
known_face_names = []

# Initialize database
def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE,
            student_name TEXT,
            exam_name TEXT,
            start_time TIMESTAMP,
            end_time TIMESTAMP,
            status TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS violations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            timestamp TIMESTAMP,
            violation_type TEXT,
            details TEXT,
            severity INTEGER,
            image_data TEXT,
            FOREIGN KEY (session_id) REFERENCES sessions (session_id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# Load known face encodings
def load_known_faces():
    global known_face_encodings, known_face_names
    known_face_encodings = []
    known_face_names = []
    
    if not os.path.exists(KNOWN_FACES_DIR):
        os.makedirs(KNOWN_FACES_DIR)
        return
        
    for filename in os.listdir(KNOWN_FACES_DIR):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            try:
                img_path = os.path.join(KNOWN_FACES_DIR, filename)
                img = face_recognition.load_image_file(img_path)
                encodings = face_recognition.face_encodings(img)
                
                if encodings:
                    known_face_encodings.append(encodings[0])
                    known_face_names.append(os.path.splitext(filename)[0])
                else:
                    print(f"No face found in {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

# Enhanced object detection function
def detect_suspicious_objects(img):
    """Detect phones, books, and other potentially suspicious objects"""
    suspicious_objects = []
    
    # Convert to grayscale for object detection
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Load cascade classifiers for objects
    try:
        # Phone detection (simplified - you'd need a trained model for better accuracy)
        phone_cascade = cv2.CascadeClassifier('models/phone_cascade.xml')
        if os.path.exists('models/phone_cascade.xml'):
            phones = phone_cascade.detectMultiScale(gray, 1.1, 4)
            if len(phones) > 0:
                suspicious_objects.append(f"Phone detected ({len(phones)} instances)")
    except:
        pass
    
    # Simple edge detection to identify rectangular objects (books, papers)
    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    book_like_objects = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 5000:  # Filter small objects
            # Check if the contour is rectangular
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            if len(approx) == 4:
                book_like_objects += 1
    
    if book_like_objects > 2:  # More than 2 rectangular objects might indicate books/papers
        suspicious_objects.append(f"Rectangular objects detected ({book_like_objects} instances)")
    
    return suspicious_objects

# Enhanced attention analysis
def analyze_gaze_direction(img):
    """Analyze if the person is looking at the screen"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Load face and eye cascade classifiers
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    
    if len(faces) == 0:
        return {"status": "no_face", "details": "No face detected for gaze analysis"}
    
    attention_score = 0
    gaze_details = []
    
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 5)
        
        if len(eyes) >= 2:
            attention_score += 50  # Base score for detecting both eyes
            
            # Analyze eye positions (simplified)
            eye_positions = [(ex + ew//2, ey + eh//2) for (ex, ey, ew, eh) in eyes[:2]]
            
            # Check if eyes are looking forward (very basic check)
            if len(eye_positions) == 2:
                eye_distance = abs(eye_positions[0][0] - eye_positions[1][0])
                if 30 < eye_distance < 80:  # Eyes are properly spaced
                    attention_score += 30
                    gaze_details.append("Eyes properly positioned")
        elif len(eyes) == 1:
            attention_score += 20
            gaze_details.append("Only one eye visible")
        else:
            gaze_details.append("Eyes not clearly visible")
    
    if attention_score >= 70:
        return {"status": "focused", "score": attention_score, "details": gaze_details}
    elif attention_score >= 40:
        return {"status": "partially_focused", "score": attention_score, "details": gaze_details}
    else:
        return {"status": "distracted", "score": attention_score, "details": gaze_details}

# Load faces on startup
load_known_faces()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-session', methods=['POST'])
def start_session():
    data = request.get_json()
    session_id = secrets.token_urlsafe(16)
    student_name = data.get('student_name', 'Unknown')
    exam_name = data.get('exam_name', 'Exam')
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sessions (session_id, student_name, exam_name, start_time, status)
        VALUES (?, ?, ?, ?, 'active')
    ''', (session_id, student_name, exam_name, datetime.datetime.now()))
    conn.commit()
    conn.close()
    
    session['session_id'] = session_id
    session['student_name'] = student_name
    
    return jsonify({"status": "success", "session_id": session_id})

@app.route('/end-session', methods=['POST'])
def end_session():
    session_id = session.get('session_id')
    if not session_id:
        return jsonify({"status": "error", "message": "No active session"})
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE sessions SET end_time = ?, status = 'completed'
        WHERE session_id = ?
    ''', (datetime.datetime.now(), session_id))
    conn.commit()
    conn.close()
    
    session.clear()
    return jsonify({"status": "success"})

@app.route('/verify-face', methods=['POST'])
def verify_face():
    try:
        file = request.files['image']
        npimg = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({"status": "error", "message": "Invalid image"})

        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_img)
        faces = face_recognition.face_encodings(rgb_img, face_locations)

        # Enhanced analysis
        analysis_results = {
            "face_count": len(faces),
            "suspicious_objects": detect_suspicious_objects(img),
            "gaze_analysis": analyze_gaze_direction(img) if len(faces) == 1 else None,
            "image_quality": assess_image_quality(img)
        }

        if not faces:
            log_violation_db("no_face", "No face detected", 3, 
                           base64.b64encode(cv2.imencode('.jpg', img)[1]).decode())
            return jsonify({"status": "no_face", "face_count": 0, "analysis": analysis_results})

        # Check for multiple faces
        if len(faces) > 1:
            log_violation_db("multiple_faces", f"Multiple faces detected: {len(faces)}", 4, 
                           base64.b64encode(cv2.imencode('.jpg', img)[1]).decode())
            return jsonify({"status": "multiple_faces", "face_count": len(faces), "analysis": analysis_results})

        # Verify the single face
        if known_face_encodings:
            face_distances = face_recognition.face_distance(known_face_encodings, faces[0])
            best_match_index = np.argmin(face_distances)
            
            if face_distances[best_match_index] < 0.6:  # Threshold for face recognition
                confidence = (1 - face_distances[best_match_index]) * 100
                
                # Log suspicious objects if detected
                if analysis_results["suspicious_objects"]:
                    for obj in analysis_results["suspicious_objects"]:
                        log_violation_db("suspicious_object", obj, 3)
                
                return jsonify({
                    "status": "verified", 
                    "name": known_face_names[best_match_index],
                    "confidence": round(confidence, 2),
                    "face_count": 1,
                    "analysis": analysis_results
                })
        
        log_violation_db("unverified", "Face did not match any registered user", 4,
                        base64.b64encode(cv2.imencode('.jpg', img)[1]).decode())
        return jsonify({"status": "unverified", "face_count": 1, "analysis": analysis_results})
        
    except Exception as e:
        print(f"Error in face verification: {e}")
        return jsonify({"status": "error", "message": str(e)})

def assess_image_quality(img):
    """Assess the quality of the captured image"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Calculate brightness
    brightness = np.mean(gray)
    
    # Calculate sharpness using Laplacian variance
    sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    quality_score = 0
    issues = []
    
    if brightness < 50:
        issues.append("Image too dark")
    elif brightness > 200:
        issues.append("Image too bright")
    else:
        quality_score += 30
    
    if sharpness < 100:
        issues.append("Image blurry")
    else:
        quality_score += 40
    
    # Check image size
    height, width = gray.shape
    if width < 640 or height < 480:
        issues.append("Image resolution too low")
    else:
        quality_score += 30
    
    return {
        "score": quality_score,
        "brightness": round(brightness, 1),
        "sharpness": round(sharpness, 1),
        "issues": issues
    }

@app.route('/analyze-attention', methods=['POST'])
def analyze_attention():
    try:
        file = request.files['image']
        npimg = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        
        if img is None:
            return jsonify({"status": "error", "message": "Invalid image"})

        # Use enhanced gaze analysis
        gaze_result = analyze_gaze_direction(img)
        
        # Traditional eye detection as fallback
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
        
        combined_analysis = {
            "eyes_detected": len(eyes),
            "gaze_analysis": gaze_result,
            "attention_score": gaze_result.get("score", 0)
        }
        
        # Determine overall attention status
        if gaze_result["status"] == "focused":
            status = "attentive"
        elif gaze_result["status"] == "partially_focused":
            status = "attention_warning"
            log_violation_db("partial_attention", f"Partial attention detected - Score: {gaze_result.get('score', 0)}", 2)
        else:
            status = "distracted"
            log_violation_db("distracted", f"Student appears distracted - Score: {gaze_result.get('score', 0)}", 3)
        
        return jsonify({
            "status": status, 
            "analysis": combined_analysis,
            "details": gaze_result.get("details", [])
        })
        
    except Exception as e:
        print(f"Error in attention analysis: {e}")
        return jsonify({"status": "error", "message": str(e)})

@app.route('/log-violation', methods=['POST'])
def log_violation_endpoint():
    data = request.get_json()
    violation_type = data.get('type')
    details = data.get('details')
    severity = data.get('severity', 1)
    log_violation(violation_type, details)
    log_violation_db(violation_type, details, severity)
    return jsonify({"status": "logged"})

@app.route('/get-violations')
def get_violations():
    session_id = session.get('session_id')
    if not session_id:
        return jsonify({"violations": []})
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT timestamp, violation_type, details, severity
        FROM violations
        WHERE session_id = ?
        ORDER BY timestamp DESC
        LIMIT 50
    ''', (session_id,))
    
    violations = []
    for row in cursor.fetchall():
        violations.append({
            'timestamp': row[0],
            'type': row[1],
            'details': row[2],
            'severity': row[3]
        })
    
    conn.close()
    return jsonify({"violations": violations})

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/download-report')
def download_report():
    create_pdf_report()
    return send_file(PDF_REPORT_PATH, as_attachment=True)

def log_violation(violation_type, details):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log = {"timestamp": timestamp, "type": violation_type, "details": details}
    os.makedirs(os.path.dirname(REPORTS_FILE), exist_ok=True)
    try:
        with open(REPORTS_FILE, 'r') as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []
    logs.append(log)
    with open(REPORTS_FILE, 'w') as f:
        json.dump(logs, f, indent=2)

def log_violation_db(violation_type, details, severity=1, image_data=None):
    session_id = session.get('session_id', 'unknown')
    timestamp = datetime.datetime.now()
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO violations (session_id, timestamp, violation_type, details, severity, image_data)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (session_id, timestamp, violation_type, details, severity, image_data))
    conn.commit()
    conn.close()

def create_pdf_report():
    session_id = session.get('session_id')
    
    # Get data from database if session exists, otherwise use JSON file
    if session_id:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.student_name, s.exam_name, s.start_time, s.end_time,
                   v.timestamp, v.violation_type, v.details, v.severity
            FROM sessions s
            LEFT JOIN violations v ON s.session_id = v.session_id
            WHERE s.session_id = ?
            ORDER BY v.timestamp
        ''', (session_id,))
        data = cursor.fetchall()
        conn.close()
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="Proctoring Violation Report", ln=True, align='C')
        pdf.ln(10)
        
        if data:
            student_name = data[0][0] or 'Unknown'
            exam_name = data[0][1] or 'Unknown Exam'
            start_time = data[0][2]
            end_time = data[0][3] or 'Ongoing'
            
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(200, 10, txt=f"Student: {student_name}", ln=True)
            pdf.cell(200, 10, txt=f"Exam: {exam_name}", ln=True)
            pdf.cell(200, 10, txt=f"Start Time: {start_time}", ln=True)
            pdf.cell(200, 10, txt=f"End Time: {end_time}", ln=True)
            pdf.ln(10)
            
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(200, 10, txt="Violations:", ln=True)
            pdf.set_font("Arial", size=10)
            
            violation_count = 0
            for row in data:
                if row[4]:  # If timestamp exists (violation data)
                    violation_count += 1
                    severity_text = ["Low", "Medium", "High", "Critical"][min(row[7]-1, 3)]
                    line = f"{row[4]} | {row[5]} | {row[6]} | Severity: {severity_text}"
                    pdf.multi_cell(0, 8, txt=line)
            
            if violation_count == 0:
                pdf.cell(200, 10, txt="No violations recorded.", ln=True)
            else:
                pdf.ln(5)
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(200, 10, txt=f"Total Violations: {violation_count}", ln=True)
    else:
        # Fallback to JSON file
        try:
            with open(REPORTS_FILE, 'r') as f:
                logs = json.load(f)
        except:
            logs = []
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="Proctoring Violation Report", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", size=10)
        
        for log in logs:
            line = f"{log['timestamp']} | {log['type']} | {log['details']}"
            pdf.multi_cell(0, 8, txt=line)
    
    os.makedirs(os.path.dirname(PDF_REPORT_PATH), exist_ok=True)
    pdf.output(PDF_REPORT_PATH)

if __name__ == '__main__':
    # Load configuration
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            print("Configuration loaded successfully")
    except FileNotFoundError:
        print("Config file not found, using defaults")
        config = {}
    
    print("Starting Biometric Proctoring System...")
    print(f"Known faces loaded: {len(known_face_names)}")
    print(f"Database initialized: {DATABASE_PATH}")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

# Additional API endpoints for enhanced functionality
@app.route('/api/stats')
def get_stats():
    """Get system statistics"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Get total sessions
    cursor.execute('SELECT COUNT(*) FROM sessions')
    total_sessions = cursor.fetchone()[0]
    
    # Get active sessions
    cursor.execute('SELECT COUNT(*) FROM sessions WHERE status = "active"')
    active_sessions = cursor.fetchone()[0]
    
    # Get total violations
    cursor.execute('SELECT COUNT(*) FROM violations')
    total_violations = cursor.fetchone()[0]
    
    # Get violations by type
    cursor.execute('''
        SELECT violation_type, COUNT(*) 
        FROM violations 
        GROUP BY violation_type 
        ORDER BY COUNT(*) DESC
    ''')
    violations_by_type = dict(cursor.fetchall())
    
    conn.close()
    
    return jsonify({
        'total_sessions': total_sessions,
        'active_sessions': active_sessions,
        'total_violations': total_violations,
        'violations_by_type': violations_by_type,
        'known_faces': len(known_face_names)
    })

@app.route('/api/sessions')
def get_sessions():
    """Get all sessions with pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    offset = (page - 1) * per_page
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT s.session_id, s.student_name, s.exam_name, s.start_time, s.end_time, s.status,
               COUNT(v.id) as violation_count
        FROM sessions s
        LEFT JOIN violations v ON s.session_id = v.session_id
        GROUP BY s.session_id
        ORDER BY s.start_time DESC
        LIMIT ? OFFSET ?
    ''', (per_page, offset))
    
    sessions = []
    for row in cursor.fetchall():
        sessions.append({
            'session_id': row[0],
            'student_name': row[1],
            'exam_name': row[2],
            'start_time': row[3],
            'end_time': row[4],
            'status': row[5],
            'violation_count': row[6]
        })
    
    conn.close()
    return jsonify({'sessions': sessions})

@app.route('/api/upload-face', methods=['POST'])
def upload_face():
    """Upload a new known face"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    name = request.form.get('name', '').strip()
    
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        # Save the uploaded image
        filename = f"{name}.jpg"
        filepath = os.path.join(KNOWN_FACES_DIR, filename)
        file.save(filepath)
        
        # Reload known faces
        load_known_faces()
        
        return jsonify({'message': f'Face for {name} uploaded successfully'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/config')
def get_config():
    """Get current configuration"""
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        return jsonify(config)
    except:
        return jsonify({'error': 'Configuration not found'}), 404

@app.route('/api/config', methods=['POST'])
def update_config():
    """Update configuration"""
    try:
        config = request.get_json()
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=2)
        return jsonify({'message': 'Configuration updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics')
def get_analytics():
    """Get advanced analytics and charts"""
    try:
        session_id = session.get('session_id')
        if not session_id:
            return jsonify({"error": "No active session"}), 400

        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # Get violations over time
        cursor.execute('''
            SELECT DATE(timestamp) as date, COUNT(*) as count
            FROM violations 
            WHERE session_id = ?
            GROUP BY DATE(timestamp)
            ORDER BY date
        ''', (session_id,))
        violations_over_time = dict(cursor.fetchall())

        # Get violations by severity
        cursor.execute('''
            SELECT severity, COUNT(*) as count
            FROM violations 
            WHERE session_id = ?
            GROUP BY severity
        ''', (session_id,))
        violations_by_severity = dict(cursor.fetchall())

        # Get violations by type
        cursor.execute('''
            SELECT violation_type, COUNT(*) as count
            FROM violations 
            WHERE session_id = ?
            GROUP BY violation_type
            ORDER BY count DESC
            LIMIT 10
        ''', (session_id,))
        violations_by_type = dict(cursor.fetchall())

        conn.close()

        return jsonify({
            'violations_over_time': violations_over_time,
            'violations_by_severity': violations_by_severity,
            'violations_by_type': violations_by_type,
            'total_violations': sum(violations_by_severity.values())
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/session/<session_id>/violations')
def get_session_violations(session_id):
    """Get detailed violations for a specific session"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT timestamp, violation_type, details, severity, image_data
            FROM violations
            WHERE session_id = ?
            ORDER BY timestamp DESC
        ''', (session_id,))
        
        violations = []
        for row in cursor.fetchall():
            violations.append({
                'timestamp': row[0],
                'type': row[1],
                'details': row[2],
                'severity': row[3],
                'has_image': bool(row[4])
            })
        
        conn.close()
        return jsonify({'violations': violations})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/screenshot')
def take_screenshot():
    """Take a screenshot for monitoring purposes"""
    try:
        # This would require additional implementation for screen capture
        # For now, return a placeholder response
        timestamp = datetime.datetime.now().isoformat()
        log_violation_db("screenshot_taken", "Screenshot taken for monitoring", 1)
        return jsonify({
            'status': 'success',
            'timestamp': timestamp,
            'message': 'Screenshot captured'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    try:
        # Check database connection
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT 1')
        db_status = 'healthy'
        conn.close()
    except:
        db_status = 'error'
    
    return jsonify({
        'status': 'healthy',
        'database': db_status,
        'known_faces': len(known_face_names),
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.route('/api/export/<format>')
def export_data(format):
    """Export session data in various formats"""
    try:
        session_id = session.get('session_id')
        if not session_id:
            return jsonify({"error": "No active session"}), 400
        
        if format not in ['json', 'csv']:
            return jsonify({"error": "Unsupported format"}), 400
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Get session and violation data
        cursor.execute('''
            SELECT s.session_id, s.student_name, s.exam_name, s.start_time, s.end_time,
                   v.timestamp, v.violation_type, v.details, v.severity
            FROM sessions s
            LEFT JOIN violations v ON s.session_id = v.session_id
            WHERE s.session_id = ?
            ORDER BY v.timestamp
        ''', (session_id,))
        
        data = cursor.fetchall()
        conn.close()
        
        if format == 'json':
            export_data = []
            for row in data:
                export_data.append({
                    'session_id': row[0],
                    'student_name': row[1],
                    'exam_name': row[2],
                    'start_time': row[3],
                    'end_time': row[4],
                    'violation_timestamp': row[5],
                    'violation_type': row[6],
                    'violation_details': row[7],
                    'violation_severity': row[8]
                })
            
            response = jsonify(export_data)
            response.headers['Content-Disposition'] = f'attachment; filename=session_{session_id}.json'
            return response
            
        # CSV format would be implemented here
        return jsonify({"error": "CSV export not yet implemented"}), 501
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
