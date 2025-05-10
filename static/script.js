const video = document.getElementById('webcam');
const examFrame = document.getElementById('examFrame');
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => { video.srcObject = stream })
    .catch(err => {
        alert("Webcam access denied");
        logViolation("webcam_off", "User blocked or disabled the camera");
    });

function verifyFace() {
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    canvas.toBlob(blob => {
        const formData = new FormData();
        formData.append('image', blob);
        fetch('/verify-face', { method: 'POST', body: formData })
            .then(res => res.json())
            .then(data => {
                document.getElementById('status').textContent = JSON.stringify(data);
                if (data.status !== 'verified') logViolation(data.status, 'Face verification failed');
            });
    });
}

function loadExam() {
    const url = document.getElementById('examUrl').value;
    if (url) {
        examFrame.src = url;
        examFrame.style.display = 'block';
        verifyFace();
    }
}

document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
        logViolation("tab_switch", "User left the exam tab");
    }
});

function logViolation(type, details) {
    fetch('/log-violation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type, details })
    });
}
