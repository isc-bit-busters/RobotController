from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
from agent.alphabotlib.AlphaBot2 import AlphaBot2
import asyncio
import os
import time
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("AlphaBotAgent")

# Enable SPADE and XMPP specific logging
for log_name in ["spade", "aioxmpp", "xmpp"]:
    log = logging.getLogger(log_name)
    log.setLevel(logging.DEBUG)
    log.propagate = True

class AlphaBotAgent(Agent):
    class HeartbeatBehaviour(PeriodicBehaviour):
        async def on_start(self):
            logger.info("[Heartbeat] Starting heartbeat behavior")
            
        async def run(self):
            logger.debug("[Heartbeat] Sending heartbeat message")
            try:
                # Create heartbeat message to self
                msg = Message(to=str(self.agent.jid))
                msg.set_metadata("performative", "inform")
                msg.body = "heartbeat"
                
                await self.send(msg)
                logger.debug("[Heartbeat] Heartbeat message sent successfully")
            except Exception as e:
                logger.error(f"[Heartbeat] Error sending heartbeat: {str(e)}")

    class XMPPCommandListener(CyclicBehaviour):
        async def on_start(self):
            logger.info("[Behavior] Initializing AlphaBot2...")
            self.ab = AlphaBot2()
            logger.info("[Behavior] Ready to receive commands.")
            
        async def run(self):
            logger.debug("[Behavior] Waiting for messages...")
            msg = await self.receive(timeout=10)
            if msg:
                logger.info(f"[Behavior] Received command: {msg.body}")
                await self.process_command(msg.body)
                
                # Send a confirmation response
                reply = Message(to=str(msg.sender))
                reply.set_metadata("performative", "inform")
                reply.body = f"Executed command: {msg.body}"
                await self.send(reply)
                logger.info(f"[Behavior] Sent reply to {msg.sender}")
            else:
                logger.debug("[Behavior] No message received during timeout.")
        
        async def process_command(self, command):
            command = command.strip().lower()
            
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
        
        # Add heartbeat behavior that runs every 30 seconds
        heartbeat_behavior = self.HeartbeatBehaviour(period=30)
        self.add_behaviour(heartbeat_behavior)
        
        logger.info("[Agent] Behaviors added, setup complete.")

import asyncio

async def main():
    # Get XMPP credentials from environment variables
    xmpp_domain = os.environ.get("XMPP_DOMAIN", "prosody")
    xmpp_username = os.environ.get("XMPP_USERNAME", "alpha-pi-zero-agent")
    xmpp_jid = f"{xmpp_username}@{xmpp_domain}"
    xmpp_password = os.environ.get("XMPP_PASSWORD", "top_secret")
    
    # Check for XMPP server in environment (can be different from domain)
    xmpp_server = os.environ.get("XMPP_SERVER", "prosody")
    xmpp_port = int(os.environ.get("XMPP_PORT", "5222"))
    
    logger.info("Starting AlphaBot XMPP Agent")
    logger.info(f"XMPP JID: {xmpp_jid}")
    logger.info(f"XMPP Password: {'*' * len(xmpp_password)}")
    logger.info(f"XMPP Server: {xmpp_server}")
    logger.info(f"XMPP Port: {xmpp_port}")
    
    # Test server connectivity
    logger.info(f"Testing connection to XMPP server {xmpp_server}...")
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        result = s.connect_ex((xmpp_server, xmpp_port))
        if result == 0:
            logger.info(f"Successfully connected to {xmpp_server}:{xmpp_port}")
        else:
            logger.error(f"Could not connect to {xmpp_server}:{xmpp_port}, error code: {result}")
        s.close()
    except Exception as e:
        logger.error(f"Error testing connection: {str(e)}")
    
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
