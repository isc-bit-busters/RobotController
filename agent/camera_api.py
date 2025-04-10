from flask import Flask, Response
from picamera2 import Picamera2, Preview
import cv2
import threading
import time

app = Flask(__name__)
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
picam2.start()

frame = None

# Continuously update the latest frame
def update_frame():
    global frame
    while True:
        frame = picam2.capture_array()
        time.sleep(0.03)  # ~30 FPS

threading.Thread(target=update_frame, daemon=True).start()

@app.route('/frame')
def stream_frame():
    global frame
    if frame is not None:
        _, jpeg = cv2.imencode('.jpg', frame)
        return Response(jpeg.tobytes(), mimetype='image/jpeg')
    return Response(status=503)

@app.route('/video_feed')
def video_feed():
    def generate():
        while True:
            frame = picam2.capture_array()
            _, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
