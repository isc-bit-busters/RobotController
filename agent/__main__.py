import base64
from spade.agent import Agent
from spade.behaviour import TimeoutBehaviour
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

IMAGE_FREQUENCY = 0.5 # seconds

class AlphaBotAgent(Agent):
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
                request_image_behavior = self.RequestImageBehaviour(start_at=now + IMAGE_FREQUENCY * 1000)
                self.agent.add_behaviour(request_image_behavior)
            else:
                logger.debug("[Behavior] No message received during timeout.")


    async def setup(self):
        logger.info(f"[Agent] AlphaBotAgent {self.jid} starting setup...")
        logger.info(f"[Agent] Will connect as {self.jid} to server {os.environ.get('XMPP_SERVER', 'prosody')}")
        
        # Add command listener behavior
        now = asyncio.get_event_loop().time() * 1000
        request_image_behavior = self.RequestImageBehaviour(start_at=now)
        self.add_behaviour(request_image_behavior)
        
        logger.info("[Agent] Behaviors added, setup complete.")

    async def stop(self):
        logger.info("[Agent] Stopping AlphaBotAgent " + self.jid)
        unregister_behavior = self.UnregisterFromCameraAgentBehaviour()
        self.add_behaviour(unregister_behavior)
        
        await super().stop()
        logger.info("[Agent] AlphaBotAgent stopped.")

async def main():
    xmpp_domain = os.environ.get("XMPP_DOMAIN", "prosody")
    xmpp_username = os.environ.get("XMPP_USERNAME", "alpha-pi-zero-agent")
    xmpp_jid = f"{xmpp_username}@{xmpp_domain}"
    xmpp_password = os.environ.get("XMPP_PASSWORD", "top_secret")
    
    logger.info("Starting AlphaBot XMPP Agent")
    logger.info(f"XMPP JID: {xmpp_jid}")
    logger.info(f"XMPP Password: {'*' * len(xmpp_password)}")
    
    try:
        agent = AlphaBotAgent(
            jid=xmpp_jid, 
            password=xmpp_password,
            verify_security=False
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
