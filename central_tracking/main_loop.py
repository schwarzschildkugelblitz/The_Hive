"""
By Mudit Aggarwal (2021-09-06 01:07:00)
Main file for central tracking system, controls the 3 main
components of the system:
	Camera (Marker detection using Aruco)
	Serial Communication with arduino
	Control system for commands

Dependencies:
	pip install opencv

	marker_detection
	serial_communication
	control_system
"""

import cv2
from marker_detection import Camera
from serial_communication import Serial_Communication
from control_system import Control_System

"""
The width and height of final processed window is to be d
determined manually as it is a function of required/available
resolution of camera and absolute width and height of arena
"""
width, height = int(44*800/34.5), int(24*800/34.5)

#initliazing the 3 mian components of tracking system
camera = Camera(width = width,
				height = height,
				camera = 3)
# arduino = Serial_Communication("COM4", 115200)
control = Control_System(width, height)

def main():
	#detects corners and unwarps the image
	camera.detect_corners()

	#Main loop of the system, is run until manually terminated
	while camera.capture.isOpened():
		
		# markers, labels = camera.test_markers()
		markers, labels = camera.detect_markers()

		# print(markers, labels)
		# signal = control.command(markers, labels)

		#Placeholder/ TODO
		# print(signal)
		# arduino.send(signal)

		#exit condition, press key 'd'd
		if cv2.waitKey(22) & 0xFF == ord('d'):
			break

	# arduino.send(b"232 0\n") #Stop for robot 0
	# arduino.send(b"232 0\n") #Stop for robot 0
	# arduino.send(b"232 0\n") #Stop for robot 0
	# arduino.send(b"232 0\n") #Stop for robot 0
	# arduino.send(b"232 0\n") #Stop for robot 0
	# arduino.send(b"232 0\n") #Stop for robot 0
	# arduino.send(b"232 0\n") #Stop for robot 0

	camera.capture.release()

if __name__ == "__main__":
	main()