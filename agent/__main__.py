from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from agent.alphabotlib.AlphaBot2 import AlphaBot2
import asyncio

class AlphaBotAgent(Agent):
    class RunDeviceFunctions(OneShotBehaviour):
        async def run(self):
            print("[Behavior] Initializing AlphaBot2...")
            ab = AlphaBot2()

            print("[Behavior] Moving forward...")
            ab.forward()
            await asyncio.sleep(2)
            print("[Behavior] Stopping...")
            ab.stop()
            await asyncio.sleep(2)

            print("[Behavior] Moving backward...")
            ab.backward()
            await asyncio.sleep(2)
            print("[Behavior] Stopping...")
            ab.stop()
            await asyncio.sleep(2)

            print("[Behavior] Turning left...")
            ab.left()
            await asyncio.sleep(2)
            print("[Behavior] Stopping...")
            ab.stop()
            await asyncio.sleep(2)

            print("[Behavior] Turning right...")
            ab.right()
            await asyncio.sleep(2)
            print("[Behavior] Stopping...")
            ab.stop()
            await asyncio.sleep(2)

            print("[Behavior] Setting motor speeds to 50 (left) and 50 (right)...")
            ab.setMotor(50, 50)
            await asyncio.sleep(2)
            print("[Behavior] Stopping motors...")
            ab.stop()
            await asyncio.sleep(2)

            print("[Behavior] Completed all device functions.")
            self.kill()

    async def setup(self):
        print("[Agent] AlphaBotAgent started.")
        self.add_behaviour(self.RunDeviceFunctions())
