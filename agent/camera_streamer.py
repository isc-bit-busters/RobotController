import cv2
import base64
import time
import redis
import socket
from picamera2 import Picamera2

# Connexion à Redis (PC fixe)
redis_host = "192.168.88.249"
redis_port = 6379
redis_db = 0

r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

robot_id = socket.gethostname()

# Config caméra
picam2 = Picamera2()
video_config = picam2.create_video_configuration(main={"size": (320, 240)})
picam2.configure(video_config)
picam2.start()

try:
    while True:
        frame = picam2.capture_array("main")
        _, buffer = cv2.imencode('.jpg', frame)
        img_base64 = base64.b64encode(buffer).decode("utf-8")
        timestamp = time.time()
        timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))

        # Clé unique par image (ex: camera:robot1:timestamp)
        key = f"camera:{robot_id}:{int(timestamp * 1000)}"

        # Métadonnées
        data = {
            "timestamp": timestamp_str,
            "timestamp_epoch": timestamp,
            "robot_id": robot_id,
            "resolution": f"{frame.shape[1]}x{frame.shape[0]}",
            "format": "jpg",
            "image": img_base64
        }

        # Stockage permanent (ex: liste ou stream)
        r.hset(key, mapping=data)

        # Dernière image visible
        r.hset("camera:latest", mapping=data)

        print(f"📤 Image envoyée @ {timestamp_str}")

        time.sleep(0.5)

except KeyboardInterrupt:
    print("❌ Interruption")

finally:
    picam2.stop()
