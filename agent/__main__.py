import base64
import datetime
import math
from spade.agent import Agent
from spade.behaviour import TimeoutBehaviour, OneShotBehaviour, CyclicBehaviour
from spade.message import Message
from spade.template import Template
import asyncio
import os
import time
import logging
import asyncio
import numpy as np
import cv2
import uuid
from camera_api import CameraHandler
import vision

from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
from agent.alphabotlib.AlphaBot2 import AlphaBot2
from agent.alphabotlib.test import detectAruco, get_walls
from agent.nav_utils import generate_navmesh, find_path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AlphaBotAgent")

# Enable SPADE and XMPP-specific logging
for log_name in ["spade", "aioxmpp", "xmpp"]:
    log = logging.getLogger(log_name)
    log.setLevel(logging.INFO)
    log.propagate = True

IMAGE_INTERVAL_MS = 500 
IMAGE_OFFSET_MS = IMAGE_INTERVAL_MS / 2

class AlphaBotAgent(Agent):
    def __init__(self, jid, password, verify_security=True, name=None):
        super().__init__(jid=jid, password=password, verify_security=verify_security)
        self.alphabot = AlphaBot2()
        self.robot_name = name
        self.other_agent = "mael" if name == "gerald" else "gerald"

    class RequestImageBehaviour(TimeoutBehaviour):
        async def run(self):
            msg = Message(to="camera_agent@prosody") 
            msg.body = "request_image"
            now = datetime.datetime.now()

            logger.info(f"[Behavior] Requesting image at {now}...") 
            await self.send(msg)
            logger.info("[Behavior] Registration message sent.")

            delta = datetime.timedelta(milliseconds=IMAGE_INTERVAL_MS)
            request_image_behavior = self.agent.RequestImageBehaviour(start_at=now + delta)
            self.agent.add_behaviour(request_image_behavior)
    
    class ListenToImageBehaviour(CyclicBehaviour):
        async def run(self):
            robot_id = 7
            goal_id = 6

            logger.info("[Behavior] Listening for image messages...")
            msg = await self.receive(timeout=1)
            if msg and msg.body.startswith("image "):
                logger.info(f"[Behavior] Received image message from {msg.sender}")
                time_ms = asyncio.get_event_loop().time() * 1000
                logger.info(f"[Behavior] Message received at {time_ms} ms")

                if str(msg.sender).startswith("camera_agent@"):
                    # forward the message to the other robot
                    logger.info(f"[Behavior] Forwarding image to {self.agent.other_agent}...")
                    forward_msg = Message(to=f"{self.agent.other_agent}@prosody")
                    forward_msg.body = msg.body
                    await self.send(forward_msg)
                    logger.info(f"[Behavior] Image forwarded to {self.agent.other_agent}.")

                encoded_img = msg.body.split("image ")[1].strip()

                logger.info("[Behavior] Decoding image..." )
                decoded_img = base64.b64decode(encoded_img)
                logger.info("[Behavior] Image decoded.")

                img = cv2.imdecode(np.frombuffer(decoded_img, np.uint8), cv2.IMREAD_COLOR)
                logger.info("[Behavior] Image decoded successfully.")

                arucos = detectAruco(img)
                print(f"Detected Arucos: {arucos}")
                if robot_id not in arucos:
                    logger.warning("[] Robot ID not found in image.")
                pos1 = arucos[robot_id]
                pos2 = arucos[goal_id]
                
                logger.info(f"[] going from {pos1} to {pos2}")

                path = find_path((pos1["x"], 0, pos1["y"]), (pos2["x"], 0, pos2["y"]), *self.agent.navmesh)

                if path is not None:
                    logger.info(f"[Behavior] Path found: {path}")
                else:
                    logger.warning("[Behavior] No path found.")
                    

            else:
                logger.debug("[Behavior] Message received but not an image.")

    class PingBehaviour(OneShotBehaviour):
        def __init__(self, to, **kwargs):
            super().__init__(**kwargs)
            self.to = to # waf

        async def run(self):
            msg = Message(to=self.to) 
            msg.body = "ping"
            logger.info("[Behavior] Sending ping to camera agent...")
            await self.send(msg)

            reply = await self.receive(timeout=30)
            if reply:
                logger.info(f"[Behavior] Received ping reply from {msg.sender}")
            else:
                logger.debug("[Behavior] No ping reply received during timeout.")

    class PongBehaviour(OneShotBehaviour):
        async def run(self):
            while True:
                msg = await self.receive(timeout=30)
                if msg:
                    if msg.body != "ping":
                        continue

                    logger.info(f"[Behavior] Received ping from {msg.sender}")
                    reply = Message(to=str(msg.sender))
                    reply.body = "pong"
                    logger.info("[Behavior] Sending pong reply...")
                    await self.send(reply)
                else:
                    logger.debug("[Behavior] No ping message received during timeout.")

    class InitBehaviour(OneShotBehaviour):
        async def run(self):
            robot_id = 7

            logger.info("[Step 0] Requesting initial image...")
            msg = Message(to="camera_agent@prosody", body="request_image")
            await self.send(msg)

            reply = await self.receive(timeout=10)
            if not reply or not reply.body.startswith("image "):
                logger.warning("[Step 0] No image received.")
                return

            encoded_img = reply.body.split("image ")[1].strip()
            # print(encoded_img)
            img0 = cv2.imdecode(np.frombuffer(base64.b64decode(encoded_img), np.uint8), cv2.IMREAD_COLOR)

            # === STEP 0: Generate NavMesh ===
            logger.info("[Step 0] Generating NavMesh...")
            walls = get_walls(img0)

            logger.info(f"[Step 0] Detected walls: {walls}")
                
            vertices, polygons = generate_navmesh(walls)

            logger.info(f"[Step 0] NavMesh vertices: {vertices}")
            logger.info(f"[Step 0] NavMesh polygons: {polygons}")

            self.agent.navmesh = (vertices, polygons)

            detected_bot = False
            while not detected_bot:
                await asyncio.sleep(2)

                # === STEP 1: Take the first image ===
                logger.info("[Step 1] Requesting initial image...")
                msg = Message(to="camera_agent@prosody", body="request_image")
                await self.send(msg)

                reply = await self.receive(timeout=10)
                if not reply or not reply.body.startswith("image "):
                    logger.warning("[Step 1] No image received.")
                    return

                encoded_img = reply.body.split("image ")[1].strip()
                # print(encoded_img)
                img1 = cv2.imdecode(np.frombuffer(base64.b64decode(encoded_img), np.uint8), cv2.IMREAD_COLOR)
                arucos1 = detectAruco(img1)
                print(f"Detected Arucos: {arucos1}")
                if robot_id not in arucos1:
                    logger.warning("[Step 1] Robot ID not found in initial image.")
                    continue

                pos1 = arucos1[robot_id]
                logger.info(f"[Step 1] Robot initial position: {pos1}")

                detected_bot = True
            

            await asyncio.sleep(2)

            t = 2  # seconds
            # === STEP 2: Move the robot ===
            logger.info("[Step 2] Moving robot forward...")
            self.agent.alphabot.advance(t)  # Move for 2 seconds
            await asyncio.sleep(t)

            # === STEP 3: Take the second image ===
            logger.info("[Step 3] Requesting image after movement...")
            msg2 = Message(to="camera_agent@prosody", body="request_image")
            await self.send(msg2)

            reply2 = await self.receive(timeout=10)
            if not reply2 or not reply2.body.startswith("image "):
                logger.warning("[Step 3] No image received after move.")

            encoded_img2 = reply2.body.split("image ")[1].strip()
            img2 = cv2.imdecode(np.frombuffer(base64.b64decode(encoded_img2), np.uint8), cv2.IMREAD_COLOR)
            arucos2 = detectAruco(img2)
            if robot_id not in arucos2:
                logger.warning("[Step 3] Robot ID not found in second image.")

            pos2 = arucos2[robot_id]
            logger.info(f"[Step 3] Robot new position: {pos2}")

            # === STEP 4: Compute distance ===
            dist = np.sqrt(
                (pos2["x"] - pos1["x"]) ** 2 + (pos2["y"] - pos1["y"]) ** 2
            )
            
            logger.info(f"[Step 4] Distance moved: {dist}")
            speed = dist / t
            self.agent.alphabot.setSpeed(speed)
            logger.info(f"[Step 4] Speed: {speed} units/s")

            

        async def on_end(self):
            logger.info("[Behavior] MoveAndMeasureBehaviour ended.")

            # gerald requests images on x.0 and x.5 sec, mael on x.25 and x.75 sec 
            now = datetime.datetime.now()
            staggered_start_time = now + datetime.timedelta(milliseconds=IMAGE_OFFSET_MS if self.agent.robot_name == "mael" else 0)

            logger.info(f"[Agent] Staggered start time: {staggered_start_time}")

            request_image_behavior = self.agent.RequestImageBehaviour(start_at=staggered_start_time)
            self.agent.add_behaviour(request_image_behavior)

            listen_to_image_behavior = self.agent.ListenToImageBehaviour()
            self.agent.add_behaviour(listen_to_image_behavior)
        
            # ping_behavior = self.PingBehaviour(to=f"{self.other_agent}@prosody")
            # self.add_behaviour(ping_behavior)
            
            # pong_behavior = self.PongBehaviour()
            # self.add_behaviour(pong_behavior)
            

    async def setup(self):
        logger.info(f"[Agent] AlphaBotAgent {self.jid} starting setup...")
        logger.info(f"[Agent] Will connect as {self.jid} to server {os.environ.get('XMPP_SERVER', 'prosody')}")
        
        logger.info(f"[Agent] AlphaBotAgent {self.jid} setup starting...")
       
        self.add_behaviour(self.InitBehaviour())
        logger.info("[Agent] Behaviors added, setup complete.") 


    async def stop(self):
        logger.info(f"[Agent] Stopping AlphaBotAgent {self.jid}")
        await super().stop()
        logger.info("[Agent] Stopped.")

# === MAIN ===
async def main():
    xmpp_domain = os.environ.get("XMPP_DOMAIN", "prosody")
    xmpp_username = os.environ.get("XMPP_USERNAME")
    if not xmpp_username:
        logger.error("XMPP_USERNAME environment variable is not set.")
        return 
    
    ##Test camera api
    camera_api = CameraHandler()
    camera_api.initialize_camera()
    image=camera_api.capture_image()
    
    #Vision
    model=vision.load_model('yolov5n.onnx')
    calib=vision.load_calibration('camera_calibration.npz')
    frame=vision.preprocess_image(image)
    
    #Detection
    results=vision.detect_objects(model,frame,calib)
    print(results)
    
         

    xmpp_jid = f"{xmpp_username}@{xmpp_domain}"
    xmpp_password = os.environ.get("XMPP_PASSWORD", "top_secret")

    logger.info("Starting AlphaBot XMPP Agent...")
    logger.info(f"XMPP JID: {xmpp_jid}")

    try:
        agent = AlphaBotAgent(
            jid=xmpp_jid, 
            password=xmpp_password,
            verify_security=False,
            name = xmpp_username
        )
        
        logger.info("Agent created, attempting to start...")
        await agent.start(auto_register=True)
        logger.info("Agent started successfully!")

        while agent.is_alive():
            await asyncio.sleep(10)

    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received. Stopping agent...")
        await agent.stop()
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.critical(f"Critical error in main loop: {str(e)}", exc_info=True)
