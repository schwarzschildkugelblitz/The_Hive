import numpy as np
from time import time

robots = [7, 8, 9, 10]  # marker labels of robots

# Path for each robot to follow
path = np.array([
    np.array([( 8.5/20, 0.5/10), ( 8.5/20, 8.5/10), ( 2.5/20, 8.5/10), ( 8.5/20, 8.5/10), ( 8.5/20, 0.5/10)]),
    np.array([( 9.5/20, 0.5/10), ( 9.5/20, 9.5/10), ( 2.5/20, 9.5/10), ( 9.5/20, 9.5/10), ( 9.5/20, 0.5/10)]),
    np.array([(10.5/20, 0.5/10), (10.5/20, 9.5/10), (17.5/20, 9.5/10), (10.5/20, 9.5/10), (10.5/20, 0.5/10)]),
    np.array([(11.5/20, 0.5/10), (11.5/20, 8.5/10), (17.5/20, 8.5/10), (11.5/20, 8.5/10), (11.5/20, 0.5/10)])
])

# special command for each robot after each step through path
bot_commands = [['right', 'drop', 'left', 'stop'],
                ['right', 'drop', 'left', 'stop'],
                ['left', 'drop', 'right', 'stop'],
                ['left', 'drop', 'right', 'stop']]

# proximity threshold to the target coordinate of path
threshold = 70


def special_command(address, bot_command):
    """
    Special commands called after each step, the function looks up the command
    and returns it
    commands:
        left -> 90° anti-clockwise rotation
        right -> 90° clockwise rotation
        stop -> Halt the robot
        drop -> Drop the package and 180° turn
    """

    commands = {'left': 56, 'right': 57, 'stop': 58, 'drop': 59}  # speed
    delay = {'left': 1, 'right': 1, 'stop': 0, 'drop': 3}

    command_num = commands[bot_command] * 4
    command_num = command_num + address

    return bytes(str(command_num) + ' ' + '0' + '\n', 'utf-8'), delay[bot_command]


def distance(p1, p2):
    # Returns distance between 2 points

    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


def return_angle(a0, a1, b0, b1):
    """
    Returns angle between 2 lines formed by the the points
    a0 with a1 and b0 with b1
    A unit vector is created and angle is calculated using dot product
    Output type -> degrees
    """

    mag_a = distance(a0, a1)
    va = ((a1[1] - a0[1]) / mag_a, (a1[0] - a0[0]) / mag_a)

    mag_b = distance(b0, b1)
    vb = ((b1[1] - b0[1]) / mag_b, (b1[0] - b0[0]) / mag_b)

    angle = np.arccos(np.clip(np.dot(va, vb), -1.0, 1.0))

    if va[0] * vb[1] - va[1] * vb[0] < 0:
        angle = -angle

    return np.rad2deg(angle)


def return_center(marker):
    """
    Returns skewed center of marker to match closely to the center of the robot
    Requires tuning (TODO)
    """

    avg_x = (marker[0][0]*3 + marker[1][0]*3 + marker[2][0] + marker[3][0]) // 8
    avg_y = (marker[0][1]*3 + marker[1][1]*3 + marker[2][1] + marker[3][1]) // 8
    return avg_x, avg_y


class ControlSystem:
    """
    Manages all the commands to every robot
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height

        path[:, :, 0] *= self.width
        path[:, :, 1] *= self.height

        # markers will hold the coordinate data returned from camera system
        self.markers = np.zeros((4, 4, 2), dtype=np.float32)
        # angles will hold the angle of robots with current path(s)
        self.angles = np.zeros(4, dtype=np.float32)
        # data is he final data to be sent through radio to each robot
        self.data = np.zeros((4, 2), dtype=np.uint8)

        # PID (feedback) system variables
        self.filter_state = np.zeros(4, dtype=np.float32)
        self.integrator_state = np.zeros(4, dtype=np.float32)
        self.Kp = 0.0266
        self.Ki = 0.0031
        self.Kd = 0.005
        self.N = 13.97
        self.last_time = time()

        # to hold id of current bot and current step that bot is on
        self.current_bot = 0
        self.current_step = 0

        self.transition_begin = time()
        self.transition_delay = 0

    def command(self, markers, labels):
        """
        Generates and returns commands for the robots
        Robots need to reach the next target in their respective paths
        to account for any deviation, a correction system (based on PID)
        is used which constantly corrects for the angle of robot with the current path

        parameters:
            markers -> np.float32 array storing coordinates of all points of markers of all robots
            labels -> aruco marker label of the robot with detected coordinates respectively

        returns:
            a byte string of uint8 numbers denoting the offset speed and sign of direction of robot
            eg. "32 -1\n"
            here 32 is the speed offset for left and right motors of robot which helps
            it to turn and correct its angle

            -1 means the robot needs to turn clockwise for correction
            1 means the robot needs to turn anti-clockwise for correction
        """

        for i in range(len(robots)):
            # iterate over all robots and store their coordinates
            if labels is not None and robots[i] in labels:
                self.markers[i] = markers[list(labels).index(robots[i])]

        # Set current path and current target of current robot
        # changes after each step
        # current_path = (path[self.current_bot][self.current_step], path[self.current_bot][self.current_step + 1])
        current_path = (return_center(self.markers[self.current_bot]), path[self.current_bot][self.current_step + 1])
        current_target = path[self.current_bot][self.current_step + 1]

        # last_angle = self.angles[self.current_bot]

        # distance between current robot and current target of robot
        dist = distance(return_center(self.markers[self.current_bot]), current_target)
        print("Center of current robot:", return_center(self.markers[self.current_bot]),\
              "\nCoordinates of current target:", current_target,\
              "Distance of robot from current target:", dist)

        if dist < threshold:
            # if robot reached current target, a special command needs to be issued

            self.transition_begin = time()
            to_return, self.transition_delay = \
                special_command(self.current_bot, bot_commands[self.current_bot][self.current_step])
            self.angles[self.current_bot] = 0.0

            # increment current step so target and path can be updated
            self.current_step = (self.current_step + 1) % 4

            # if robot completed all its steps, increment current robot
            if self.current_step == 0:
                self.current_bot += 1

            return to_return

        # angle between current path and robot
        angle = return_angle(self.markers[self.current_bot][3], self.markers[self.current_bot][0],
                             current_path[0], current_path[1])
        print("Angle current robot with line joining the target to robot:", angle)
        self.angles[self.current_bot] = np.round(angle, decimals=1)

        if time() - self.transition_begin < self.transition_delay:
            # PID variables need to be re-initialized as path changed
            self.integrator_state[self.current_bot] = 0.0
            # self.filter_state[self.current_bot] = 0.0

        # speed offset between left and right motors, calculated through PID
        speed = self.pid()

        # Arrange and compress data to transmit to robots
        self.data[self.current_bot][0] = 4 * abs(speed) + self.current_bot
        self.data[self.current_bot][1] = 1 if speed < 0 else 0

        return bytes(str(self.data[self.current_bot][0]) + ' ' + str(self.data[self.current_bot][1]) + '\n', 'utf-8')

    def pid(self, last_angle = 0):

        delta_t = time() - self.last_time
        self.last_time = time()

        theta = self.angles[self.current_bot]

        # theta_last = last_angle

        # D = (self.Kd * theta - self.filter_state[i]) * self.N
        # D = self.Kd * (theta - theta_last) / 0.03
        # V = self.Kp * theta + self.integrator_state[self.current_bot] + D

        D = (self.Kd * theta - self.filter_state[self.current_bot]) * self.N
        V = (self.Kp * theta + self.integrator_state[self.current_bot]) + D
        self.integrator_state[self.current_bot] += self.Ki * theta * delta_t
        self.filter_state[self.current_bot] += delta_t * D

        V = min(1.29, max(-1.29, V))

        if -15 < theta < 15:
            self.integrator_state[self.current_bot] += self.Ki * theta * delta_t
        else:
            self.integrator_state[self.current_bot] = 0

        speed = V * 50 / 1.29
        return np.round(speed)


