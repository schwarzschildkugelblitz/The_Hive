"""
By Mudit Aggarwal (2021-06-29 01:19:00)
ArUco marker detection program, 
This program corrects distorted perspective of a rectangular plane
with ArUco markers at its corners. 
It can detect and output any valid ArUco marker in the selected dictionary

The aruco module is based on the ArUco library, a popular library for detection of 
square fiducial markers developed by Rafael Muñoz and Sergio Garrido

Dependencies:
	pip install opencv-contrib-python
	pip install numpy
	pip install scikit-image
"""

import cv2
import cv2.aruco as aruco
import numpy as np

def resize(scale_percent, img):
	'''
	Resize OpenCV image to given percent of its original width and height
	width and height are resized linearly, area is not taken into account

	scale_percent (float): percent by which to change width and height
	img (numpy array/openCV image): Image to resize

	returns resized image
	'''
	width = int(img.shape[1] * scale_percent / 100)
	height = int(img.shape[0] * scale_percent / 100)
	dim = (width, height)
	# resize image
	return cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

def unwarp(img, src, dst):
	'''
	From stackoverflow: https://stackoverflow.com/a/47830321
	Unwarps the image by directly mapping 4 points in src array to 4 points in dst array

	img (numpy array/OpenCV image): image onto which points will be mapped
	src (1x4 array): 4 corners of distorted quad to be mapped
	dst (1x4 array): 4 corners of dstination quad

	returns unwarped image
	'''
    h, w = img.shape[:2]
    # use cv2.getPerspectiveTransform() to get M, the transform matrix, and Minv, the inverse
    M = cv2.getPerspectiveTransform(src, dst)
    # use cv2.warpPerspective() to warp your image to a top-down view
    warped = cv2.warpPerspective(img, M, (w, h), flags=cv2.INTER_LINEAR)
    return warped

#predefined dictionary for ArUco markers
#for Robot application 5x5 grid with upto 50 Ids is choses
#for list of predefined dictionaries: https://docs.opencv.org/3.4/dc/df7/dictionary_8hpp.html
#This MUST be same as the one chosen to make the markers
dictionary = aruco.getPredefinedDictionary(aruco.DICT_5X5_50)

#Initiate video capture at camera 0, if more than 1 camera
#change accordingly
camera = 0
capture = cv2.VideoCapture(camera, cv2.CAP_DSHOW)

#width and height of the rectangular arena
#aspect ratio needs to maintained
width, height = 240, 365

#initialized corners of border markers
src = np.float32([(0, 0), (0, 0), (0, 0), (0, 0)])
#Destination markers based on aspect ratio of arena
dst = np.float32([(0, 0), (width, 0), (width, height), (0, height)])

got_corners = False
while not got_corners:
	'''
	capture initial frame when all markers are visible
	src matrix is set accroding to this initial frame
	the 4 border markers are put to the corners and cannot be detected henceforth
	'''
	#break condition
	if cv2.waitKey(20) & 0xFF == ord('d'):
		break

	#read frame
	ret, frame = capture.read()

	if not ret:
		raise Exception("Camera Exception")

	#detect positions of markers
	marker_positions_and_labels = aruco.detectMarkers(frame, dictionary)[0:2]
	marker_positions = [marker_positions_and_labels[0][i][0] for i in range(len(marker_positions_and_labels[0]))]
	marker_labels = [lab[0] for lab in marker_positions_and_labels[1]]

	markers = aruco.drawDetectedMarkers(frame.copy(), marker_positions_and_labels[0])

	#show frame for testing camera position
	#loop is broken out of when all border markers are detectable
	cv2.imshow("markers", markers)
	try:
		if set([0, 1, 2, 3]).issubset(set(marker_labels)):
			'''Assume markers with ids 0, 1, 2 and 3 are at corners
			TOP-LEFT, TOP-RIGHT, BOTTOM-RIGHT and BOTTOM-LEFT respectively
			only these 4 markers are checked at this stage
			if these 4 markers are detected, got_corners is set to True

			TOP-LEFT corner of TOP-LEFT marker is considered
			TOP-RIGHT corner of TOP-RIGHT marker is considered
			BOTTOM-RIGHT corner of BOTTOM-RIGHT marker is considered
			BOTTOM-LEFT corner of BOTTOM-LEFT marker is considered'''
			got_corners = True
			for i in range(len(marker_labels)):
				label = marker_labels[i]
				if label < 4:
					#update src depending on label of 4 markers
					src[label] = (marker_positions[i][label][0], marker_positions[i][label][1])
	except:
		continue

#destroy framing window
cv2.destroyAllWindows()

while capture.isOpened():
	'''
	unwarped view of arena is captured and markers are detected
	border markers cannot be detected
	Markers inside the arena are detected and positions are stored in 'markers' list
	'''
	ret, frame = capture.read()

	cv2.imshow("original", frame)
	#image cannot be flipped
	# frame = cv2.flip(frame, 1)

	#unwarp image and crop according to arena aspect ratio
	#so markers appear to be square and not skewed rectangles
	unwarped_frame = unwarp(frame, src, dst)[:height, :width]

	#detect position of markers
	#corresponding labels are in labels at same index
	markers, labels = aruco.detectMarkers(unwarped_frame, dictionary)[0:2]
	frame_with_markers = aruco.drawDetectedMarkers(unwarped_frame.copy(), markers[0])

	# for marker, label in zip(markers, labels):
	# 	print(marker, label)

	cv2.imshow("Top view frame with Markers", frame_with_markers)

	#exit condition, press key 'd'
	if cv2.waitKey(20) & 0xFF == ord('d'):
		break
capture.release()