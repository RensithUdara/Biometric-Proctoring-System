const video = document.getElementById('webcam');
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => { video.srcObject = stream })
  .catch(err => console.error('Camera error:', err));

function verifyFace() {
  const canvas = document.createElement('canvas');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext('2d').drawImage(video, 0, 0);
  canvas.toBlob(blob => {
    const formData = new FormData();
    formData.append('image', blob);

    fetch('/verify-face', {
      method: 'POST',
      body: formData
    })
      .then(res => res.json())
      .then(data => {
        document.getElementById('status').textContent = JSON.stringify(data);
      });
  });
}

// Tab switch detection
let hidden;
if (typeof document.hidden !== "undefined") {
  hidden = "hidden";
}

document.addEventListener("visibilitychange", () => {
  if (document[hidden]) alert("You switched tabs during the exam. This may be flagged.");
});
