"""
By Mudit Aggarwal
Main file for central tracking system, controls the 3 main
components of the system:
    Camera (Marker detection using Aruco)
    Serial Communication with arduino
    Control system for commands

Dependencies:
    pip install opencv

    marker_detection
    control_system
    serial_communication
"""
import time
import cv2
from marker_detection import Camera
from serialcommunication import SerialCommunication
from control_system import ControlSystem

from multiprocessing import Process, Pipe

"""
The width and height of final processed window is to be d
determined manually as it is a function of required/available
resolution of camera and absolute width and height of arena
"""

width, height = 750, 700
extra_height = 10

# initializing the 3 main components of tracking system
camera = Camera(width=width, height=height, camera=1, extra_height=extra_height)
control = ControlSystem(width, height)


def send_signal(conn):

    arduino = SerialCommunication("COM11", 115200)

    while True:
        signals = conn.recv()

        for signal in signals:
            arduino.send(signal)
            # print(signal)
            time.sleep(0.01)


def main(conn):
    # detect corners and unwarp the image
    camera.detect_corners()

    # Main loop of the system, is run until manually terminated
    while True:

        # markers, labels = camera.test_markers()

        markers, labels, video_feed = camera.detect_markers()

        signals = control.command(markers, labels)
        control.draw_packages(video_feed)

        conn.send(signals)

        cv2.imshow("Arena", video_feed)

        # exit condition, press key 'd'
        if cv2.waitKey(50) & 0xFF == ord('d'):
            break

    camera.capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parent_conn, child_conn = Pipe()
    serial_process = Process(target=send_signal, args=(child_conn,))
    serial_process.daemon = True
    serial_process.start()

    main(parent_conn)

    serial_process.join()
    exit()
