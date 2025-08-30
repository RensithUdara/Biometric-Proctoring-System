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
    file = request.files['image']
    npimg = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    faces = face_recognition.face_encodings(rgb_img)

    if not faces:
        log_violation("no_face", "No face detected")
        return jsonify({"status": "no_face"})

    match = face_recognition.compare_faces(known_face_encodings, faces[0])
    if True in match:
        return jsonify({"status": "verified", "name": known_face_names[match.index(True)]})
    else:
        log_violation("unverified", "Face did not match any registered user")
        return jsonify({"status": "unverified"})

@app.route('/log-violation', methods=['POST'])
def log_violation_endpoint():
    data = request.get_json()
    violation_type = data.get('type')
    details = data.get('details')
    log_violation(violation_type, details)
    return jsonify({"status": "logged"})

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

def create_pdf_report():
    try:
        with open(REPORTS_FILE, 'r') as f:
            logs = json.load(f)
    except:
        logs = []
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Proctoring Violation Report", ln=True, align='C')
    pdf.ln(10)
    for log in logs:
        line = f"{log['timestamp']} | {log['type']} | {log['details']}"
        pdf.multi_cell(0, 10, txt=line)
    os.makedirs(os.path.dirname(PDF_REPORT_PATH), exist_ok=True)
    pdf.output(PDF_REPORT_PATH)

if __name__ == '__main__':
    app.run(debug=True)
