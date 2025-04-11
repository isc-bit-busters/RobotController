import RPi.GPIO as GPIO
import time
import math

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
		self.PWMA.ChangeDutyCycle(30)
		self.PWMB.ChangeDutyCycle(30)
		GPIO.output(self.AIN1,GPIO.HIGH)
		GPIO.output(self.AIN2,GPIO.LOW)
		GPIO.output(self.BIN1,GPIO.LOW)
		GPIO.output(self.BIN2,GPIO.HIGH)


	def right(self):
		self.PWMA.ChangeDutyCycle(30)
		self.PWMB.ChangeDutyCycle(30)
		GPIO.output(self.AIN1,GPIO.LOW)
		GPIO.output(self.AIN2,GPIO.HIGH)
		GPIO.output(self.BIN1,GPIO.HIGH)
		GPIO.output(self.BIN2,GPIO.LOW)


	def advance(self, dist=1.0):
		DR = 16
		DL = 19

		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
		GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)

		for i in range(int(dist*10)):
			DR_status = GPIO.input(DR)
			DL_status = GPIO.input(DL)
			if(DL_status == 0):
				Ab.turn(90)
			elif(DR_status == 0):
				Ab.turn(-90)
			else:
				self.setPWMA(7.8)
				self.setPWMB(7.3)
				self.forward()
				time.sleep(12 * 0.1)



	def turn(self, deg):
		if deg > 0:
			self.left()
		else:
			self.right()
		time.sleep(abs(deg)/640.0)
		self.stop()


	def goto(self, x1, y1, x2, y2, curr_angle):
		angle = math.atan2(y2 - y1, x2 - x1) * 180 / math.pi
		rot_angle = angle - curr_angle
		if rot_angle > 180:
			rot_angle -= 360
		elif rot_angle < -180:
			rot_angle += 360

		self.turn(rot_angle)

		time.sleep(0.3)

		dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
		if dist > 0:
			self.advance(dist)
		self.stop()

		time.sleep(0.3)

		return angle


	def setPWMA(self,value):
		self.PA = value
		self.PWMA.ChangeDutyCycle(self.PA)


	def setPWMB(self,value):
		self.PB = value
		self.PWMB.ChangeDutyCycle(self.PB)	
		

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
	angle = 0
	waypoints = [
		(0, 0),
		(2, 0),
		#(1, -1),
		# (1, -2), 
		# (2, -2),
		# (2, -1),
	]

	coordinates1 = (361, 79)
	coordinates2 = (363, 253)

	# Calculate the scaling factor and offset
	x_scale = coordinates2[0] - coordinates1[0]
	y_scale = coordinates2[1] - coordinates1[1]

	x_offset = coordinates1[0]
	y_offset = coordinates1[1]


	def waypoint_to_pixel(waypoint):
		x_pixel = x_offset + waypoint[0] * x_scale
		y_pixel = y_offset + waypoint[1] * y_scale
		return (x_pixel, y_pixel)

	# map coordinates1 and coordinates2 to waypoints (0,0) and (1,0)


	for i in range(len(waypoints) - 1):
		pixel_waypoint1 = waypoint_to_pixel(waypoints[i])
		pixel_waypoint2 = waypoint_to_pixel(waypoints[i+1])
		angle = Ab.goto(waypoints[i][0]*0.2, waypoints[i][1]*0.2, waypoints[i + 1][0]*0.2, waypoints[i + 1][1]*0.2, angle)
		#time.sleep(0.33)

	# Ab.turn(90)


	#Ab.stop()

	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		GPIO.cleanup()
