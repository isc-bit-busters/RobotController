import RPi.GPIO as GPIO
import time
import math
import logging

logger = logging.getLogger(__name__)

class AlphaBot2(object):
	def __init__(self,ain1=12,ain2=13,ena=6,bin1=20,bin2=21,enb=26):
		self.AIN1 = ain1
		self.AIN2 = ain2
		self.BIN1 = bin1
		self.BIN2 = bin2
		self.ENA = ena
		self.ENB = enb
		self.PA  = 50
		self.PB  = 50
		self.speed = 1.0
		self.turn_speed = 1.0
		self.gotoing = False

		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(self.AIN1,GPIO.OUT)
		GPIO.setup(self.AIN2,GPIO.OUT)
		GPIO.setup(self.BIN1,GPIO.OUT)
		GPIO.setup(self.BIN2,GPIO.OUT)
		GPIO.setup(self.ENA,GPIO.OUT)
		GPIO.setup(self.ENB,GPIO.OUT)
		self.PWMA = GPIO.PWM(self.ENA,500)
		self.PWMB = GPIO.PWM(self.ENB,500)
		self.PWMA.start(self.PA)
		self.PWMB.start(self.PB)
		self.stop()

	def forward(self):
		self.PWMA.ChangeDutyCycle(self.PA)
		self.PWMB.ChangeDutyCycle(self.PB)
		GPIO.output(self.AIN1,GPIO.LOW)
		GPIO.output(self.AIN2,GPIO.HIGH)
		GPIO.output(self.BIN1,GPIO.LOW)
		GPIO.output(self.BIN2,GPIO.HIGH)


	def stop(self):
		self.PWMA.ChangeDutyCycle(0)
		self.PWMB.ChangeDutyCycle(0)
		GPIO.output(self.AIN1,GPIO.LOW)
		GPIO.output(self.AIN2,GPIO.LOW)
		GPIO.output(self.BIN1,GPIO.LOW)
		GPIO.output(self.BIN2,GPIO.LOW)

	def backward(self):
		self.PWMA.ChangeDutyCycle(self.PA)
		self.PWMB.ChangeDutyCycle(self.PB)
		GPIO.output(self.AIN1,GPIO.HIGH)
		GPIO.output(self.AIN2,GPIO.LOW)
		GPIO.output(self.BIN1,GPIO.HIGH)
		GPIO.output(self.BIN2,GPIO.LOW)

		
	def left(self):
		self.PWMA.ChangeDutyCycle(30/2)
		self.PWMB.ChangeDutyCycle(30/2)
		GPIO.output(self.AIN1,GPIO.HIGH)
		GPIO.output(self.AIN2,GPIO.LOW)
		GPIO.output(self.BIN1,GPIO.LOW)
		GPIO.output(self.BIN2,GPIO.HIGH)


	def right(self):
		self.PWMA.ChangeDutyCycle(30/2)
		self.PWMB.ChangeDutyCycle(30/2)
		GPIO.output(self.AIN1,GPIO.LOW)
		GPIO.output(self.AIN2,GPIO.HIGH)
		GPIO.output(self.BIN1,GPIO.HIGH)
		GPIO.output(self.BIN2,GPIO.LOW)


	def advance(self, duration=1.0):
		DR = 16
		DL = 19

		logger.info(f"Advance {duration}")

		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(DR, GPIO.IN, GPIO.PUD_UP)
		GPIO.setup(DL, GPIO.IN, GPIO.PUD_UP)

		start_time = time.time()
		while time.time() - start_time < duration:
			DR_status = GPIO.input(DR)
			DL_status = GPIO.input(DL)
			logger.info(f"DL: {DL_status}, DR: {DR_status}")

			if DL_status == 0:
				logger.info("Obstacle detected on the left. Turning right.")
				self.turn_left(float(self.get_rotation_time(45)))  # Turn right for 90 degrees
			elif DR_status == 0:
				logger.info("Obstacle detected on the right. Turning left.")
				self.turn_right(float(self.get_rotation_time(45)))  # Turn left for 90 degrees
			else:
				self.setPWMA(7.8*1.5)
				self.setPWMB(7.8*1.5)
				self.forward()
				time.sleep(0.1)  # Move forward for a short time

		self.stop()


	def get_move_time(self, dist):
		return dist / self.speed

	
	def get_rotation_time(self, angle):
		return abs(angle) / self.turn_speed


	def turn_left(self, turn_time):
		self.left()
		logger.info(f"Turning left for {turn_time} seconds")
		time_before = time.time()
		time.sleep(turn_time)
		time_after = time.time()
		logger.info(f"Time taken to turn left: {time_after - time_before} seconds")
		self.stop()


	def turn_right(self, turn_time):
		self.right()
		logger.info(f"Turning right for {turn_time} seconds")
		time_before = time.time()
		time.sleep(turn_time)
		time_after = time.time()
		logger.info(f"Time taken to turn right: {time_after - time_before} seconds")
		self.stop()

	def get_angle_between(self, x1, y1, x2, y2):
		angle = math.atan2(x2 - x1, y2 - y1)
		angle = math.degrees(angle)  # Convert to degrees
		angle = angle % 360  # Normalize angle to [0, 360)
		return angle 


	def goto(self, x1, y1, x2, y2, curr_angle, max_time=0.25):
		if self.gotoing == True:
			return 0

		self.gotoing = True
		self.stop()
		sleep_time = 0.1
		angle = self.get_angle_between(x1, y1, x2, y2)

		logger.info(f"Current angle: {curr_angle}")
		logger.info(f"x1: {x1}, y1: {y1}, x2: {x2}, y2: {y2}")
		logger.info(f"Angle x1,y1 towards x2,y2 = {angle}")


		rot_angle = angle - curr_angle
		if rot_angle > 180:
			rot_angle -= 360
		elif rot_angle < -180:
			rot_angle += 360

		logger.info(f"Turning {rot_angle}")

		spent_time = 0
		if abs(rot_angle) > 3:
			rotation_time = float(self.get_rotation_time(rot_angle))
			# rotation_time = 0.19
			logger.info(f"ROTATION TIME {rotation_time}")
			if rot_angle > 0:
				self.turn_left(rotation_time)
			else:
				self.turn_right(rotation_time)

			time.sleep(sleep_time)

			spent_time += rotation_time + sleep_time

		dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
		if dist > 0:
			move_time = self.get_move_time(dist)
			logger.info(f"Move time: {move_time}")
			# move_time = max(0, min(move_time, max_time - spent_time))
			logger.info(f"Real Move time: {move_time}")
			self.advance(min(move_time, max_time))
		self.stop()

		# time.sleep(0.3)

		self.gotoing = False

		return angle


	def setPWMA(self,value):
		self.PA = value
		self.PWMA.ChangeDutyCycle(self.PA)


	def setPWMB(self,value):
		self.PB = value
		self.PWMB.ChangeDutyCycle(self.PB)	

	def setSpeed(self, speed):
		self.speed = speed

	def setTurnSpeed(self, turn_speed):
		self.turn_speed = abs(turn_speed)

	def setMotor(self, left, right):
		if((right >= 0) and (right <= 100)):
			GPIO.output(self.AIN1,GPIO.HIGH)
			GPIO.output(self.AIN2,GPIO.LOW)
			self.PWMA.ChangeDutyCycle(right)
		elif((right < 0) and (right >= -100)):
			GPIO.output(self.AIN1,GPIO.LOW)
			GPIO.output(self.AIN2,GPIO.HIGH)
			self.PWMA.ChangeDutyCycle(0 - right)
		if((left >= 0) and (left <= 100)):
			GPIO.output(self.BIN1,GPIO.HIGH)
			GPIO.output(self.BIN2,GPIO.LOW)
			self.PWMB.ChangeDutyCycle(left)
		elif((left < 0) and (left >= -100)):
			GPIO.output(self.BIN1,GPIO.LOW)
			GPIO.output(self.BIN2,GPIO.HIGH)
			self.PWMB.ChangeDutyCycle(0 - left)


if __name__=='__main__':
	Ab = AlphaBot2()
	Ab.advance(1)
	# angle = 0
	# waypoints = [
	# 	(0, 0),
	# 	(2, 0),
	# 	#(1, -1),
	# 	# (1, -2), 
	# 	# (2, -2),
	# 	# (2, -1),
	# ]

	# coordinates1 = (361, 79)
	# coordinates2 = (363, 253)

	# # Calculate the scaling factor and offset
	# x_scale = coordinates2[0] - coordinates1[0]
	# y_scale = coordinates2[1] - coordinates1[1]

	# x_offset = coordinates1[0]
	# y_offset = coordinates1[1]


	# def waypoint_to_pixel(waypoint):
	# 	x_pixel = x_offset + waypoint[0] * x_scale
	# 	y_pixel = y_offset + waypoint[1] * y_scale
	# 	return (x_pixel, y_pixel)

	# # map coordinates1 and coordinates2 to waypoints (0,0) and (1,0)


	# for i in range(len(waypoints) - 1):
	# 	pixel_waypoint1 = waypoint_to_pixel(waypoints[i])
	# 	pixel_waypoint2 = waypoint_to_pixel(waypoints[i+1])
	# 	angle = Ab.goto(waypoints[i][0]*0.2, waypoints[i][1]*0.2, waypoints[i + 1][0]*0.2, waypoints[i + 1][1]*0.2, angle)
	# 	#time.sleep(0.33)

	# # Ab.turn(90)


	# #Ab.stop()

	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		GPIO.cleanup()
