from agent.alphabotlib.Camera import get_picture_base64
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
from agent.alphabotlib.AlphaBot2 import AlphaBot2
from agent import camera_streamer
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
    class XMPPCommandListener(CyclicBehaviour):
        async def on_start(self):
            logger.info("[Behavior] Initializing AlphaBot2...")
            self.ab = AlphaBot2()
            logger.info("[Behavior] Ready to receive commands.")
            
        async def run(self):
            logger.debug("[Behavior] Waiting for messages...")
            msg = await self.receive(timeout=10)
            if msg:
                logger.info(f"[Behavior] Received command ({msg.sender}): {msg.body}")
                await self.process_command(msg)
                
                # Send a confirmation response
                reply = Message(to=str(msg.sender))
                reply.set_metadata("performative", "inform")
                reply.body = f"Executed command: {msg.body}"
                await self.send(reply)
                logger.info(f"[Behavior] Sent reply to {msg.sender}")
            else:
                logger.debug("[Behavior] No message received during timeout.")
        
        async def process_command(self, message):
            command = message.body.strip().lower()
            thread = message.thread
            sender = str(message.sender)

            if command == "forward":
                logger.info("[Behavior] Moving forward...")
                self.ab.forward()
                await asyncio.sleep(2)
                self.ab.stop()
                
            elif command == "backward":
                logger.info("[Behavior] Moving backward...")
                self.ab.backward()
                await asyncio.sleep(2)
                self.ab.stop()
                
            elif command == "left":
                logger.info("[Behavior] Turning left...")
                self.ab.left()
                await asyncio.sleep(2)
                self.ab.stop()
                
            elif command == "right":
                logger.info("[Behavior] Turning right...")
                self.ab.right()
                await asyncio.sleep(2)
                self.ab.stop()
                
            elif command.startswith("motor "):
                try:
                    _, left, right = command.split()
                    left_speed = int(left)
                    right_speed = int(right)
                    logger.info(f"[Behavior] Setting motor speeds to {left_speed} (left) and {right_speed} (right)...")
                    self.ab.setMotor(left_speed, right_speed)
                    await asyncio.sleep(2)
                    self.ab.stop()
                except (ValueError, IndexError):
                    logger.error("[Behavior] Invalid motor command format. Use 'motor <left_speed> <right_speed>'")

            elif command == "takepic":
                logger.info("[Behavior] Taking picture...")
                encoded_img = await get_picture_base64()

                msg = Message(to=sender)
                msg.body = encoded_img
                msg.thread = thread

                await self.send(msg)
                print("Picture sent.")

                pass
                    
            elif command == "stop":
                logger.info("[Behavior] Stopping...")
                self.ab.stop()
                
            else:
                logger.warning(f"[Behavior] Unknown command: {command}")

    async def setup(self):
        logger.info("[Agent] AlphaBotAgent starting setup...")
        logger.info(f"[Agent] Will connect as {self.jid} to server {os.environ.get('XMPP_SERVER', 'prosody')}")
        
        # Add command listener behavior
        command_behavior = self.XMPPCommandListener()
        self.add_behaviour(command_behavior)
        
        logger.info("[Agent] Behaviors added, setup complete.")

async def main():
    xmpp_domain = os.environ.get("XMPP_DOMAIN", "prosody")
    xmpp_username = os.environ.get("XMPP_USERNAME", "gerald")
    xmpp_jid = f"{xmpp_username}@{xmpp_domain}"
    xmpp_password = os.environ.get("XMPP_PASSWORD", "top_secret")
    
    logger.info("Starting AlphaBot XMPP Agent")
    logger.info(f"XMPP JID: {xmpp_jid}")
    logger.info(f"XMPP Password: {'*' * len(xmpp_password)}")
    
    
    # ✅ Démarrer le stream caméra dans un thread
    camera_streamer.start_camera_thread()


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
