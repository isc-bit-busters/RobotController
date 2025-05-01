import base64
import datetime
import math
from agent.vision import *
from agent.camera_api import CameraHandler
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


from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
from agent.alphabotlib.AlphaBot2 import AlphaBot2
# from agent.alphabotlib.test import detectAruco, detect_walls, load_points, build_transformation
from agent.nav_utils import generate_navmesh, find_path, SCALE as navmesh_scale

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
        self.camera_api = CameraHandler()

    class RequestImageBehaviour(TimeoutBehaviour):
        async def run(self):
            thread_id = str(uuid.uuid4())
            msg = Message(to="camera_agent@prosody") 
            msg.body = "request_image"
            msg.thread = thread_id
            msg.metadata = {"thread": thread_id}
            now = datetime.datetime.now()
            await self.send(msg)

            delta = datetime.timedelta(milliseconds=IMAGE_INTERVAL_MS)
            request_image_behavior = self.agent.RequestImageBehaviour(start_at=now + delta)
            self.agent.add_behaviour(request_image_behavior)
    
    class ListenToImageBehaviour(CyclicBehaviour):
        async def run(self):
            robot_id = 7
            goal_id = 5

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
                    logger.warning("[Behaviour] ⚠ Robot ID not found in image.")
                    return

                if goal_id not in arucos:
                    logger.warning("[Behaviour] ⚠ Goal ID not found in image.")
                    return

                pos1 = arucos[robot_id]
                pos2 = arucos[goal_id]
                
                logger.info(f"[Behaviour] going from {pos1} to {pos2}")

                path = find_path((pos1["x"], 0, pos1["y"]), (pos2["x"], 0, pos2["y"]), *self.agent.navmesh)

                if path is not None:
                    logger.info(f"[Behavior] Path found: {path}")
                else:
                    logger.warning("[Behavior] No path found.")
                    return

                if len(path) < 2:
                    logger.warning(f"[Behavior] Path only contains {len(path)} elements, not enough waypoints.")
                    return

                next_waypoint = path[1]
                last_waypoint = path[-1]
                dist_to_first_waypoint = math.sqrt(
                    (next_waypoint[0] - pos1["x"]) ** 2 + (next_waypoint[2] - pos1["y"]) ** 2
                )

                if dist_to_first_waypoint < 40:
                    logger.info("[Behaviour] Next waypoint too close, skipping to next")
                    if len(path) < 3:
                        logger.warning(f"[Behavior] Path only contains {len(path)} elements, not enough waypoints.")
                        return

                    next_waypoint = path[2]
                    dist_to_first_waypoint = math.sqrt(
                        (next_waypoint[0] - pos1["x"]) ** 2 + (next_waypoint[2] - pos1["y"]) ** 2
                    )

                time_to_move = self.agent.alphabot.get_move_time(dist_to_first_waypoint)

                logger.info(f"[Behavior] Next waypoint: {next_waypoint}")
                logger.info(f"[Behavior] Current position: {pos1}")
                logger.info(f"[Behavior] Distance to first waypoint: {dist_to_first_waypoint}")
                logger.info(f"[Behavior] Time to first waypoint: {time_to_move} seconds")

                if self.agent.alphabot.gotoing:
                    logger.info("[Behavior] Already going to a waypoint, skipping this message.")
                    return

                self.agent.alphabot.goto(pos1["x"], pos1["y"], next_waypoint[0], next_waypoint[2], pos1["angle"], max_time=100)

                # draw the navmesh on the image
                navmesh_overlay = np.zeros_like(img)
                for polygon in self.agent.navmesh[1]:
                    pts = np.array([[self.agent.navmesh[0][i][0] * navmesh_scale, self.agent.navmesh[0][i][2] * navmesh_scale] for i in polygon], np.int32)
                    cv2.fillPoly(navmesh_overlay, [pts], (60, 190, 60), lineType=cv2.LINE_AA)
                    cv2.polylines(img, [pts], isClosed=True, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)

                cv2.addWeighted(navmesh_overlay, 0.2, img, 1, 0, img)

                # draw the path on the image
                for i in range(len(path) - 1):
                    pt1 = (int(path[i][0]), int(path[i][2]))
                    pt2 = (int(path[i + 1][0]), int(path[i + 1][2]))
                    cv2.line(img, pt1, pt2, (0, 255, 255), 2)
                    cv2.circle(img, pt1, 5, (0, 255, 255), -1)

                # Show the robot in red and the next waypoint in blue
                cv2.circle(img, (int(pos1["x"]), int(pos1["y"])), 5, (0, 0, 255), -1)
                cv2.circle(img, (int(next_waypoint[0]), int(next_waypoint[2])), 5, (255, 0, 0), -1)
                cv2.circle(img, (int(last_waypoint[0]), int(last_waypoint[2])), 5, (255, 0, 255), -1)

                # Get the position of the robot on the "ground" by applying the homography transformation
                trans = self.agent.trans
                real_robot_pos = trans((pos1["x"], pos1["y"]))
                real_robot_pos = (real_robot_pos[0], real_robot_pos[1])

                print(f"Real robot position: {real_robot_pos}")

                cv2.circle(img, (real_robot_pos[0], real_robot_pos[1]), 5, (255, 255, 255), -1)


                # Draw line showing the robot's angle 
                angle_rad = math.radians(pos1["angle"])
                angle_length = 50  # Length of the line
                pt1 = (int(pos1["x"]), int(pos1["y"]))
                pt2 = (int(pos1["x"] + angle_length * math.sin(angle_rad)),
                        int(pos1["y"] + angle_length * math.cos(angle_rad)))
                cv2.line(img, pt1, pt2, (125, 0, 125), 2)

                # print the angle as text next to the robot
                angle_text = f"Angle: {pos1['angle']:.2f}°"
                cv2.putText(img, angle_text, (int(pos1["x"]) + 5, int(pos1["y"])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

                cv2.imwrite(f"/agent/path_image_{int(time.time())}.jpg", img)

            else:
                logger.debug("[Behavior] Message received but not an image.")

    class InitBehaviour(OneShotBehaviour):
        async def request_image(self, name=None):
            thread_id = str(uuid.uuid4())
            msg = Message(to="camera_agent@prosody", body="request_image")
            msg.thread = thread_id
            msg.metadata = {"thread": thread_id}
            await self.send(msg)

            logger.info(f"[Behavior] Requesting image from camera agent on thread {thread_id}...")

            reply = await self.receive(timeout=20)
            while not reply or not reply.thread == thread_id or not reply.body.startswith("image "):
                has_reply = reply is not None
                thread = reply.thread if reply else None
                message = reply.body[20:] if reply else None

                logger.info(f"[Behavior] Received reply: {has_reply}, thread: {thread}, message: {message}")

                logger.warning("No image received, retrying")
                await asyncio.sleep(1)

                thread_id = str(uuid.uuid4())
                msg = Message(to="camera_agent@prosody", body="request_image")
                msg.thread = thread_id
                msg.metadata = {"thread": thread_id}
                await self.send(msg)
                logger.info(f"[Behavior] Requesting image from camera agent on thread {thread_id}...")
                reply = await self.receive(timeout=20)

            encoded_img = reply.body.split("image ")[1].strip()
            img = cv2.imdecode(np.frombuffer(base64.b64decode(encoded_img), np.uint8), cv2.IMREAD_COLOR)

            if name is not None:
                cv2.imwrite(f"{name}.jpg", img)

            return img

        async def run(self):
            robot_id = 7

            a_points, b_points = load_points("/agent/points_mapping.png")
            logger.info(f"[Step 0] Points loaded: {a_points}, {b_points}")

            trans = build_transformation(a_points, b_points)

            self.agent.trans = trans

            # === STEP 0: Generate NavMesh ===

            if os.path.exists("/agent/navmesh.txt"):
                logger.info(f"[Step 0] Cached NavMesh found, loading from cache file")
                with open("/agent/navmesh.txt", "r") as f:
                    lines = f.readlines()
                    vertices = eval(lines[0])
                    polygons = eval(lines[1])
            else:
                logger.info("[Step 0] No cached NavMesh found, generating a new one...")

                logger.info("[Step 0] Requesting initial image...")
                img0 = await self.request_image("0_initial")

                cv2.imwrite("/agent/navmesh_image.jpg", img0)

                walls = detect_walls(img0)

                # Apply the homography transformation to the walls
                walls = [[tx1, ty1, tx2, ty2] 
                        for x1, y1, x2, y2 in walls 
                        for tx1, ty1 in [trans((x1, y1))]
                        for tx2, ty2 in [trans((x2, y2))]]

                logger.info(f"[Step 0] Detected walls: {walls}")
                before_time = time.time()
                logger.info("[Step 0] Generating NavMesh...")
                vertices, polygons = generate_navmesh(walls)

                with open("/agent/navmesh.txt", "w") as f:
                    f.write(f"{vertices}\n")
                    f.write(f"{polygons}\n")

                after_time = time.time()
                logger.info(f"[Step 0] NavMesh generated in {after_time - before_time:.2f} seconds")

            logger.info(f"[Step 0] NavMesh vertices: {vertices}")
            logger.info(f"[Step 0] NavMesh polygons: {polygons}")

            self.agent.navmesh = (vertices, polygons)

            detected_bot = False
            while not detected_bot:
                await asyncio.sleep(2)

                # === STEP 1: Take the first image ===
                logger.info("[Step 1] Requesting initial image...")
                img1 = await self.request_image("1_initial")
                arucos1 = detectAruco(img1)
                print(f"Detected Arucos: {arucos1}")
                if robot_id not in arucos1:
                    logger.warning("[Step 1] ⚠ Robot ID not found in initial image.")
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
            img2 = await self.request_image("2_after_move")
            arucos2 = detectAruco(img2)
            if robot_id not in arucos2:
                logger.warning("[Step 3] ⚠ Robot ID not found in second image.")

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

            # Calibrate rotation speed
            rot_t = 0.25
            self.agent.alphabot.turn_left(rot_t)
            await asyncio.sleep(rot_t)

            logger.info("[Step 5] Requesting image after rotation...")
            img3 = await self.request_image("3_after_rotation")
            arucos3 = detectAruco(img3)
            if robot_id not in arucos3:
                logger.warning("[Step 5] ⚠ Robot ID not found in third image.")
            
            pos3 = arucos3[robot_id]
            logger.info(f"[Step 5] Robot new position after rotation: {pos3}")

            rot_angle = pos3["angle"] - pos2["angle"]
            self.agent.alphabot.setTurnSpeed(rot_angle / rot_t)
            logger.info(f"[Step 5] Rotation speed: {rot_angle / rot_t} degrees/s")
            
            logger.info(f"[Step 5] Calibration done. Set the robot in the initial position.")



            await asyncio.sleep(2)

            

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
            
    class SendImageToDashBehaviour(CyclicBehaviour):
        async def run(self):
            xmpp_username="receiverClient"
            xmpp_server="prosody"
            msg = Message(to=f"{xmpp_username}@{xmpp_server}")
            msg.set_metadata("robot_id", self.agent.robot_name)
            msg.set_metadata("type", "image")

            image=self.agent.camera_api.capture_image()
            _, buffer = cv2.imencode(".jpg", image)
            encoded_image = base64.b64encode(buffer).decode("utf-8")

            msg.body = encoded_image
            try:
                await self.send(msg)
                logger.info(f"Message sent to {msg.to}")
            except Exception as e:
                logger.info(f"Failed to send message: {e}")
            await asyncio.sleep(2)

    class CubeDetectionBehaviour(CyclicBehaviour):
        def __init__(self):
            super().__init__()
            from agent.alphabotlib.PCA9685 import PCA9685
            self.pwm = PCA9685(debug=False)
            self.pwm.set_pwm_freq(50)
            # Calibration settings for SG90 servos
            self.x_min_pulse = 700
            self.x_max_pulse = 2000
            self.y_min_pulse = 1200
            self.y_max_pulse = 1700

            # Load model and calibration once
            from agent.vision import load_model, load_calibration
            self.session, self.input_name = load_model('/agent/yolov5n.onnx')
            self.camera_matrix, self.dist_coeffs, self.focal_length = load_calibration('/agent/camera_calibration.npz')

        async def run(self):
            logger.info("[CubeDetection] Starting cube detection cycle...")

            # X-axis angles (horizontal sweep)
            x_angles = [-30, 0, 30]
            # Y-axis angles (vertical sweep)
            y_angles = [-30, 0, 30]

            for x_angle in x_angles:
                self.pwm.set_servo_angle(0, x_angle, min_pulse=self.x_min_pulse, max_pulse=self.x_max_pulse)
                await asyncio.sleep(0.3)
                for y_angle in y_angles:
                    self.pwm.set_servo_angle(1, y_angle, min_pulse=self.y_min_pulse, max_pulse=self.y_max_pulse)
                    await asyncio.sleep(0.3)

                    logger.info(f"[CubeDetection] Capturing image at X: {x_angle}°, Y: {y_angle}°...")
                    
                    image = self.agent.camera_api.capture_image()

                    os.makedirs("/images", exist_ok=True)
                    time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    self.agent.camera_api.save_image(image, f"/images/cam_{x_angle}_{y_angle}_{time}.jpg")
                    
                    # Run YOLO detection
                    from agent.vision import detect_cubes
                    results = detect_cubes(
                        image=image,
                        session=self.session,
                        input_name=self.input_name,
                        camera_matrix=self.camera_matrix,
                        dist_coeffs=self.dist_coeffs,
                        focal_length=self.focal_length
                    )

                    logger.info(f"[CubeDetection] Detection results at X: {x_angle}, Y: {y_angle}: {results}")

                    # Send results to the dashboard
                    msg = Message(to="receiverClient@prosody")
                    msg.set_metadata("robot_id", self.agent.robot_name)
                    msg.set_metadata("type", "cube_detection")

                    msg.body = str(results) + f" at X: {x_angle}, Y: {y_angle}"
                    try:
                        await self.send(msg)
                        logger.info(f"[CubeDetection] Message sent to {msg.to}")
                    except Exception as e:
                        logger.info(f"[CubeDetection] Failed to send message: {e}")

    async def setup(self):
        logger.info(f"[Agent] AlphaBotAgent {self.jid} starting setup...")
        self.camera_api.initialize_camera()
        logger.info(f"[Agent] Will connect as {self.jid} to server {os.environ.get('XMPP_SERVER', 'prosody')}")
        
        logger.info(f"[Agent] AlphaBotAgent {self.jid} setup starting...")
       
        self.add_behaviour(self.SendImageToDashBehaviour())
        self.add_behaviour(self.CubeDetectionBehaviour())
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
