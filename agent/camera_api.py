from flask import Flask, Response
from picamera2 import Picamera2
import cv2
import threading
import time
import subprocess

# === 🔁 Restart the camera system ===
subprocess.run(["sudo", "systemctl", "restart", "camera"], check=False)
# Optional: wait a bit to allow hardware to recover
time.sleep(1)

app = Flask(__name__)

# === Initialize the camera ===
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
picam2.start()

frame = None

# === Background thread to grab latest frame continuously ===
def update_frame():
    global frame
    while True:
        frame = picam2.capture_array()
        time.sleep(0.03)

threading.Thread(target=update_frame, daemon=True).start()

# === MJPEG Stream endpoint ===
@app.route('/video_feed')
def video_feed():
    def generate():
        while True:
            if frame is not None:
                modified = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                _, jpeg = cv2.imencode('.jpg', modified)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
            time.sleep(0.03)
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

# === Run server ===
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
