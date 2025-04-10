from flask import Flask, Response
from picamera2 import Picamera2
import cv2
import time

app = Flask(__name__)

# Initialiser la caméra
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())
picam2.start()
time.sleep(1)  # Laisse le temps à la caméra de chauffer

def get_jpeg_frame():
    frame = picam2.capture_array()
    _, jpeg = cv2.imencode('.jpg', frame)
    return jpeg.tobytes()

@app.route('/frame')
def stream_image():
    image = get_jpeg_frame()
    return Response(image, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
