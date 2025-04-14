import base64
import os
import time
import logging
import asyncio
import numpy as np
import cv2
import uuid

from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
from agent.alphabotlib.AlphaBot2 import AlphaBot2
from agent.alphabotlib.test import detectAruco

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AlphaBotAgent")

# Enable SPADE and XMPP-specific logging
for log_name in ["spade", "aioxmpp", "xmpp"]:
    logging.getLogger(log_name).setLevel(logging.INFO)

class AlphaBotAgent(Agent):
    def __init__(self, jid, password, verify_security=True):
        super().__init__(jid=jid, password=password, verify_security=verify_security)
        self.alphabot = AlphaBot2()
    class RegisterToCameraAgentBehaviour(OneShotBehaviour):
        async def run(self):
            msg = Message(to="camera_agent@prosody") 
            msg.body = "register"
            
            logger.info("[Behavior] Registering to camera agent...")
            await self.send(msg)
            logger.info("[Behavior] Registration message sent.")

    class UnregisterFromCameraAgentBehaviour(OneShotBehaviour):
        async def run(self):
            msg = Message(to="camera_agent@prosody") 
            msg.body = "unregister"
            
            logger.info("[Behavior] Unregistering from camera agent...")
            await self.send(msg)
            logger.info("[Behavior] Unregistration message sent.")

    class ListenForImageBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=15)
            if msg and msg.body.startswith("image "):
                logger.info(f"[Behavior] Received image message from {msg.sender}")
                time_ms = asyncio.get_event_loop().time() * 1000
                logger.info(f"[Behavior] Message received at {time_ms} ms")

                encoded_img = msg.body.split("image ")[1].strip()

                logger.info("[Behavior] Decoding image..." )
                decoded_img = base64.b64decode(encoded_img)
                logger.info("[Behavior] Image decoded.")
            else:
                logger.debug("[Behavior] No message received during timeout.")

    class MoveAndMeasureBehaviour(OneShotBehaviour):
        async def run(self):
            robot_id = 7

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

            pos1 = arucos1[robot_id]
            logger.info(f"[Step 1] Robot initial position: {pos1}")

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
            speed = dist /t
            logger.info(f"[Step 4] Speed: {speed} units/s")
            

    async def setup(self):
        logger.info(f"[Agent] AlphaBotAgent {self.jid} setup starting...")
       
        self.add_behaviour(self.MoveAndMeasureBehaviour())
        logger.info("[Agent] Setup complete. Behaviour added.")
        register_behavior = self.RegisterToCameraAgentBehaviour()
        self.add_behaviour(register_behavior)

    async def stop(self):
        logger.info(f"[Agent] Stopping AlphaBotAgent {self.jid}")
        await super().stop()
        logger.info("[Agent] Stopped.")

# === MAIN ===
async def main():
    xmpp_domain = os.environ.get("XMPP_DOMAIN", "prosody")
    xmpp_username = os.environ.get("XMPP_USERNAME", "alpha-pi-zero-agent")
    xmpp_password = os.environ.get("XMPP_PASSWORD", "top_secret")
    xmpp_jid = f"{xmpp_username}@{xmpp_domain}"

    logger.info("Starting AlphaBot XMPP Agent...")
    logger.info(f"XMPP JID: {xmpp_jid}")

    try:
        agent = AlphaBotAgent(jid=xmpp_jid, password=xmpp_password, verify_security=False)

# Print the battery level
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
