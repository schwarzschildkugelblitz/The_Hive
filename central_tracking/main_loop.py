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
The width and height of final processed window is to be 
determined manually as it is a function of required/available
resolution of camera and absolute width and height of arena
"""
width, height = 640, 320

#initliazing the 3 mian components of tracking system
camera = Camera(width = width,
				height = height,
				camera = 0)
arduino = Serial_Communication("COM4", 912600)
control = Control_System(width, height)

def main():
	#detects corners and unwarps the image
	camera.detect_corners()

	#Main loop of the system, is run until manually terminated
	while camera.capture.isOpened():
		markers, labels = camera.detect_markers()
		print(markers, labels)

		#Placeholder/ TODO
		arduino.send(b"0")

		#exit condition, press key 'd'
		if cv2.waitKey(20) & 0xFF == ord('d'):
			break
	camera.capture.release()

if __name__ == "__main__":
	main()