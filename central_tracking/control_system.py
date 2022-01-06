import cv2
import numpy as np
from time import time
from queue import Full

from bot import Bot
from fetch_job import job_generator

robots = [4, 5, 6, 7]  # marker labels of robots

# Path for each robot to follow
path = [
    np.array([(8.5 / 20, 8.5 / 10), (2.5 / 20, 8.5 / 10), (8.5 / 20, 8.5 / 10), (8.5 / 20, 0.5 / 10)]),
    np.array([(14.5 / 15, 4.5 / 14), (14.5 / 15, 6.5 / 14), (0.5 / 15, 6.5 / 14)]),
    np.array([(14.5 / 15, 6.5 / 14), (14.5 / 15, 8.5 / 14), (0.5 / 15, 8.5 / 14)]),
    np.array([(11.5 / 20, 8.5 / 10), (17.5 / 20, 8.5 / 10), (11.5 / 20, 8.5 / 10), (11.5 / 20, 0.5 / 10)])
]

# special command for each robot after each step through path
bot_commands = [['right', 'drop', 'left', 'stop'],
                ['right', 'right', 'stop'],
                ['right', 'right', 'stop'],
                ['left', 'drop', 'right', 'stop']]

# proximity threshold to the target coordinate of path
threshold = 75


def special_command(bot_command):
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
    # TODO implement delay = {'left': 1, 'right': 1, 'stop': 0, 'drop': 3}

    return commands[bot_command]


class ControlSystem:
    """
    Manages all the commands to every robot
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.bots = [Bot(i, robots[i]) for i in range(4)]

        self.job = job_generator()

        for i, robo_path in enumerate(path):
            for target_point in robo_path:
                target_point[0] *= self.width
                target_point[1] *= self.height

            self.bots[i].path = robo_path
            self.bots[i].commands = bot_commands[i]

        # PID (feedback) system variables
        self.filter_state = np.zeros(4, dtype=np.float32)
        self.integrator_state = np.zeros(4, dtype=np.float32)
        self.Kp = 0.01
        self.Ki = 0.0008
        self.Kd = 0.0002
        self.N = 3.3

        self.priority = [0, 1, 2, 3]

    def command(self, detected_markers, detected_labels, queue):
        """
        Generates and returns commands for the robots.
        Robots need to reach the next target in their respective paths
        to account for any deviation, a correction system (based on PID)
        is used which constantly corrects for the angle of robot with the current path

        parameters:
            markers -> np.float32 array storing coordinates of all points of markers of all robots
            labels -> aruco marker label of the robot with detected coordinates respectively

        returns:
            a byte string of uint8 numbers denoting the offset speed and sign of direction of robot
            e.g. "32 -1\n"
            here 32 is the speed offset for left and right motors of robot which helps
            it to turn and correct its angle

            -1 means the robot needs to turn clockwise for correction
            1 means the robot needs to turn anti-clockwise for correction
        """

        for bot in self.bots:
            # iterate over all robots and store their coordinates
            if detected_labels is not None and bot.marker_id in detected_labels:
                bot.marker = detected_markers[list(detected_labels).index(bot.marker_id)][0]

            if bot.idle:
                job = next(self.job)
                bot.payload = job[0]
                # TODO both.path = astar_something(bot.coords, *job[1:])
                bot.idle = False

        for bot in self.bots:
            bot.set_center()
            bot.set_angle()

            if bot.target_dist() < threshold:
                speed = special_command(bot.get_command())
                self.integrator_state[bot.id] = 0.0
            else:
                speed = self.pid(bot)

            for high_priority_bot_id in self.priority[self.priority.index(bot.id):]:
                if high_priority_bot_id != bot.id:
                    if bot.check_collision(self.bots[high_priority_bot_id]):
                        # TODO call pathfinding and get new path with high_priority robot as obstacle
                        speed = special_command('stop')

            speed_data = int(4 * abs(speed) + bot.id)
            speed_sign = 1 if speed < 0 else 0

            signal = bytes(str(speed_data) + ' ' + str(speed_sign) + '\n', 'utf-8')

            if bot.id == 2:
                print(bot.marker_id, speed, bot.path[bot.step])
                # print(bot.marker_id, speed, bot.path[bot.step])

            try:

                queue.put(signal)
            except Full:
                print("Hello 1")
                continue

    # noinspection PyPep8Naming
    def pid(self, bot):

        delta_t = time() - bot.last_time
        bot.last_time = time()

        theta = bot.angle

        D = (self.Kd * theta - self.filter_state[bot.id]) * self.N
        V = (self.Kp * theta + self.Ki * self.integrator_state[bot.id]) + D
        # self.integrator_state[bot] += self.Ki * theta * delta_t
        # self.filter_state[bot] += delta_t * D

        V = min(1.8, max(-1.8, V))
        if -40 < theta < 40:
            # self.integrator_state[bot] += self.Ki * theta * delta_t
            self.integrator_state[bot.id] += theta * delta_t
            self.filter_state[bot.id] += delta_t * D

            self.integrator_state[bot.id] = min(1.8, max(-1.8, self.integrator_state[bot.id]))
            self.filter_state[bot.id] = min(1.8, max(-1.8, self.filter_state[bot.id]))
        else:
            self.integrator_state[bot.id] = 0
            self.filter_state[bot.id] = 0

        speed = V * 55 / 1.8
        return np.round(speed)

    def draw_packages(self, video_feed):
        for bot in self.bots:
            if any(bot.coords != np.zeros(2)):
                cv2.putText(video_feed, bot.payload, bot.coords.astype(np.int32), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8,
                            (0, 0, 0), 1, cv2.LINE_8)
