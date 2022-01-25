""" this code was written by Harshit Batra and Rohan Deswal 

as part of hive round 2 """
import numpy as np
import pygame
from math import atan2, degrees
from astar import astar, Large_number_of_iterations
from path_gen import gen_path

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
    'Bengaluru4': (7, 9),
    'Bengaluru5': (8, 8),
    'Bengaluru6': (8, 7),
    'Bengaluru7': (6, 6),
    'Bengaluru8': (7, 6),

    'Hyderabad1': (8, 12),
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
    -3: (77, 53, 51), # Custom Blocks
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
         [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [-1, 0, 0, 4, 4, 0, 0, 5, 5, 0, 0, 6, 6, 0, 0],
         [-1, 0, 0, 4, 4, 0, 0, 5, 5, 0, 0, 6, 6, 0, 0],
         [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [-1, 0, 0, 7, 7, 0, 0, 8, 8, 0, 0, 9, 9, 0, 0],
         [-1, 0, 0, 7, 7, 0, 0, 8, 8, 0, 0, 9, 9, 0, 0],
         [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


def get_bot_angle(bot_top_left, bot_bottom_left):
    return atan2(bot_top_left[1] - bot_bottom_left[1], bot_top_left[0] - bot_bottom_left[0])


def get_align_command(bot_vector, path_vectors):
    angle_threshold = 45

    direction = [path_vectors[1][0] - path_vectors[0][0], path_vectors[1][1] - path_vectors[0][1]]

    angle = atan2(bot_vector[0] * direction[1] - bot_vector[1] * direction[0],
                  bot_vector[0] * direction[0] + bot_vector[1] * direction[1])

    angle = degrees(angle)
    # print("Angle:",angle)
    # print("Bot Vector:",bot_vector)
    # print("Direction:",direction)

    if abs(angle - 90) < angle_threshold:
        return ['left']
    elif abs(angle + 90) < angle_threshold:
        return ['right']
    elif not abs(angle) <= angle_threshold:
        return ['180']
    return ['stop']


def get_turns_only(path):
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


def get_distance(path):
    dist = 0
    for i in range(len(path) - 1):
        y1, x1 = path[i]
        y2, x2 = path[i + 1]

        dist += ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
    return dist


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
        self.line_path = []

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
                        if self.calculate_button_coord[0] <= x <= self.calculate_button_coord[0] + self.scale and \
                                self.calculate_button_coord[1] <= y <= self.calculate_button_coord[1] + self.scale and \
                                self.calculate_path:
                            self.line_path = gen_path(arena,self.points_to_visit[0], self.points_to_visit[1], self.rows, self.cols)
                            # print("Line Path:", self.line_path)
                        if self.reset_button_coord[0] <= x <= self.reset_button_coord[0] + self.scale and \
                                self.reset_button_coord[1] <= y <= self.reset_button_coord[1] + self.scale:
                            self.calculate_path = False
                            for point in self.points_to_visit:
                                arena[point[0]][point[1]] = 0
                            for point in self.new_blocks:
                                arena[point[0]][point[1]] = 0
                            self.points_to_visit = []
                            self.new_blocks = []
                            self.path = []
                            self.line_path = []

                    if event.button == 2: #set Blocks:
                        self.set_block(pygame.mouse.get_pos())


            game_display.fill((255, 255, 255))
            for i in range(self.rows):
                for j in range(self.cols):
                    color = colors[arena[i][j]]
                    if arena[i][j] != 0:
                        pygame.draw.rect(game_display, color, pygame.Rect(j * self.scale, i * self.scale,
                                                                      self.scale, self.scale))
                    pygame.draw.rect(game_display, (0, 0, 0), pygame.Rect(j * self.scale, i * self.scale,
                                                                          self.scale, self.scale), 2)
            for i in range(2):
                if len(self.points_to_visit) > 0:
                    try:
                        cell = self.points_to_visit[i]
                        if i == 0:
                            cell_color = (0,255,0)
                        else:
                            cell_color = (255,0,0)
                        pygame.draw.rect(game_display,cell_color, pygame.Rect(cell[1] * self.scale, cell[0] * self.scale,
                                                                              self.scale, self.scale))
                        pygame.draw.rect(game_display, (0, 0, 0), pygame.Rect(cell[1] * self.scale, cell[0] * self.scale,
                                                                              self.scale, self.scale), 2)
                    except:
                        pass
                        
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


            # Line Path Render
            for i in range(len(self.line_path)-1):
                cell_1 = self.line_path[i]
                cell_2 = self.line_path[i+1]
                y1,x1 = cell_1[0]*self.scale + self.scale//2, cell_1[1]*self.scale + self.scale//2
                y2,x2 = cell_2[0]*self.scale + self.scale//2, cell_2[1]*self.scale + self.scale//2
                pygame.draw.line(game_display,(0,0,0),[x1,y1],[x2,y2],3)

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


    def get_path(self, target, location, bot_top_left, bot_bottom_left):
        # print("Target: ",target,"Location:",location)
        bot_vector = [bot_top_left[1] - bot_bottom_left[1], bot_top_left[0] - bot_bottom_left[0]]
        start = [int(location[1]//self.scale), int(location[0]//self.scale)]
        if target == '1' or target == '2':
            end = locations_coords[target]
        else:
            min_dist = float('inf')
            min_ind = -1
            paths = []
            path_found = False
            for i in range(1,9):
                cur_path = gen_path(arena,start,locations_coords[target + str(i)],self.rows,self.cols)
                if cur_path is None:
                    paths.append(None)
                    continue
                path_found = True
                cur_dist = get_distance(cur_path)
                paths.append(cur_path)

                if cur_dist < min_dist:
                    min_dist = cur_dist
                    min_ind = i-1
            if not path_found:
                # print("inside get path not found")
                # print(np.array(arena))
                return None, None
            path = paths[min_ind]
            turns = get_turns(path)

            final_cell = path[-1]
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

            align_command = get_align_command(bot_vector, path[:2])
            drop_command = get_drop_align(path[-2:],path_vectors)

            outurns = align_command + turns + drop_command

            return self.convert_to_space(path,False,None),outurns

        path = gen_path(arena,start,end,self.rows,self.cols)
        if path is None:
            # print("Induction None")
            return None, None
        turns = get_turns(path)
        align_command = get_align_command(bot_vector, path[:2])

        outurns = align_command + turns

        if outurns[0] == '180' and outurns[1] == 'right':
            outurns = ['left']
            path = [path[0]] + [path[-1]]

        return self.convert_to_space(path,True,target),outurns + ['stop']

        # return self.convert_to_space(path,True,target), align_command + turns + ['stop']

    def set_block(self, block):
        block_x = int(block[0]//self.scale - 1) if block[0]//self.scale%2==0 else int(block[0]//self.scale)
        block = [block_x, (int(block[1]) // (self.scale*2))*2]
        print("Inside Set Block:",block)
        for i in range(0, 2):
            for j in range(0, 2):
                try:
                    if arena[block[1] + i][block[0]+ j] == 0:
                        arena[block[1]+ i][block[0]+ j] = -3
                        self.new_blocks.append([block[1] + i, block[0] + j])
                except IndexError:
                    continue
        print("Block State:\n", np.array(arena,dtype=np.int32))

    def reset_arena(self):

        for block in self.new_blocks:
            arena[block[0]][block[1]] = 0
        self.new_blocks = []

    def get_induction_distance(self, path):
        dist = 0
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]

            dist += ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
        return dist

    def convert_to_space(self, points, to_induction, induction):
        off = 25
        space_points = []
        
        for point in points:
            x = point[1]
            y = point[0]
            xoff, yoff = 0, 0
            if x == 0 and y == 4:
                xoff = -off
                # yoff = -off
            else:    
                if x % 2 == 0:
                    xoff = - off
                else:
                    xoff = + off

                if x > 1:
                    if y % 2 == 0:
                        yoff = + off
                    else:
                        yoff = - off
                if x == 1:
                    if y == 12:
                        yoff = + off
                    if y == 1:
                        yoff = - off
                    # if y == 4:
                    #     yoff = - off
            x = point[1] * self.scale + self.scale // 2 + xoff
            y = point[0] * self.scale + self.scale // 2 + yoff
            space_points.append([x, y])

        return np.array(space_points, dtype=np.int32)


def set_text(string, coordx, coordy, font_size):  # Function to set text

    font = pygame.font.Font('freesansbold.ttf', font_size)
    text = font.render(string, True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (coordx, coordy)
    return text, text_rect


if __name__ == '__main__':
    P = PathFinder(750, 700)
    P.draw_path()