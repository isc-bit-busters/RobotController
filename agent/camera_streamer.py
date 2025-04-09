# =========================
# 📦 Fichier : agent/camera_streamer.py
# =========================

import cv2
import base64
import asyncio
from threading import Thread
from picamera2 import Picamera2
from slixmpp import ClientXMPP

class CameraBot(ClientXMPP):
    def __init__(self, jid, password, recipient, robot_id, camera_index=0):
        super().__init__(jid, password)
        self.recipient = recipient
        self.robot_id = robot_id
        self.running = True

        self.picam2 = Picamera2(camera_num=camera_index)
        self.picam2.configure(self.picam2.create_video_configuration(
            main={"size": (320, 240), "format": "XBGR8888"},
            buffer_count=2
        ))
        self.picam2.start(show_preview=False)

        self.add_event_handler("session_start", self.start)

    async def send_frame(self):
        while self.running:
            frame = self.picam2.capture_array("main")
            _, buffer = cv2.imencode('.jpg', frame)
            img_base64 = base64.b64encode(buffer).decode()
            msg = self.make_message(mto=self.recipient, mbody=img_base64, mtype='chat')
            msg['subject'] = self.robot_id
            msg.send()
            await asyncio.sleep(0.2)

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        await self.send_frame()

    def stop(self):
        self.running = False
        self.picam2.stop()
        self.disconnect()

def start_camera_thread():
    import os
    def worker():
        robot_id = os.environ.get("ROBOT_ID", "robot1")
        bot = CameraBot(
            jid=f"{robot_id}@prosody",
            password=os.environ.get("XMPP_PASSWORD", "robotpassword"),
            recipient="dashboard@prosody",
            robot_id=robot_id
        )
        bot.connect()
        bot.process()

    t = Thread(target=worker, daemon=True)
    t.start()