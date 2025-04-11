import base64
from agent.alphabotlib.Camera import get_picture_base64
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour, OneShotBehaviour
from spade.message import Message
from agent.alphabotlib.AlphaBot2 import AlphaBot2
import asyncio
import os
import time
import logging
import asyncio

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("AlphaBotAgent")

# Enable SPADE and XMPP specific logging
for log_name in ["spade", "aioxmpp", "xmpp"]:
    log = logging.getLogger(log_name)
    log.setLevel(logging.DEBUG)
    log.propagate = True

class AlphaBotAgent(Agent):
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

    async def setup(self):
        logger.info(f"[Agent] AlphaBotAgent {self.jid} starting setup...")
        logger.info(f"[Agent] Will connect as {self.jid} to server {os.environ.get('XMPP_SERVER', 'prosody')}")
        
        # Add command listener behavior
        register_behavior = self.RegisterToCameraAgentBehaviour()
        self.add_behaviour(register_behavior)

        listen_for_image_behavior = self.ListenForImageBehaviour()
        self.add_behaviour(listen_for_image_behavior)
        
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
