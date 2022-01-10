""" this code was written by Harshit Batra and Rohan Deswal 

as part of hive round 2 """
import pygame
from math import atan2, pi
import random
from astar import astar

locations = {
    'Mumbai': 1,
    'Delhi': 2,
    'Kolkata': 3,
    'Chennai': 4,
    'Bengaluru': 5,
    'Hyderabad': 6,
    'Pune': 7,
    'Ahmedabad': 8,
    'Jaipur': 9
}

locations_coords = {
    '1': (4, 0),
    '2': (9, 0),

    'Mumbai1': (1, 3),
    'Mumbai2': (1, 4),
    'Mumbai3': (2, 2),
    'Mumbai4': (3, 2),
    'Mumbai5': (4, 3),
    'Mumbai6': (4, 4),
    'Mumbai7': (2, 5),
    'Mumbai8': (3, 5),
    'Delhi1': (1, 7),
    'Delhi2': (1, 8),
    'Delhi3': (2, 9),
    'Delhi4': (3, 9),
    'Delhi5': (4, 8),
    'Delhi6': (4, 7),
    'Delhi7': (3, 6),
    'Delhi8': (2, 6),
    'Kolkata1': (1, 11),
    'Kolkata2': (1, 12),
    'Kolkata3': (2, 13),
    'Kolkata4': (3, 13),
    'Kolkata5': (4, 12),
    'Kolkata6': (4, 11),
    'Kolkata7': (3, 10),
    'Kolkata8': (2, 10),
    'Chennai1': (5, 3),
    'Chennai2': (5, 4),
    'Chennai3': (6, 5),
    'Chennai4': (7, 5),
    'Chennai5': (8, 4),
    'Chennai6': (8, 3),
    'Chennai7': (7, 2),
    'Chennai8': (6, 2),
    'Bengaluru1': (5, 7),
    'Bengaluru2': (5, 8),
    'Bengaluru3': (6, 9),
    'Bengaluru4': (8, 8),
    'Bengaluru5': (8, 8),
    'Bengaluru6': (8, 7),
    'Bengaluru7': (8, 6),
    'Bengaluru8': (7, 6),
    'Hyderabad1': (6, 6),
    'Hyderabad2': (5, 11),
    'Hyderabad3': (5, 12),
    'Hyderabad4': (6, 13),
    'Hyderabad5': (7, 13),
    'Hyderabad6': (8, 11),
    'Hyderabad7': (7, 10),
    'Hyderabad8': (6, 10),
    'Pune1': (9, 3),
    'Pune2': (9, 4),
    'Pune3': (10, 5),
    'Pune4': (11, 5),
    'Pune5': (12, 4),
    'Pune6': (12, 3),
    'Pune7': (11, 2),
    'Pune8': (10, 2),
    'Ahmedabad1': (9, 7),
    'Ahmedabad2': (9, 8),
    'Ahmedabad3': (10, 9),
    'Ahmedabad4': (11, 9),
    'Ahmedabad5': (12, 8),
    'Ahmedabad6': (12, 7),
    'Ahmedabad7': (11, 6),
    'Ahmedabad8': (10, 6),
    'Jaipur1': (9, 11),
    'Jaipur2': (9, 12),
    'Jaipur3': (10, 13),
    'Jaipur4': (11, 13),
    'Jaipur5': (12, 12),
    'Jaipur6': (12, 11),
    'Jaipur7': (11, 10),
    'Jaipur8': (10, 10)
}

colors = {
    -2: (158, 0, 69),  # Node to Visit
    -1: (0, 0, 0),  # Blocked Cell
    0: (255, 255, 255),  # Empty Cell
    1: (171, 169, 166),  # Mumbai
    2: (25, 98, 224),  # Delhi
    3: (252, 223, 76),  # Kolkata
    4: (252, 158, 76),  # Chennai
    5: (243, 116, 247),  # Bengaluru
    6: (242, 19, 49),  # Hyderabad
    7: (51, 135, 68),  # Pune
    8: (145, 81, 35),  # Ahmedabad
    9: (119, 67, 191)  # Jaipur
}
arena = [[-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [-1, 0, 0, 1, 1, 0, 0, 2, 2, 0, 0, 3, 3, 0, 0],
         [-1, 0, 0, 1, 1, 0, 0, 2, 2, 0, 0, 3, 3, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [-1, 0, 0, 4, 4, 0, 0, 5, 5, 0, 0, 6, 6, 0, 0],
         [-1, 0, 0, 4, 4, 0, 0, 5, 5, 0, 0, 6, 6, 0, 0],
         [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [-1, 0, 0, 7, 7, 0, 0, 8, 8, 0, 0, 9, 9, 0, 0],
         [-1, 0, 0, 7, 7, 0, 0, 8, 8, 0, 0, 9, 9, 0, 0],
         [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


def get_align_command(bot_coords, path_vectors):

    direction = [path_vectors[1][0] - path_vectors[0][0], path_vectors[1][1] - path_vectors[0][1]]
    bot_vector = [0, 0]
    if bot_coords[1] == 2 or bot_coords[1] == 6 or bot_coords[1] == 10:  # Facing Right
        bot_vector = [0, 1]
    elif bot_coords[1] == 5 or bot_coords[1] == 9 or bot_coords[1] == 13:  # Facing Left
        bot_vector = [0, -1]
    elif bot_coords[0] == 1 or bot_coords[0] == 5 or bot_coords[0] == 9:  # Facing Down
        bot_vector = [1, 0]
    elif bot_coords[0] == 4 or bot_coords[0] == 8 or bot_coords[0] == 12:  # Facing Up
        bot_vector = [-1, 0]

    if bot_vector[0] == 0 and bot_vector[1] == 0:
        raise Exception("Unexpected Bot Vector")
    angle = atan2(bot_vector[0] * direction[1] - bot_vector[1] * direction[0],
                  bot_vector[0] * direction[0] + bot_vector[1] * direction[1])

    if angle > 0:
        return ['left']

    return ['right']


def get_turns_only(path):
    # print('Full Path:',path)
    out = [path[0]]
    i = 0
    j = 1
    while i < len(path) - 1:
        while j < len(path):
            if path[i][0] != path[j][0] and path[i][1] != path[j][1]:
                out.append(path[j - 1])
                break
            j += 1
        i = j - 1
        j = i + 1

    return out + [path[-1]]


def get_drop_align(bot_vectors, path_vectors):
    # print('BV:',bot_vectors)
    a = (bot_vectors[1][0] - bot_vectors[0][0], bot_vectors[1][1] - bot_vectors[0][1])
    b = (path_vectors[1][0] - path_vectors[0][0], path_vectors[1][1] - path_vectors[0][1])

    angle = atan2(a[0] * b[1] - a[1] * b[0], a[0] * b[0] + a[1] * b[1])

    if angle > 0:
        return ['left_drop']
    elif angle < 0:
        return ['right_drop']
    return ['drop']


def get_turns(turns_only_path):

    turns = []

    for i in range(1, len(turns_only_path) - 1):

        a = (turns_only_path[i][0] - turns_only_path[i - 1][0], turns_only_path[i][1] - turns_only_path[i - 1][1])
        b = (turns_only_path[i + 1][0] - turns_only_path[i][0], turns_only_path[i + 1][1] - turns_only_path[i][1])

        angle = atan2(a[0] * b[1] - a[1] * b[0], a[0] * b[0] + a[1] * b[1])
        # print(angle)
        if angle > 0:
            turns.append('left')
        else:
            turns.append('right')
    return turns


class PathFinder:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.rows = 14
        self.cols = 15
        self.scale = w // self.cols
        self.points_to_visit = []
        self.calculate_path = False
        self.calculate_button_coord = (3 * self.scale, self.rows * self.scale)
        self.reset_button_coord = (11 * self.scale, self.rows * self.scale)
        self.path = []
        self.new_blocks = []

    def draw_path(self):
        pygame.init()

        game_display = pygame.display.set_mode((self.width, self.height + self.scale))
        pygame.display.set_caption('A* Path Show')

        clock = pygame.time.Clock()
        crashed = False
        while not crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        crashed = True

                # Press Events
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:  # Set Nodes to Visit In Order
                        if not self.calculate_path:
                            x, y = pygame.mouse.get_pos()
                            if y // self.scale < self.rows and x // self.scale < self.cols and \
                                    arena[y // self.scale][x // self.scale] == 0:
                                self.points_to_visit.append([y // self.scale, x // self.scale])
                    if event.button == 1:  # Find Path Button or Reset
                        x, y = pygame.mouse.get_pos()
                        if self.calculate_button_coord[0] <= x <= self.calculate_button_coord[0] + self.scale and \
                                self.calculate_button_coord[1] <= y <= self.calculate_button_coord[1] + self.scale:
                            self.calculate_path = True

                # Release Events
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # Find Path Button or Reset
                        x, y = pygame.mouse.get_pos()
                        print('(', y // self.scale, ',', x // self.scale, ')')
                        if self.calculate_button_coord[0] <= x <= self.calculate_button_coord[0] + self.scale and \
                                self.calculate_button_coord[1] <= y <= self.calculate_button_coord[1] + self.scale and \
                                self.calculate_path:
                            # print('\nNodes:', self.points_to_visit)
                            self.path = astar(arena, self.points_to_visit[0], self.points_to_visit[1], None)
                            # print('Path:', self.path)

                        if self.reset_button_coord[0] <= x <= self.reset_button_coord[0] + self.scale and \
                                self.reset_button_coord[1] <= y <= self.reset_button_coord[1] + self.scale:
                            self.calculate_path = False
                            for point in self.points_to_visit:
                                arena[point[0]][point[1]] = 0
                            self.points_to_visit = []
                            self.path = []

                            # print("Nodes after Reset:", self.points_to_visit)
                            # print("Path after Reset:", self.path)

            game_display.fill((255, 255, 255))
            for i in range(self.rows):
                for j in range(self.cols):
                    color = colors[arena[i][j]]
                    pygame.draw.rect(game_display, color, pygame.Rect(j * self.scale, i * self.scale,
                                                                      self.scale, self.scale))
                    pygame.draw.rect(game_display, (0, 0, 0), pygame.Rect(j * self.scale, i * self.scale,
                                                                          self.scale, self.scale), 2)
            # Draw Path
            for cell in self.path:
                pygame.draw.rect(game_display, (0, 0, 0), pygame.Rect(cell[1] * self.scale, cell[0] * self.scale,
                                                                      self.scale, self.scale))
            for cell in self.points_to_visit:
                pygame.draw.rect(game_display, (0, 0, 0), pygame.Rect(cell[1] * self.scale, cell[0] * self.scale,
                                                                      self.scale, self.scale))

            # Calculate Path Button
            x, y = pygame.mouse.get_pos()
            if self.calculate_button_coord[0] <= x <= self.calculate_button_coord[0] + self.scale and \
                    self.calculate_button_coord[1] <= y <= self.calculate_button_coord[1] + self.scale:
                color = (0, 255, 0)
            else:
                color = (224, 189, 139)
            textobj = set_text('O', self.calculate_button_coord[0] + self.scale // 2,
                               self.calculate_button_coord[1] + self.scale // 2, 50)
            pygame.draw.rect(game_display, color,
                             pygame.Rect(self.calculate_button_coord[0],
                                         self.calculate_button_coord[1], self.scale, self.scale))
            pygame.draw.rect(game_display, (0, 0, 0),
                             pygame.Rect(self.calculate_button_coord[0],
                                         self.calculate_button_coord[1], self.scale, self.scale), 2)
            game_display.blit(textobj[0], textobj[1])

            # Reset Path Button
            x, y = pygame.mouse.get_pos()
            if self.reset_button_coord[0] <= x <= self.reset_button_coord[0] + self.scale and \
                    self.reset_button_coord[1] <= y <= self.reset_button_coord[1] + self.scale:
                color = (255, 0, 0)
            else:
                color = (224, 189, 139)
            textobj = set_text('X', self.reset_button_coord[0] + self.scale // 2,
                               self.reset_button_coord[1] + self.scale // 2, 50)
            pygame.draw.rect(game_display, color,
                             pygame.Rect(self.reset_button_coord[0], self.reset_button_coord[1],
                                         self.scale, self.scale))
            pygame.draw.rect(game_display, (0, 0, 0),
                             pygame.Rect(self.reset_button_coord[0], self.reset_button_coord[1],
                                         self.scale, self.scale), 2)
            game_display.blit(textobj[0], textobj[1])
            pygame.display.update()
            clock.tick(60)

        pygame.quit()
        quit()

    def get_path(self, induction, target, location):

        paths = []
        all_turns = []
        bot_coords = [location[1] // self.scale, location[0] // self.scale]
        start = locations_coords[induction]
        min_turns = float('inf')
        min_ind = 0
        for i in range(1, 9):
            end = locations_coords[target + str(i)]
            path = astar(arena, start, end, locations[target])
            path = get_turns_only(path)
            turns = get_turns(path)
            curr_min = len(turns)
            paths.append(path)
            all_turns.append(turns)

            if curr_min < min_turns:
                min_turns = curr_min
                min_ind = i
            path = []

        # Path from bot to induction
        path_1 = get_turns_only(astar(arena, bot_coords, locations_coords[induction], None))
        turns_1 = get_turns(path_1)

        # Path from induction to location
        path_2 = paths[min_ind]
        turns_2 = all_turns[min_ind]

        final_cell = path_2[-1]

        row = final_cell[0]
        col = final_cell[1]

        if arena[row + 1][col] != 0:
            path_vectors = [[row, col], [row + 1, col]]

        elif arena[row - 1][col] != 0:
            path_vectors = [[row, col], [row - 1, col]]

        elif arena[row][col + 1] != 0:
            path_vectors = [[row, col], [row, col + 1]]

        else:
            path_vectors = [[row, col], [row, col - 1]]

        return self.convert_to_space(path_1[:-1] + path_2), get_align_command(bot_coords, path_1[:2]) + turns_1 + [
            '180'] + turns_2 + get_drop_align(path_2[-2:], path_vectors)

    def set_blocks(self, blocks):

        for block in blocks:
            arena[block[1] // self.scale][block[0] // self.scale] = -3
            self.new_blocks.append([block[1] // self.scale, block[0] // self.scale])

    def reset_arena(self):

        for block in self.new_blocks:
            arena[block[0]][block[1]] = 0
        self.new_blocks = []

    def convert_to_space(self, points):
        space_points = []
        for point in points:
            space_points.append([point[1] * self.scale + self.scale // 2, point[0] * self.scale + self.scale // 2])
        return space_points


def set_text(string, coordx, coordy, font_size):  # Function to set text

    font = pygame.font.Font('freesansbold.ttf', font_size)
    text = font.render(string, True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (coordx, coordy)
    return text, text_rect


if __name__ == '__main__':
    P = PathFinder(750, 700)
    print(P.get_path('1', 'Kolkata', [175, 75]))
