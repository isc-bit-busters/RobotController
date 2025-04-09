import cv2
import base64
import time
import redis
from picamera2 import Picamera2

# Connexion à Redis sur le PC
r = redis.Redis(host="192.168.88.249", port=6379)

# Initialiser la caméra
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

        # Envoie l'image encodée dans une liste Redis (clé = "robot:frames")
        r.lpush("robot:frames", encoded)

        time.sleep(0.2)
except KeyboardInterrupt:
    picam2.stop()
