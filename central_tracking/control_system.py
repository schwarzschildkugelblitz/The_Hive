import cv2
import numpy as np
import time

from bot import Bot
from fetch_job import job_generator
from path_finder import PathFinder, locations, colors

robots = [4, 5, 6, 7]  # marker labels of robots

# proximity threshold to the target coordinate of path
threshold = 40


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

    commands = {'left': 56, 'right': 57, 'stop': 58, 'right_drop': 59, 'left_drop': 60, 'drop': 61, '180': 62}  # speed
    delay = {'left': 0.5, 'right': 0.5, 'stop': 0.5, 'right_drop': 2, 'left_drop': 2, 'drop': 1, '180': 1}  # delay

    return commands[bot_command], delay[bot_command]


def is_equal(arr_a, arr_b):
    """
    Function to compare equality of two arrays
    containing vectors
    """
    if len(arr_a) != len(arr_b):
        return False
    else:
        for i in range(len(arr_a)):
            a = arr_a[i]
            b = arr_b[i]

            if a[0] != b[0] or a[1] != b[1]:
                return False
        return True


class ControlSystem:
    """
    Manages all the commands to every robot
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.bots = [Bot(i, robots[i]) for i in range(4)]

        self.job = job_generator()
        self.path_finder = PathFinder(self.width, self.height)

        # PID (feedback) system variables
        self.filter_state = np.zeros(4, dtype=np.float32)
        self.integrator_state = np.zeros(4, dtype=np.float32)
        self.Kp = 0.0071 / 40
        self.Ki = 3.1364 / 40
        self.Kd = 0.14 / 40
        self.N = 4.5
        self.priority = [0, 1, 2, 3]

        self.signals = []
        self.bot_group = 0

    def command(self, detected_markers, detected_labels):
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

        self.signals = []
        self.priority = []

        for bot in self.bots:

            # iterate over all robots and store their coordinates
            if detected_labels is not None and bot.marker_id in detected_labels:
                bot.marker = detected_markers[list(detected_labels).index(bot.marker_id)][0]

            bot.set_center()

            if time.time() - bot.command_start < bot.command_delay:
                continue

            if bot.idle:
                job = next(self.job)
                bot.payload = job[0]
                bot.target, bot.next_target = job[1], job[2]
                if bot.id == 0: # or bot.id == 1:
                    bot.path, bot.commands = self.path_finder.get_path(bot.target, bot.coords,
                                                                       bot.marker[0], bot.marker[3])
                    bot.path_color = colors[locations[job[2]]]
                    if len(bot.path) > 0: # Boom Rohan
                        print(bot.id, bot.path, bot.commands, bot.target, bot.next_target)
                bot.idle = False
                
                # if bot.id == 1:
                #     print(bot.path, bot.commands, bot.target, bot.next_target)

            if bot.next_target is not None and bot.path is not None:
                self.priority.append(bot.id)

            if bot.transition:
                bot.path, bot.commands = self.path_finder.get_path(bot.target, bot.coords,
                                                                   bot.marker[0], bot.marker[3])
                bot.transition = False
                if bot.path is not None:
                    print(bot.id, bot.path, bot.commands, bot.target, bot.next_target)

            # bot.blocked = False
            bot.set_angle()

        self.priority.sort(key=lambda bot_id: self.path_finder.get_induction_distance(self.bots[bot_id].path))
        for bot in self.bots:
            if bot.id not in self.priority:
                self.priority.append(bot.id)

        self.priority = self.priority[::-1]

        for bot in self.bots[self.bot_group:self.bot_group + 1]:

            if time.time() - bot.command_start < bot.command_delay:
                continue

            if bot.target_dist() < threshold or bot.step >= len(bot.commands):
                try:
                    bot.old_target = bot.path[bot.step]
                except IndexError:
                    bot.old_target = bot.path[-1]

                bot.command_start = time.time()
                speed, bot.command_delay = special_command(bot.get_command())
            else:
                speed = self.pid(bot)

            if bot.old_target_dist() < threshold:
                self.integrator_state[bot.id] = 0.0
                self.filter_state[bot.id] = 0.0

            for high_priority_bot_id in self.priority[self.priority.index(bot.id):]:
                if high_priority_bot_id != bot.id:
                    if bot.check_collision(self.bots[high_priority_bot_id]):
                        # print(f"{bot.id} is colliding with {high_priority_bot_id} at " +
                        #       f"{self.bots[high_priority_bot_id].coords}")
                        # print(self.bots[high_priority_bot_id].coords)
                        
                        # if bot.recalculate is None:
                        #     bot.blocked = True
                        #     bot.recalculate = time.time()

                        self.path_finder.set_block(self.bots[high_priority_bot_id].coords)
                        new_path, new_commands = self.path_finder.get_path(bot.target, bot.coords,
                                                                           bot.marker[0], bot.marker[3])
                        self.path_finder.reset_arena()
                        if new_path is None:
                            bot.blocked = True
                            if bot.blocking is not None:
                                self.bots[bot.blocking].blocked = False
                                self.bots[bot.blocking].blocked_by = None
                            continue
                        elif bot.blocked:
                            bot.blocked = False

                        if not is_equal(new_path, bot.path):
                            bot.step = 0
                            bot.path, bot.commands = new_path, new_commands


            # if bot.recalculate is not None and time.time() - bot.recalculate > 0.5:
                
            #     bot.blocked = False
            #     bot.recalculate = None
                
                

            if bot.blocked:
                # bot.command_start = time.time()
                self.integrator_state[bot.id] = 0.0
                self.filter_state[bot.id] = 0.0
                speed, bot.command_delay = special_command('stop')
            # if bot.id == 1:
                # print("Speed:",speed)
            speed_data = int(4 * abs(speed) + bot.id)
            speed_sign = 1 if speed < 0 else 0

            signal = bytes(str(speed_data) + ' ' + str(speed_sign) + '\n', 'utf-8')

            if speed > 55:
                self.signals.append(signal)
                self.signals.append(signal)
                # self.signals.append(signal)
                # self.signals.append(signal)

            self.signals.append(signal)

        # self.bot_group = (self.bot_group + 2) % 4
        return self.signals

    # noinspection PyPep8Naming
    def pid(self, bot):

        delta_t = time.time() - bot.last_time
        bot.last_time = time.time()

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

        speed = V * 45 / 1.8
        return np.round(speed)

    def draw_packages(self, video_feed):
        for bot in self.bots:
            if bot.id == 0: # or bot.id == 1:
                for i in range(len(bot.path) - 1):
                    cv2.line(video_feed, bot.path[i], bot.path[i + 1], bot.path_color[::-1], 4)
                if any(bot.coords != np.zeros(2)):
                    cv2.putText(video_feed, bot.payload, bot.coords.astype(np.int32), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                0.8,
                                bot.path_color[::-1], 1, cv2.LINE_8)
