import cv2
import base64
import asyncio
import redis
import datetime
import os
from threading import Thread
from picamera2 import Picamera2

class CameraStreamer:
    def __init__(self, redis_host="localhost", redis_port=6379, robot_id="robot1", camera_index=0):
        self.redis = redis.Redis(host=redis_host, port=redis_port)
        self.robot_id = robot_id
        self.picam2 = Picamera2(camera_num=camera_index)
        self.picam2.configure(self.picam2.create_video_configuration(
            main={"size": (320, 240), "format": "XBGR8888"},
            buffer_count=2
        ))
        self.picam2.start()
        self.running = True

    def send_loop(self):
        while self.running:
            frame = self.picam2.capture_array("main")
            _, buffer = cv2.imencode('.jpg', frame)
            encoded = base64.b64encode(buffer).decode()

            now = datetime.datetime.utcnow().isoformat()
            key = f"{self.robot_id}:{now}"

            self.redis.set(key, encoded)
            print(f"[INFO] Image sent at {now}")
            asyncio.sleep(0.2)

    def stop(self):
        self.running = False
        self.picam2.stop()

def start_streamer():
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = int(os.getenv("REDIS_PORT", "6379"))
    robot_id = os.getenv("ROBOT_ID", "robot1")

    streamer = CameraStreamer(redis_host, redis_port, robot_id)
    try:
        streamer.send_loop()
    except KeyboardInterrupt:
        streamer.stop()

if __name__ == "__main__":
    start_streamer()
