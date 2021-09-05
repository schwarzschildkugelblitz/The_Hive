import cv2
from marker_detection import Camera
from serial_communication import Serial_Communication
from control_system import Control_System

width, height = 640, 320

camera = Camera(width = width,
				height = height,
				camera = 0)
arduino = Serial_Communication("COM4", 912600)
control = Control_System(width, height)

def main():
	camera.detect_corners()

	while camera.capture.isOpened():
		markers, labels = camera.detect_markers()
		print(markers, labels)

		arduino.send(b"0")

		#exit condition, press key 'd'
		if cv2.waitKey(20) & 0xFF == ord('d'):
			break
	camera.capture.release()

if __name__ == "__main__":
	main()