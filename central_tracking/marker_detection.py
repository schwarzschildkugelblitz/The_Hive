"""
By Mudit Aggarwal
   Harshit Batra
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
# noinspection PyUnresolvedReferences
import cv2.aruco as aruco
import numpy as np
import time

# time at the beginning of program


def timer_and_fps(set_time, previous_time, req):
    """
    the function creates timer and gives current fps

    returns timer for req = "timer" or "Timer"
    returns current fps for req = "fps" or "FPS"
    """

    current_time = time.time()
    timer = int(current_time - set_time)
    fps = 1 / (current_time - previous_time)
    if req == "timer" or req == "Timer":
        return timer
    if req == "fps" or req == "FPS":
        return fps
    if req == "Previous_time":
        return current_time


def resize(scale_percent, img):
    """
    OpenCV image is resized to  given percent of its original width and height
    width and height are resized linearly, area is not taken into account

    scale_percent (float): percent by which to change width and height
    img (numpy array/openCV image): Image to resize

    returns resized image
    """
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)


def unwarp(img, src, dst):
    """
    From stackoverflow: https://stackoverflow.com/a/47830321
    Unwarps the image by directly mapping 4 points in src array to 4 points in dst array

    img (numpy array/OpenCV image): image onto which points will be mapped
    src (1x4 array): 4 corners of distorted quad to be mapped
    dst (1x4 array): 4 corners of destination quad

    returns unwarped image
    """
    h, w = img.shape[:2]
    # use cv2.getPerspectiveTransform() to get M, the transform matrix, and Minv, the inverse
    m = cv2.getPerspectiveTransform(src, dst)
    # use cv2.warpPerspective() to warp your image to a top-down view
    unwarped = cv2.warpPerspective(img, m, (w, h), flags=cv2.INTER_LINEAR)

    # returns unwarped frame
    return unwarped


class Camera:

    def __init__(self, width, height, camera=0, extra_height=0):

        # predefined dictionary for ArUco markers
        # for Robot application 5x5 grid with up to 50 Ids is chooses
        # for list of predefined dictionaries: https://docs.opencv.org/3.4/dc/df7/dictionary_8hpp.html
        # This MUST be same as the one chosen to make the markers
        self.dictionary = aruco.getPredefinedDictionary(aruco.DICT_5X5_50)

        # Initiate video capture at camera 0, if more than 1 camera
        # change accordingly
        self.camera = camera
        self.set_time = 0
        self.capture = cv2.VideoCapture(camera, cv2.CAP_DSHOW)

        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        # width and height of the rectangular arena
        # aspect ratio needs to maintained
        self.width, self.height = width, height
        self.extra_height = extra_height

        # initialized corners of border markers
        self.src = np.float32([(0, 0), (0, 0), (0, 0), (0, 0)])
        # Destination markers based on aspect ratio of arena
        self.dst = np.float32([(0, 0), (width, 0), (width, height + extra_height), (0, height + extra_height)])

        # Destination markers based on aspect ratio of arena

        self.markers_set = [0, 1, 11, 3]

    def detect_corners(self):
        """
        Detect the aruco markers in the corner of the image,
        the requisite pattern is:
        label 0 					label 1


        label 3 					label 2
        """

        got_corners = False

        while not got_corners:
            '''
            capture initial frame when all markers are visible
            src matrix is set according to this initial frame
            the 4 border markers are put to the corners and cannot be detected henceforth
            '''
            # break condition
            if cv2.waitKey(20) & 0xFF == ord('d'):
                break

            # read frame
            ret, frame = self.capture.read()
            # frame = cv2.flip(frame, 1)
            # print(frame.shape[:2])

            if not ret:
                raise Exception(f"Camera Exception {ret}")

            # detect positions of markers

            marker_positions_and_labels = aruco.detectMarkers(frame, self.dictionary)[0:2]

            positions = []
            labels = []

            if marker_positions_and_labels and marker_positions_and_labels[1] is not None:
                positions = [marker_positions_and_labels[0][i][0] for i in range(len(marker_positions_and_labels[0]))]
                labels = [lab[0] for lab in marker_positions_and_labels[1]]

            markers = aruco.drawDetectedMarkers(frame.copy(), marker_positions_and_labels[0])

            # show frame for testing camera position
            # loop is broken out of when all border markers are detectable
            markers_to_show = resize(50, markers)
            cv2.imshow("markers", markers_to_show)

            # try:
            if set(self.markers_set).issubset(set(labels)):
                '''Assume markers with ids 0, 1, 2 and 3 are at corners
                TOP-LEFT, TOP-RIGHT, BOTTOM-RIGHT and BOTTOM-LEFT respectively
                only these 4 markers are checked at this stage
                if these 4 markers are detected, got_corners is set to True

                TOP-LEFT corner of TOP-LEFT marker is considered
                TOP-RIGHT corner of TOP-RIGHT marker is considered
                BOTTOM-RIGHT corner of BOTTOM-RIGHT marker is considered
                BOTTOM-LEFT corner of BOTTOM-LEFT marker is considered'''
                got_corners = True
                for i, label in enumerate(labels):
                    if label in self.markers_set:
                        j = self.markers_set.index(label)
                        self.src[j] = positions[i][(j + 2) % 4]

        # except:
        # 	continue

        # destroy framing window
        cv2.destroyAllWindows()
        self.set_time = time.time()

    def test_markers(self):
        """
        Tests marker detection without setting got_markers variable
        for debugging and testing

        markers are not unwarped, just to test camera and marker coordinates
        """
        ret, frame = self.capture.read()

        # positions = []
        labels = []

        if not ret:
            raise Exception("Camera Exception")

        # detect positions of markers
        marker_positions_and_labels = aruco.detectMarkers(frame, self.dictionary)[0:2]

        if marker_positions_and_labels and marker_positions_and_labels[1] is not None:
            # positions = [marker_positions_and_labels[0][i][0] for i in range(len(marker_positions_and_labels[0]))]
            labels = [lab[0] for lab in marker_positions_and_labels[1]]

        markers = aruco.drawDetectedMarkers(frame.copy(), marker_positions_and_labels[0])

        # show frame for testing camera position
        # loop is broken out of when all border markers are detectable
        markers_to_show = resize(50, markers)
        cv2.imshow("markers", markers_to_show)

        return markers, labels

    def processed_video_text(self, src, previous_time):
        cv2.putText(src, 'Team PlaceHolders', (550, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 255), 2, cv2.LINE_4)
        cv2.putText(src, f'Time : {int(timer_and_fps(self.set_time, previous_time, "Timer"))} sec ',
                    (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2, cv2.LINE_4)
        cv2.putText(src, f'FPS : {int(timer_and_fps(self.set_time, previous_time, req="fps"))} ',
                    (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2, cv2.LINE_4)
        # previous_time = timer_and_fps(self.set_time, previous_time, "Previous_time")

    def detect_markers(self):
        """
        unwarped view of arena is captured and markers are detected
        border markers cannot be detected
        Markers inside the arena are detected and positions are stored and returned in 'markers' list

        Inner corners of every marker is considered and rectangle extracted and unwarped
        """
        previous_time = time.time()

        ret, frame = self.capture.read()

        # cv2.imshow("original", frame)

        # Frames must not be flipped or markers wont be detected
        # frame = cv2.flip(frame, 1)

        # unwarp image and crop according to arena aspect ratio
        # so markers appear to be square and not skewed rectangles
        unwarped_frame = unwarp(frame, self.src, self.dst)[:self.height + self.extra_height, :self.width]

        # unwarped_frame = np.concatenate((unwarped_frame1, unwarped_frame2), axis = 1)

        # detect position of markers
        # corresponding labels are in labels at same index
        markers, labels = aruco.detectMarkers(unwarped_frame, self.dictionary)[0:2]

        the_hive_processed_video = aruco.drawDetectedMarkers(unwarped_frame.copy(), markers)

        # Save videos
        # self.processed1.write(the_hive_processed_video)
        # self.processed2.write(the_hive_processed_video_with_grid)
        # self.original.write(frame)
        return markers, labels, the_hive_processed_video
