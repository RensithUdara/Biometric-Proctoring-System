from flask import Flask, render_template, request, jsonify
import face_recognition
import numpy as np
import cv2
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

KNOWN_FACES_DIR = 'models/known_faces'
known_face_encodings = []
known_face_names = []

# Load known face encodings at startup
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
        return jsonify({"status": "no_face"})

    match = face_recognition.compare_faces(known_face_encodings, faces[0])
    if True in match:
        return jsonify({"status": "verified", "name": known_face_names[match.index(True)]})
    else:
        return jsonify({"status": "unverified"})

if __name__ == '__main__':
    app.run(debug=True)
