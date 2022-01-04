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
import cv2
from marker_detection import Camera
from serialcommunication import SerialCommunication
from control_system import ControlSystem

"""
The width and height of final processed window is to be d
determined manually as it is a function of required/available
resolution of camera and absolute width and height of arena
"""
# width, height = int(44*800/34.5), int(24*800/34.5)
# width, height = 600, 300
width, height = 750, 700
extra_height = 10

# initializing the 3 main components of tracking system
camera = Camera(width=width, height=height, camera=1, extra_height=extra_height)
arduino = SerialCommunication("COM11", 115200)
control = ControlSystem(width, height)


def main():
    # detect corners and unwarp the image
    camera.detect_corners()

    # Main loop of the system, is run until manually terminated
    while True:

        # markers, labels = camera.test_markers()
        markers, labels = camera.detect_markers()

        # print(markers, labels)
        signal = control.command(markers, labels)

        # Placeholder
        # print(signal)
        arduino.send(signal)
        print(signal)

        # exit condition, press key 'd'
        if cv2.waitKey(20) & 0xFF == ord('d'):
            break

    camera.capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
