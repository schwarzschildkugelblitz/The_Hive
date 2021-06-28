'''
By Mudit Aggarwal (2021-06-29 01:19:00)
for making ArUco markers according to given dictionary

The aruco module is based on the ArUco library, a popular library for detection of 
square fiducial markers developed by Rafael Muñoz and Sergio Garrido

Dependencies:
	pip install opencv-contrib-python
	pip install scikit-image
'''

import cv2
import cv2.aruco as aruco

#Dictionary MUST be same as the one used for detection of markers
dictionary = aruco.getPredefinedDictionary(aruco.DICT_5X5_50)

for i in range(0, 6):
	markerImage = aruco.drawMarker(dictionary, i, 200)
	#Marker images stored with same name as their ids
	cv2.imwrite(f"markers/{i}.jpg", markerImage)