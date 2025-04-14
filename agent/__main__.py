import base64
import math
from spade.agent import Agent
from spade.behaviour import TimeoutBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template
import asyncio
import os
import logging
import asyncio
import uuid

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("AlphaBotAgent")

# Enable SPADE and XMPP specific logging
for log_name in ["spade", "aioxmpp", "xmpp"]:
    log = logging.getLogger(log_name)
    log.setLevel(logging.DEBUG)
    log.propagate = True

IMAGE_INTERVAL_MS = 500 
IMAGE_OFFSET_MS = IMAGE_INTERVAL_MS / 2

class AlphaBotAgent(Agent):
    def __init__(self, jid, password, verify_security=True, name=None):
        super().__init__(jid=jid, password=password, verify_security=verify_security)
        self.robot_name = name

    class RequestImageBehaviour(TimeoutBehaviour):
        async def run(self):
            thread_id = uuid.uuid4()
            msg = Message(to="camera_agent@prosody") 
            msg.body = "request_image"
            msg.thread = str(thread_id)
            
            logger.info("[Behavior] Requesting image to camera agent...")
            await self.send(msg)

            template = Template()
            template.thread = thread_id

            reply = await self.receive(timeout=10, template=template)
            if reply and reply.body.startswith("image "):
                logger.info(f"[Behavior] Received image message from {msg.sender}")
                time_ms = asyncio.get_event_loop().time() * 1000
                logger.info(f"[Behavior] Message received at {time_ms} ms")

                encoded_img = msg.body.split("image ")[1].strip()

                logger.info("[Behavior] Decoding image..." )
                decoded_img = base64.b64decode(encoded_img)
                logger.info("[Behavior] Image decoded.")

                now = asyncio.get_event_loop().time() * 1000
                request_image_behavior = self.RequestImageBehaviour(start_at=now + IMAGE_INTERVAL_MS)
                self.agent.add_behaviour(request_image_behavior)
            else:
                logger.debug("[Behavior] No message received during timeout.")

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


    async def setup(self):
        logger.info(f"[Agent] AlphaBotAgent {self.jid} starting setup...")
        logger.info(f"[Agent] Will connect as {self.jid} to server {os.environ.get('XMPP_SERVER', 'prosody')}")
        
        # gerald requests images on x.0 and x.5 sec, mael on x.25 and x.75 sec 
        now = asyncio.get_event_loop().time() * 1000
        staggered_start_time = math.ceil(now / IMAGE_INTERVAL_MS) * IMAGE_INTERVAL_MS 
        staggered_start_time += IMAGE_OFFSET_MS if self.robot_name == "mael" else 0

        request_image_behavior = self.RequestImageBehaviour(start_at=staggered_start_time)
        self.add_behaviour(request_image_behavior)
    
        other = "mael" if self.robot_name == "gerald" else "gerald"
        ping_behavior = self.PingBehaviour(to=f"{other}@prosody")
        self.add_behaviour(ping_behavior)
        
        pong_behavior = self.PongBehaviour()
        self.add_behaviour(pong_behavior)
        
        logger.info("[Agent] Behaviors added, setup complete.")


async def main():
    xmpp_domain = os.environ.get("XMPP_DOMAIN", "prosody")
    xmpp_username = os.environ.get("XMPP_USERNAME")
    if not xmpp_username:
        logger.error("XMPP_USERNAME environment variable is not set.")
        return        

    xmpp_jid = f"{xmpp_username}@{xmpp_domain}"
    xmpp_password = os.environ.get("XMPP_PASSWORD", "top_secret")
    
    logger.info("Starting AlphaBot XMPP Agent")
    logger.info(f"XMPP JID: {xmpp_jid}")
    logger.info(f"XMPP Password: {'*' * len(xmpp_password)}")
    
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
        
        try:
            while agent.is_alive():
                logger.debug("Agent is alive and running...")
                await asyncio.sleep(10)  # Log every 10 seconds that agent is alive
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received")
            await agent.stop()
            logger.info("Agent stopped by user.")
    except Exception as e:
        logger.error(f"Error starting agent: {str(e)}", exc_info=True)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.critical(f"Critical error in main loop: {str(e)}", exc_info=True)
