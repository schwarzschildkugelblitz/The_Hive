import time

import numpy as np

collision_threshold = 225


def distance(p1, p2):
    """Returns distance between 2 points"""

    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


class Bot:
    def __init__(self, bot_id, marker_id):
        self.id = bot_id
        self.marker_id = marker_id
        self.marker = None
        self.coords = np.array([-1000, -1000], dtype=np.int32)
        self.idle = True
        self.payload = ""

        self.path = []
        self.commands = []
        self.step = 0
        self.angle = 0

        self.blocked = False
        self.blocked_by = None
        self.blocking = None
        self.recalculate = None

        self.transition = False
        self.target = None
        self.next_target = None
        self.command_start = time.time()
        self.command_delay = 0

        self.old_target = np.zeros(2)

        self.last_time = time.time()

        self.path_color = (0, 0, 0)

    def check_collision(self, other_bot):
        dist = distance(self.coords, other_bot.coords)
        if dist < collision_threshold and not (other_bot.blocked_by == self.id):
            other_bot.blocked = True
            other_bot.blocked_by = self.id
            self.blocking = other_bot.id
            return True

        if dist > collision_threshold and other_bot.blocked_by == self.id:
            other_bot.blocked = False
            other_bot.blocked_by = None
            self.blocking = None

        return False

    def get_command(self):
        try:
            command = self.commands[self.step]
        except IndexError:
            return 'stop'

        self.step += 1

        if self.step >= len(self.path):
            self.step = 0
            if self.next_target is None:
                self.idle = True
            else:
                self.target = self.next_target
                self.next_target = None
                self.transition = True

        return command

    def set_center(self, ):
        """
        Returns skewed center of marker to match closely to the center of the robot
        Requires tuning (TODO)
        """
        if self.marker is None:
            # Bot is not initialized / not visible
            return

        self.coords[0] = (self.marker[0][0] * 3 + self.marker[1][0] * 3 + self.marker[2][0] + self.marker[3][0]) // 8
        self.coords[1] = (self.marker[0][1] * 3 + self.marker[1][1] * 3 + self.marker[2][1] + self.marker[3][1]) // 8

    def set_angle(self, ):
        """
        Returns angle between 2 lines formed by the points
        a0 with a1 and b0 with b1
        A unit vector is created and angle is calculated using dot product
        Output type -> degrees
        """
        try:
            a0 = self.marker[3]
            a1 = self.marker[0]
            b0 = self.coords
        except TypeError:
            a0, a1, b0 = [[0, 0]] * 3
        try:
            b1 = self.path[self.step]
        except IndexError:
            self.angle = 0.0
            return
        # except TypeError:
        #     self.angle = 0.0
        #     return

        mag_a = distance(a0, a1) + 0.0001
        va = ((a1[1] - a0[1]) / mag_a, (a1[0] - a0[0]) / mag_a)

        mag_b = distance(b0, b1) + 0.0001
        vb = ((b1[1] - b0[1]) / mag_b, (b1[0] - b0[0]) / mag_b)

        angle = np.arccos(np.clip(np.dot(va, vb), -1.0, 1.0))

        if va[0] * vb[1] - va[1] * vb[0] < 0:
            angle = -angle

        self.angle = np.round(np.rad2deg(angle), decimals=0)

    def target_dist(self):
        """
        Returns distance to next target point
        """

        try:
            return distance(self.coords, self.path[self.step])
        except IndexError:
            return float('NaN')

    def old_target_dist(self):
        """
        Returns distance to next target point
        """

        try:
            return distance(self.coords, self.old_target)
        except IndexError:
            return float('NaN')
