import numpy as np
from time import time

robots = [7, 8, 9, 10] #marker labels of robots

path = np.array([np.array([( 8.5/20, 0.5/10), ( 8.5/20, 8.5/10), ( 1.5/20, 8.5/10)], np.float32), 
		np.array([( 9.5/20, 0.5/10), ( 9.5/20, 9.5/10), ( 1.5/20, 9.5/10)], np.float32), 
		np.array([(10.5/20, 0.5/10), (10.5/20, 8.5/10), (18.5/20, 8.5/10)], np.float32), 
		np.array([(11.5/20, 0.5/10), (11.5/20, 9.5/10), (18.5/20, 9.5/10)], np.float32)])

class Control_System:
	"""
	Manages all the commands to every robot
	"""
	def __init__(self, width, height):
		self.width = width
		self.height = height

		path[:, :, 0] *= self.width
		path[:, :, 1] *= self.height

		self.markers = np.array([np.array([[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]], dtype = np.float32), 
								 np.array([[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]], dtype = np.float32), 
								 np.array([[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]], dtype = np.float32), 
								 np.array([[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]], dtype = np.float32)])
		self.angles = np.array([0.0, 0.0, 0.0, 0.0], dtype = np.float32)
		self.data = np.array([[0, 0],[0, 0],[0, 0],[0, 0]], dtype = np.uint8) #angle, distance

		self.filter_state = np.array([0.0, 0.0, 0.0, 0.0], dtype = np.float32)
		self.integrator_state = np.array([0.0, 0.0, 0.0, 0.0], dtype = np.float32)
		self.Kp, self.Ki, self.Kd, self.N = 0.0815, 0.0144, 0.032, 0
		self.last_time = time()

	def command(self, markers, labels):

		for i in range(len(robots)):
			if labels and robots[i] in labels:
				self.markers[i] = markers[list(labels).index(robots[i])]

		last_angles = self.angles.copy()

		for i in range(len(robots)):

			angle = np.arctan2((self.markers[i][0][1]-self.markers[i][1][1]),(self.markers[i][1][0]-self.markers[i][0][0]))
			angle -= np.arctan2((path[i][1][0]-path[i][0][0]),(path[i][1][1]-path[i][0][1]))
			angle *= 57.29
			self.angles[i] = angle

			# speed = self.pid(last_angles)
			speed = 0
			self.data[i][0] = 4*abs(speed) + i
			self.data[i][1] = 1 if speed < 0 else 0

		return bytes(str(self.data[0][0]) + ' ' + str(self.data[0][1]) + '\n', 'utf-8')

	def pid(self, last_angles):
		#TODO
		for i in range(len(robots)):
			delta_t = time() - self.last_time
			self.last_time = time()

			theta = self.angles[i]
			theta_last = last_angles[i]

			# D = (self.Kd * theta - self.filter_state[i]) * self.N
			D = self.Kd * (theta - theta_last)/delta_t
			V = self.Kp * theta + self.integrator_state[i] + D

			V = min(1.29, max(-1.29, V))

			self.integrator_state += self.Ki * theta * delta_t
			# self.filter_state += D*delta_t

			speed = V * 55/1.29
			return int(speed)

			
