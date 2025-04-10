import cv2
import base64
import time
import redis
from picamera2 import Picamera2

# Connexion à Redis (PC à IP fixe)
redis_host = "192.168.88.249"
redis_port = 6379
redis_db = 0

r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (320, 240)}))
picam2.start()

try:
    while True:
        frame = picam2.capture_array("main")
        _, buffer = cv2.imencode('.jpg', frame)
        img_base64 = base64.b64encode(buffer).decode("utf-8")
        timestamp = time.time()
        r.hset("camera:latest", mapping={
            "timestamp": timestamp,
            "image": img_base64
        })
        print(f"📤 Frame sent at {timestamp}")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("❌ Interrupted")

finally:
    picam2.stop()
