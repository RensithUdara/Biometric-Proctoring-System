from flask import Flask, render_template, request, jsonify, send_file
import face_recognition
import numpy as np
import cv2
import os
from flask_cors import CORS
import datetime
import json
from fpdf import FPDF

app = Flask(__name__)
CORS(app)

KNOWN_FACES_DIR = 'models/known_faces'
REPORTS_FILE = 'reports/violations.json'
PDF_REPORT_PATH = 'reports/violation_report.pdf'
known_face_encodings = []
known_face_names = []

# Load known face encodings
for filename in os.listdir(KNOWN_FACES_DIR):
    img = face_recognition.load_image_file(f"{KNOWN_FACES_DIR}/{filename}")
    encoding = face_recognition.face_encodings(img)[0]
    known_face_encodings.append(encoding)
    known_face_names.append(filename.split('.')[0])

@app.route('/')
def index():
    return render_template('index.html')

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
