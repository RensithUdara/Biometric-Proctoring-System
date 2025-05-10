from flask import Flask, render_template, request, jsonify
import face_recognition
import numpy as np
import cv2
import os
from flask_cors import CORS
import datetime
import json

app = Flask(__name__)
CORS(app)

KNOWN_FACES_DIR = 'models/known_faces'
REPORTS_FILE = 'reports/violations.json'
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

if __name__ == '__main__':
    app.run(debug=True)
