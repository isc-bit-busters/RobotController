import base64
import datetime
import json
import math
# from agent.vision import *
# from agent.camera_api import CameraHandler
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
from PIL import Image


from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
from agent.alphabotlib.AlphaBot2 import AlphaBot2
from agent.alphabotlib.test import detectAruco, detect_walls, load_points, build_transformation, detect_cubes_camera_agent
from agent.nav_utils import find_collision, find_path_two_bots, find_waiting_point, generate_navmesh, find_path, SCALE as navmesh_scale

from .logAgent import send_log_message

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
SKIP_DIST = 15

arucos_ids = {
    "gerald": {
        "robot": 8,
        "goal": 1
    },
    "mael": {
        "robot": 7,
        "goal": 0
    }
}

class AlphaBotAgent(Agent):
    def __init__(self, jid, password, verify_security=True, name=None):
        super().__init__(jid=jid, password=password, verify_security=verify_security)
        self.alphabot = AlphaBot2()
        self.robot_name = name
        self.other_agent = "mael" if name == "gerald" else "gerald"
        # self.camera_handler = None  
        # self.vision_session = None
        # self.vision_input_name = None
        # self.camera_matrix = None
        # self.dist_coeffs = None
        # self.focal_length = None
        # self.running = True  
        self.last_position = []
        self.stuck_counter = 0
    async def setup(self):
        logger.info(f"HELLO MY NAME IS {self.robot_name}")
        logger.info(f"[Agent] AlphaBotAgent {self.jid} starting setup...")
        logger.info(f"[Agent] Will connect as {self.jid} to server {os.environ.get('XMPP_SERVER', 'prosody')}")
        send_log_message("Hello from " + self.robot_name, self.robot_name, msg_type="log")
        
        # Initialize camera and vision components once
        logger.info("[Agent] Initializing camera and vision components...")
        # self.camera_handler = CameraHandler()
        # self.camera_handler.initialize_camera()
        
        # Load vision model and calibration
        # self.vision_session, self.vision_input_name = load_model('/agent/yolov5n.onnx')
        # self.camera_matrix, self.dist_coeffs, self.focal_length = load_calibration('/agent/camera_calibration.npz')
        
        logger.info("[Agent] Camera and vision components initialized.")
        
        self.add_behaviour(self.InitBehaviour())
        logger.info("[Agent] Behaviors added, setup complete.")

    class RequestImageBehaviour(TimeoutBehaviour):
        async def run(self):
            thread_id = str(uuid.uuid4())
            msg = Message(to="camera_agent@prosody") 
            msg.body = "request_image"
            msg.thread = thread_id
            msg.metadata = {"thread": thread_id}
            now = datetime.datetime.now()
            await self.send(msg)
            send_log_message("Requesting image from camera agent", self.agent.robot_name, msg_type="log")

            msg = await self.receive(timeout=10)
            
            # thread_id = str(uuid.uuid4())
            # msg = Message(to="camera_agent@prosody") 
            # msg.body = "request_walls"
            # msg.thread = thread_id
            # msg.metadata = {"thread": thread_id}
            # now = datetime.datetime.now()
            # await self.send(msg) # Check for a message every second
            # walls = await self.receive(timeout=10)
            # walls = json.loads(walls.body)
            async def process():
                if not msg:
                    logger.info("[Behavior] No message received.")
                    return 

                if not msg.body.startswith("image "):
                    logger.debug("[Behavior] Message received but not an image.")
                    return 

                if not msg.thread == thread_id:
                    logger.debug(f"[Behavior] Message thread {msg.thread} does not match expected thread {thread_id}.")
                    return 

                logger.info(f"[Behavior] Received image message from {msg.sender}")
                time_human = datetime.datetime.now().strftime("%H:%M:%S.%f")
                logger.info(f"[Behavior] Message received at {time_human}")

                encoded_img = msg.body.split("image ")[1].strip()

                logger.info("[Behavior] Decoding image..." )
                decoded_img = base64.b64decode(encoded_img)
                img = cv2.imdecode(np.frombuffer(decoded_img, np.uint8), cv2.IMREAD_COLOR)
                logger.info("[Behavior] Image decoded successfully.")

                img = cv2.resize(img, (1024, 576), img)

                arucos = detectAruco(img)
                print(f"[{self.agent.robot_name}] Detected Arucos: {arucos}")
                print(f"My arucos: {arucos_ids[self.agent.robot_name]}")

                if arucos_ids[self.agent.robot_name]["robot"] not in arucos:
                    logger.warning("[Behavior] ⚠ Robot ID not found in image.")

                    if self.agent.stuck_counter > 2:
                        logger.info(f"[Behavior] Stuck for {self.agent.stuck_counter} ticks, trying to unstuck by moving back.")
                        self.agent.alphabot.move_back(1)
                        self.agent.alphabot.turn_left(0.1)
                    else:
                        logger.info(f"[Behavior] Stuck for {self.agent.stuck_counter} ticks, trying to unstuck by moving forward.")
                        self.agent.alphabot.advance(2)

                    self.agent.stuck_counter += 1
                    return
                else:
                    self.agent.stuck_counter = 0

                
                if arucos_ids[self.agent.robot_name]["goal"] not in arucos:
                    logger.warning("[Behavior] ⚠ Goal ID not found in image.")
                    return
                
                if arucos_ids[self.agent.other_agent]["robot"] not in arucos:
                    logger.warning("[Behavior] ⚠ Other robot ID not found in image.")
                    return
                
                if arucos_ids[self.agent.other_agent]["goal"] not in arucos:
                    logger.warning("[Behavior] ⚠ Other robot goal ID not found in image. Setting it to other robot's position.")
                    arucos_ids[self.agent.other_agent]["goal"] = arucos_ids[self.agent.other_agent]["robot"]

                # Get the robot and goal arucos positions on the image
                robot_pos = arucos[arucos_ids[self.agent.robot_name]["robot"]]
                goal_pos = arucos[arucos_ids[self.agent.robot_name]["goal"]]

                other_robot_pos = arucos[arucos_ids[self.agent.other_agent]["robot"]]
                other_goal_pos = arucos[arucos_ids[self.agent.other_agent]["goal"]]

                delta_x = abs(self.agent.last_position["x"] - robot_pos["x"])
                delta_y = abs(self.agent.last_position["y"] - robot_pos["y"])
                logger.info(f"[Behavior] Delta X: {delta_x}, Delta Y: {delta_y}")
                if delta_x <= 0.5 and delta_y <= 0.5:
                    logger.info(f"[Behavior] Robot stuck, trying to unstuck.")
                    self.agent.alphabot.move_back(1)
                    self.agent.alphabot.turn_left(0.1)
                    return
                if self.agent.last_position == robot_pos:
                    logger.info("[Behavior] Same position as before, skipping image.")
                    
                self.agent.last_position = robot_pos

                # Apply the homography transformation to the robot to get its "ground" position
                trans = self.agent.trans
                ground_robot_pos = trans((robot_pos["x"], robot_pos["y"]))
                ground_robot_pos = (int(ground_robot_pos[0]), int(ground_robot_pos[1]))

                ground_other_robot_pos = trans((other_robot_pos["x"], other_robot_pos["y"]))
                ground_other_robot_pos = (int(ground_other_robot_pos[0]), int(ground_other_robot_pos[1]))
                
                logger.info(f"[Behaviour] going from {ground_robot_pos} to {goal_pos}")

                # path = find_path((ground_robot_pos[0], 0, ground_robot_pos[1]), (goal_pos["x"], 0, goal_pos["y"]), *self.agent.navmesh)

                paths = find_path_two_bots(
                    (ground_robot_pos[0], 0, ground_robot_pos[1]),
                    (goal_pos["x"], 0, goal_pos["y"]),
                    (ground_other_robot_pos[0], 0, ground_other_robot_pos[1]),
                    (other_goal_pos["x"], 0, other_goal_pos["y"]),
                    *self.agent.navmesh
                )

                path = paths[0] if paths else None

                if path is not None:
                    logger.info(f"[Behavior] Path found: {path}")
                else:
                    logger.warning("[Behavior] No path found.")
                    return

                if len(path) < 2:
                    logger.warning(f"[Behavior] Path only contains {len(path)} elements, not enough waypoints.")
                    return

                other_path = paths[1]
                collides = find_collision(path, other_path, step_dist=0.2)

                if collides is not None:
                    # Possible collision detected on the path.
                    # If we're the closest to the goal, we should wait and let the other robot pass.
                    # Otherwise, pray to the gods that the other robot will wait for us.
    
                    point1, point2, collision_dist = collides

                    logger.info(f"[Behavior] Collision detected on path: {point1} {point2} {collision_dist}")

                    # Compute distance to the goal for both robots
                    our_dist_to_goal = 0
                    other_dist_to_goal = 0
                    for i in range(len(path) - 1):
                        p1, p2 = path[i], path[i + 1]
                        our_dist_to_goal += np.linalg.norm(p2 - p1)

                    for i in range(len(other_path) - 1):
                        p1, p2 = other_path[i], other_path[i + 1]
                        other_dist_to_goal += np.linalg.norm(p2 - p1)

                    # Are we closer to the goal than the other robot?
                    if our_dist_to_goal < other_dist_to_goal:
                        logger.info("[Behavior] We are closer to the goal, waiting for the other robot to pass.")
                        waiting_point = find_waiting_point(path, other_path)
                        if waiting_point is not None:
                            shortened_path, _, _ = waiting_point
                            logger.info(f"[Behavior] Waiting point found: {waiting_point[-1]}")
                            path = shortened_path
                        else:
                            logger.warning("[Behavior] No waiting point found, hold on to your butts, we're going to fucking crash.")
                    else:
                        logger.info("[Behavior] Other bot is closer to the goal. Hope they're well behaved and will wait for us.")


                next_waypoint_id = 1
                next_waypoint = path[0] if len(path) == 1 else path[next_waypoint_id]
                last_waypoint = path[-1]
                dist_to_next_waypoint = math.sqrt(
                    (next_waypoint[0] - ground_robot_pos[0]) ** 2 + (next_waypoint[2] - ground_robot_pos[1]) ** 2
                )
                    
                logger.info(f"[Behaviour] SKIP::: {dist_to_next_waypoint}")

                # Robot has a hard time moving really small distances, so skip waypoints that are too close
                dist_to_skip = SKIP_DIST
                while dist_to_next_waypoint < dist_to_skip:
                    logger.info("[Behaviour] Next waypoint too close, skipping to next")
                    if next_waypoint_id + 1 >= len(path) - 1:
                        logger.warning(f"[Behavior] Path only contains {len(path)} elements, not enough waypoints.")
                        break 

                    next_waypoint = path[next_waypoint_id + 1]
                    dist_to_next_waypoint = math.sqrt(
                        (next_waypoint[0] - ground_robot_pos[0]) ** 2 + (next_waypoint[2] - ground_robot_pos[1]) ** 2
                    )
                    next_waypoint_id += 1
                    dist_to_skip -= dist_to_next_waypoint
              
                time_to_move = self.agent.alphabot.get_move_time(dist_to_next_waypoint)

                logger.info(f"[Behavior] Next waypoint: #{next_waypoint_id} {next_waypoint}")
                logger.info(f"[Behavior] Current position: {robot_pos}")
                logger.info(f"[Behavior] Distance to next waypoint: {dist_to_next_waypoint}")
                logger.info(f"[Behavior] Time to next waypoint: {time_to_move} seconds")

                #region Visualization

                # Draw the navmesh 
                navmesh_overlay = np.zeros_like(img)
                for polygon in self.agent.navmesh[1]:
                    pts = np.array([[self.agent.navmesh[0][i][0] * navmesh_scale, self.agent.navmesh[0][i][2] * navmesh_scale] for i in polygon], np.int32)
                    cv2.fillPoly(navmesh_overlay, [pts], (60, 190, 60), lineType=cv2.LINE_AA)
                    cv2.polylines(img, [pts], isClosed=True, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)

                cv2.addWeighted(navmesh_overlay, 0.2, img, 1, 0, img)

                # Draw the path and waypoints
                for i in range(len(path) - 1):
                    pt1 = (int(path[i][0]), int(path[i][2]))
                    pt2 = (int(path[i + 1][0]), int(path[i + 1][2]))
                    cv2.line(img, pt1, pt2, (0, 255, 255), 2)
                    
                    # skipped waypoints in red
                    dot_color = (0, 255, 255) if i > next_waypoint_id else (0, 0, 255)
                    cv2.circle(img, pt1, 5, dot_color, -1)

                # Robot ground pos in light blue, and image pos in dark blue
                cv2.circle(img, (int(robot_pos["x"]), int(robot_pos["y"])), 5, (255, 0, 0), -1)
                cv2.circle(img, (ground_robot_pos[0], ground_robot_pos[1]), 5, (255, 200, 10), -1)

                # Next waypoint in pink 
                cv2.circle(img, (int(next_waypoint[0]), int(next_waypoint[2])), 5, (200, 200, 255), -1)
                
                # Goal in purple
                cv2.circle(img, (int(last_waypoint[0]), int(last_waypoint[2])), 5, (255, 0, 255), -1)

                # Draw line showing the robot's angle 
                angle_rad = math.radians(robot_pos["angle"])
                angle_length = 50  # Length of the line
                pt1 = (int(robot_pos["x"]), int(robot_pos["y"]))
                pt2 = (int(robot_pos["x"] + angle_length * math.sin(angle_rad)),
                        int(robot_pos["y"] + angle_length * math.cos(angle_rad)))
                cv2.line(img, pt1, pt2, (125, 0, 125), 2)

                # Draw an arrow spike at the end of the line
                arrow_length = 10
                arrow_angle = math.radians(30)  # Angle of the arrow spike
                pt3 = (int(pt2[0] - arrow_length * math.cos(angle_rad - arrow_angle)),
                        int(pt2[1] - arrow_length * math.sin(angle_rad - arrow_angle)))
                pt4 = (int(pt2[0] - arrow_length * math.cos(angle_rad + arrow_angle)),
                        int(pt2[1] - arrow_length * math.sin(angle_rad + arrow_angle)))
                cv2.line(img, pt2, pt3, (125, 0, 125), 2)
                cv2.line(img, pt2, pt4, (125, 0, 125), 2)

                # Print the angle as text next to the robot
                angle_text = f"Angle: {robot_pos['angle']:.2f} deg"
                cv2.putText(img, angle_text, (int(robot_pos["x"]) + 5, int(robot_pos["y"])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

                cv2.imwrite(f"/agent/path_image_{int(time.time())}.jpg", img)
                cv2.imwrite(f"/agent/path_image_latest.jpg", img)

                #endregion 

                if self.agent.alphabot.gotoing:
                    logger.info("[Behavior] Already going to a waypoint, skipping this message.")
                else:
                    self.agent.alphabot.goto(ground_robot_pos[0], ground_robot_pos[1], next_waypoint[0], next_waypoint[2], robot_pos["angle"], max_time=3)

            await process()

            delta = datetime.timedelta(milliseconds=IMAGE_INTERVAL_MS)
            request_image_behavior = self.agent.RequestImageBehaviour(start_at=datetime.datetime.now() + delta)
            self.agent.add_behaviour(request_image_behavior)
    class StartStopBehaviour(TimeoutBehaviour):
        async def run(self):
            logger.info("[StartStop] Waiting for start/stop commands...")
            msg = await self.receive(timeout=1)  # Wait for a message

            if msg:
                command = msg.body.lower()
                if command == "start":
                    logger.info("[StartStop] Received start command. Starting robot...")

                    # Remove existing RequestImageBehaviour instances
                    for behavior in self.agent.behaviours:
                        if isinstance(behavior, self.agent.RequestImageBehaviour):
                            self.agent.remove_behaviour(behavior)
                            logger.info("[StartStop] Removed existing RequestImageBehaviour.")

                    # Add a new RequestImageBehaviour
                    request_image_behavior = self.agent.RequestImageBehaviour(start_at=datetime.datetime.now()+IMAGE_INTERVAL_MS)
                    self.agent.add_behaviour(request_image_behavior)

                elif command == "stop":
                    logger.info("[StartStop] Received stop command. Stopping robot...")

                    # Remove all RequestImageBehaviour instances
                    for behavior in self.agent.behaviours:
                        if isinstance(behavior, self.agent.RequestImageBehaviour):
                            self.agent.remove_behaviour(behavior)
                            logger.info("[StartStop] Stopped RequestImageBehaviour.")

                    self.agent.alphabot.stop()
    # class TestBehaviour(TimeoutBehaviour):
    #     async def run(self):
    #         logger.info("[Test] Running test behavior...")
            
    #         try:
    #             # Capture image using the pre-initialized camera handler
    #             image = self.agent.camera_handler.capture_image()
                
    #             if image is not None:
    #                 # Process the image with vision components
    #                 results = detect_cubes(
    #                     image=image,
    #                     session=self.agent.vision_session,
    #                     input_name=self.agent.vision_input_name,
    #                     camera_matrix=self.agent.camera_matrix,
    #                     dist_coeffs=self.agent.dist_coeffs,
    #                     focal_length=self.agent.focal_length
    #                 )
                    
    #                 logger.info(f"[Test] Vision detection results: {results}")
                    
    #                 # timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    #                 # filename = f"/agent/test_image_{timestamp}.jpg"
    #                 # cv2.imwrite(filename, image)
    #                 # logger.info(f"[Test] Saved test image to {filename}")
    #             else:
    #                 logger.warning("[Test] Failed to capture image from camera")
                
    #         except Exception as e:
    #             logger.error(f"[Test] Error in test behavior: {str(e)}", exc_info=True)
            
    #         # Schedule the next run
    #         now = datetime.datetime.now()
    #         delta = datetime.timedelta(milliseconds=IMAGE_INTERVAL_MS)
    #         next_test = self.agent.TestBehaviour(start_at=now + delta)
    #         self.agent.add_behaviour(next_test)

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
                print(f"SAVING IMAGE {name}.jpg")
                cv2.imwrite(f"/agent/{name}.jpg", img)
            return img

        async def run(self):
            robot_id = arucos_ids[self.agent.robot_name]["robot"]

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
                
                # msg = await self.receive(timeout=10)  # Check for a message every second
                # logger.info(f" Walls {msg.sender}: {msg.body}")
            else:
                logger.info("[Step 0] No cached NavMesh found, generating a new one...")

                logger.info("[Step 0] Requesting initial image...")
                img0 = await self.request_image("0_initial")
                # while True: 
                #     msg = await self.receive(timeout=1)
                #     if msg and msg.body.startswith("validate"):
                #         logger.info(f"[Step 0] Received message from {msg.sender}: {msg.body}")
                #         break
                #     elif msg and msg.body.startswith("take_picture"):
                #         # request another img and wait the validation button 
                #         logger.info(f"[Step 0] Received message from {msg.sender}: {msg.body}")
                #         img0 = await self.request_image("0_initial")
                #         continue

                cv2.imwrite("/agent/navmesh_image_base.jpg", img0)
                print(f"img0 shape: {img0.shape}")
                # img0 = cv2.resize(img0, (1024,576), img0)
               
                thread_id = str(uuid.uuid4())
                msg = Message(to="camera_agent@prosody") 
                msg.body = "request_walls"
                msg.thread = thread_id
                msg.metadata = {"thread": thread_id}
                now = datetime.datetime.now()
                await self.send(msg) # Check for a message every second
                walls = await self.receive(timeout=10)
                walls = json.loads(walls.body)
                #convert this in an iterable object
                # walls = detect_walls(img0)
                # cubes = detect_cubes_camera_agent(img0)
                # walls += cubes
                # do comparation btw new_walls and walls
                # walls_server_array = np.array(new_walls)
                # walls_robot_array = np.array(walls)

                # # Compare the arrays
                # if np.array_equal(walls_server_array, walls_robot_array):
                #     logger.info("[Comparison] Walls server and Walls robot are the same.")
                # else:
                #     logger.info("[Comparison] Walls server and Walls robot are different.")
                    
                #     # Find the differences
                #     diff_server = []
                #     diff_robot = []

                #     for i, (server_row, robot_row) in enumerate(zip(walls_server_array, walls_robot_array)):
                #         if not np.array_equal(server_row, robot_row):
                #             diff_server.append(server_row)
                #             diff_robot.append(robot_row)

                #     logger.info(f"[Comparison] Differences in Walls server: {diff_server}")
                #     logger.info(f"[Comparison] Differences in Walls robot: {diff_robot}")
                
                # receive message from another agent 
                
                # msg = await self.receive(timeout=999)  # Check for a message every second
                # logger.info(f" Walls {msg.sender}: {msg.body}")
                
                
                # print(len(cubes))
                # wall_scale_factor = 0.8
                # # send a message to another agent
                
                
                # new_walls = []
                # for wall in walls:
                #     x1, y1, x2, y2 = wall
                #     length_x = abs(x2 - x1)
                #     length_y = abs(y2 - y1)

                #     if length_x > length_y:
                #         x1 = int(x1 - (length_x - length_x * wall_scale_factor) / 2)
                #         x2 = int(x2 + (length_x - length_x * wall_scale_factor) / 2)
                #     else:
                #         y1 = int(y1 - (length_y - length_y * wall_scale_factor) / 2)
                #         y2 = int(y2 + (length_y - length_y * wall_scale_factor) / 2)

                #     new_walls.append([x1, y1, x2, y2])

                # walls = new_walls
                
                # # Apply the homography transformation to the walls
                # walls = [[tx1, ty1, tx2, ty2] 
                #         for x1, y1, x2, y2 in walls 
                #         for tx1, ty1 in [trans((x1, y1))]
                #         for tx2, ty2 in [trans((x2, y2))]]
               
                walls_img = img0.copy()
                for p in walls:
                    cv2.rectangle(
                        walls_img, (int(p[0]), int(p[1])), (int(p[2]), int(p[3])), (0, 0, 255), 2
                    )  # Draw rectangles in red
                    cv2.circle(walls_img, (int(p[0]), int(p[1])), 5, (255, 0, 0), -1)
                    cv2.circle(walls_img, (int(p[2]), int(p[3])), 5, (0, 255, 0), -1)
                # draw the cubes in blue
                # for p in cubes:
                #     cv2.rectangle(
                #         walls_img, (int(p[0]), int(p[1])), (int(p[2]), int(p[3])), (255, 0, 0), 2
                #     )
                #     cv2.circle(walls_img, (int(p[0]), int(p[1])), 5, (255, 0, 0), -1)
                #     cv2.circle(walls_img, (int(p[2]), int(p[3])), 5, (0, 255, 0), -1)
                cv2.imwrite("/agent/walls_image.jpg", walls_img)

                send_log_message("Walls detected", self.agent.robot_name, msg_type="log")
                encoded_img = base64.b64encode(walls_img).decode("utf-8")
                # TODO: too big
                # send_log_message(encoded_img, self.agent.robot_name, msg_type="path_image")

                logger.info(f"[Step 0] Detected walls: {walls}")
                before_time = time.time()
                logger.info("[Step 0] Generating NavMesh...")                
                # walls += cubes
                vertices, polygons = generate_navmesh(walls)
                self.agent.navmesh = (vertices, polygons)
            
                nav_img = walls_img.copy()
                navmesh_overlay = np.zeros_like(nav_img)
                for polygon in self.agent.navmesh[1]:
                    pts = np.array([[self.agent.navmesh[0][i][0] * navmesh_scale, self.agent.navmesh[0][i][2] * navmesh_scale] for i in polygon], np.int32)
                    cv2.fillPoly(navmesh_overlay, [pts], (60, 190, 60), lineType=cv2.LINE_AA)
                    cv2.polylines(nav_img, [pts], isClosed=True, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)

                cv2.addWeighted(navmesh_overlay, 0.2, nav_img, 1, 0, nav_img)

                cv2.imwrite("/agent/navmesh_image.jpg", nav_img)

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
                
                while True and img1 is not None: 
                    msg = await self.receive(timeout=1)  # Check for a message every second
                    if msg:
                        print(f"msg: {msg.body}")
                #check specific content of msg
                    if msg and msg.body.startswith("validate"):
                        logger.info(f"[Step 1.5] Received message from {msg.sender}: {msg.body}")
                        break
                    elif msg and msg.body.startswith("take_picture"): 
                        # request another img and wait the validation button 
                        logger.info(f"[Step 1.5] Received message from {msg.sender}: {msg.body}")
                        img1 = await self.request_image("1_initial")
                        continue
                arucos1 = detectAruco(img1)
            
                print(f"Detected Arucos: {arucos1}")
                if robot_id not in arucos1:
                    logger.warning("[Step 1] ⚠ Robot ID not found in initial image.")
                    self.agent.alphabot.advance(0.2)
                    continue
                else: 
                    self.agent.last_position = arucos1[robot_id]

                pos1 = arucos1[robot_id]
                logger.info(f"[Step 1] Robot initial position: {pos1}")

                detected_bot = True
            if self.agent.robot_name == "gerald":
                msg = Message(to=f"armClient@prosody")
                msg.set_metadata("type", "set_host_ip")
                msg.body = "10.30.5.159"
                await self.send(msg)
                msg.set_metadata("type", "activate_gripper")
                await self.send(msg)
                msg.set_metadata("type", "open_gripper")    
                await self.send(msg)
                # msg.set_metadata("type", "trajectory")
                # msg.body = "[[-0.09, 0.27, 0.2,0,0,-1]]"
                # await self.send(msg)
      
            logger.info("[RoboticArm] Message sent ...")
            await asyncio.sleep(2)
            logger.info("[Step 1.5] Waiting for a message from another agent...")

            while True: 
                msg = await self.receive(timeout=1)  # Check for a message every second
                if msg and msg.body.startswith("calibrate"):
                    logger.info(f"[Step 1.5] Received message from {msg.sender}: {msg.body}")
                    break

            # Wait for a message from the other agent
            
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
                return
            else: 
                self.agent.last_position = arucos2[robot_id]

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
                return
            else:
                self.agent.last_position = arucos3[robot_id]
            
            pos3 = arucos3[robot_id]
            logger.info(f"[Step 5] Robot new position after rotation:f {pos3}")

            rot_angle = pos3["angle"] - pos2["angle"]
            self.agent.alphabot.setTurnSpeed(rot_angle / rot_t)
            logger.info(f"[Step 5] Rotation speed: {rot_angle / rot_t} degrees/s")
            
            logger.info(f"[Step 5] Calibration done. Set the robot in the initial position.")
            while True:
                msg = await self.receive(timeout=1)  # Check for a message every second
                if msg and msg.body.startswith("start"):
                    break   
            logger.info("[Behavior] Listening for image messages...")

            await asyncio.sleep(2)

        async def on_end(self):
            logger.info("[Behavior] MoveAndMeasureBehaviour ended.")

            # gerald requests images on x.0 and x.5 sec, mael on x.25 and x.75 sec 
            now = datetime.datetime.now()
            staggered_start_time = now + datetime.timedelta(milliseconds=IMAGE_OFFSET_MS if self.agent.robot_name == "mael" else 0)

            logger.info(f"[Agent] Staggered start time: {staggered_start_time}")

            request_image_behavior = self.agent.RequestImageBehaviour(start_at=staggered_start_time)
            self.agent.add_behaviour(request_image_behavior)

            # test = self.agent.TestBehaviour(start_at=staggered_start_time)
            # self.agent.add_behaviour(test)
            
            # startandstop = self.agent.StartStopBehaviour(start_at=staggered_start_time)
            # self.agent.add_behaviour(startandstop)

    async def stop(self):
        logger.info(f"[Agent] Stopping AlphaBotAgent {self.jid}")
        # if self.camera_handler:
        #     self.camera_handler.close_camera()
        #     logger.info("[Agent] Camera handler closed.")
        await super().stop()
        logger.info("[Agent] Stopped.")

async def main():
    xmpp_domain = os.environ.get("XMPP_DOMAIN", "prosody")
    xmpp_username = os.environ.get("XMPP_USERNAME")

    if not xmpp_username:
        logger.error("XMPP_USERNAME environment variable is not set.")
        return 
    
    # === Test depth estimation before starting the agent ===
    # try:
        # camera_api = CameraHandler()
        # camera_api.initialize_camera()
       
        # bgr_image = camera_api.capture_image()
        # rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
        # pil_image = Image.fromarray(rgb_image)

        # obstacle_zones = estimate_depth_map(pil_image, visualize=True)

        # print("Obstacle detection by zone:")
        # for zone, present in obstacle_zones.items():
        #     print(f"{zone.capitalize()}: {'🚫 Obstacle' if present else '✅ Clear'}")

    # except Exception as e:
    #     logger.error(f"❌ Depth estimation error: {e}", exc_info=True)
    #     return

    xmpp_jid = f"{xmpp_username}@{xmpp_domain}"
    xmpp_password = os.environ.get("XMPP_PASSWORD", "top_secret")

    logger.info("Starting AlphaBot XMPP Agent...")
    logger.info(f"XMPP JID: {xmpp_jid}")

    try:
        agent = AlphaBotAgent(
            jid=xmpp_jid, 
            password=xmpp_password,
            verify_security=False,
            name=xmpp_username
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