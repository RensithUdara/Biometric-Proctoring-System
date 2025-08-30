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

        if not faces:
            log_violation_db("no_face", "No face detected", 3)
            return jsonify({"status": "no_face", "face_count": 0})

        # Check for multiple faces
        if len(faces) > 1:
            log_violation_db("multiple_faces", f"Multiple faces detected: {len(faces)}", 4, 
                           base64.b64encode(cv2.imencode('.jpg', img)[1]).decode())
            return jsonify({"status": "multiple_faces", "face_count": len(faces)})

        # Verify the single face
        if known_face_encodings:
            face_distances = face_recognition.face_distance(known_face_encodings, faces[0])
            best_match_index = np.argmin(face_distances)
            
            if face_distances[best_match_index] < 0.6:  # Threshold for face recognition
                confidence = (1 - face_distances[best_match_index]) * 100
                return jsonify({
                    "status": "verified", 
                    "name": known_face_names[best_match_index],
                    "confidence": round(confidence, 2),
                    "face_count": 1
                })
        
        log_violation_db("unverified", "Face did not match any registered user", 4,
                        base64.b64encode(cv2.imencode('.jpg', img)[1]).decode())
        return jsonify({"status": "unverified", "face_count": 1})
        
    except Exception as e:
        print(f"Error in face verification: {e}")
        return jsonify({"status": "error", "message": str(e)})

@app.route('/analyze-attention', methods=['POST'])
def analyze_attention():
    try:
        file = request.files['image']
        npimg = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        
        if img is None:
            return jsonify({"status": "error", "message": "Invalid image"})

        # Convert to grayscale for eye detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Load eye cascade classifier
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(eyes) < 2:
            log_violation_db("eyes_not_detected", "Eyes not properly detected - possible looking away", 2)
            return jsonify({"status": "attention_warning", "eyes_detected": len(eyes)})
        
        return jsonify({"status": "attentive", "eyes_detected": len(eyes)})
        
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
    app.run(debug=True)
