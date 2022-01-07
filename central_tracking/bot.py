import time

import numpy as np

collision_threshold = 70

def distance(p1, p2):
    """Returns distance between 2 points"""

    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


class Bot:
    def __init__(self, bot_id, marker_id):
        self.id = bot_id
        self.marker_id = marker_id
        self.marker = np.zeros((4, 2), dtype=np.float32)
        self.coords = np.zeros(2, dtype=np.float32)

        self.path = []
        self.commands = []
        self.step = 0
        self.angle = 0

        self.last_time = time.time()

    def check_collision(self, other_bot):
        if distance(self.coords, other_bot.coords) < collision_threshold:
            return True

    def get_command(self):
        command = self.commands[self.step]
        self.step += 1

        if self.step == len(self.command):
            # TODO get new path
            pass

        return command

    def set_center(self, ):
        """
        Returns skewed center of marker to match closely to the center of the robot
        Requires tuning (TODO)
        """

        self.coords[0] = (self.marker[0][0] * 3 + self.marker[1][0] * 3 + self.marker[2][0] + self.marker[3][0]) // 8
        self.coords[1] = (self.marker[0][1] * 3 + self.marker[1][1] * 3 + self.marker[2][1] + self.marker[3][1]) // 8

    def set_angle(self, ):
        """
        Returns angle between 2 lines formed by the points
        a0 with a1 and b0 with b1
        A unit vector is created and angle is calculated using dot product
        Output type -> degrees
        """
        a0 = self.marker[3]
        a1 = self.marker[0]
        b0 = self.coords
        try:
            b1 = self.path[self.step]
        except IndexError:
            self.angle = 0.0
            return

        mag_a = distance(a0, a1) + 0.0001
        va = ((a1[1] - a0[1]) / mag_a, (a1[0] - a0[0]) / mag_a)

        mag_b = distance(b0, b1)
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