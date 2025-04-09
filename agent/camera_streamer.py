# agent/camera_streamer.py

import cv2
import base64
import json
import time
import redis
from datetime import datetime
from picamera2 import Picamera2

# Connexion Redis (vers ton PC)
r = redis.Redis(host="192.168.88.249", port=6379)

# Initialisation Picamera2
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(
    main={"size": (320, 240), "format": "XBGR8888"},
    buffer_count=2
))
picam2.start()

try:
    while True:
        frame = picam2.capture_array("main")
        _, buffer = cv2.imencode('.jpg', frame)
        encoded = base64.b64encode(buffer).decode("utf-8")
        timestamp = datetime.now().isoformat()

        # Format JSON
        payload = {
            "timestamp": timestamp,
            "image": encoded
        }

        # Envoi dans Redis (liste `robot:frames`)
        r.lpush("robot:frames", json.dumps(payload))

        time.sleep(0.2)

except KeyboardInterrupt:
    picam2.stop()
