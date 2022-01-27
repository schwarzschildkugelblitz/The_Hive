""" this code was written by Rohan Deswal

as part of hive round 2 """
import numpy as np
import pygame
from math import atan2, degrees
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

    'Mumbai': (2, 3),
    'Delhi': (2, 7),
    'Kolkata': (2, 11),
    'Chennai': (6, 3),
    'Bengaluru': (6, 7),
    'Hyderabad': (6, 11),
    'Pune': (10, 3),
    'Ahmedabad': (10, 7),
    'Jaipur': (10, 11)
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


def get_locations_coords(location_tag, suffix_val):
    if location_tag == '1' or location_tag == '2':
        return locations_coords[location_tag]

    row, col = locations_coords[location_tag]
    
    offsets = [-1,-1,0,1,2,2,1,0]

    return row + offsets[suffix_val-1], col + offsets[-suffix_val]


def get_bot_angle(bot_top_left, bot_bottom_left):
    return atan2(bot_top_left[1] - bot_bottom_left[1], bot_top_left[0] - bot_bottom_left[0])


def get_align_command(bot_vector, path_vectors):
    angle_threshold = 45

    direction = [path_vectors[1][0] - path_vectors[0][0], path_vectors[1][1] - path_vectors[0][1]]

    angle = atan2(bot_vector[0] * direction[1] - bot_vector[1] * direction[0],
                  bot_vector[0] * direction[0] + bot_vector[1] * direction[1])

    angle = degrees(angle)

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

    def reset(self):
        for point in self.points_to_visit:
            arena[point[0]][point[1]] = 0
        for point in self.new_blocks:
            arena[point[0]][point[1]] = 0
        self.__init__(self.width,self.height)


    def draw_path(self):
        pygame.init()

        game_display = pygame.display.set_mode((self.width, self.height + self.scale))
        pygame.display.set_caption('PathFinder Visualisation')

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
                            self.reset()

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

            text_obj = set_text('O', self.calculate_button_coord[0] + self.scale // 2,
                                self.calculate_button_coord[1] + self.scale // 2, 50)
            pygame.draw.rect(game_display, color,
                             pygame.Rect(self.calculate_button_coord[0],
                                         self.calculate_button_coord[1], self.scale, self.scale))
            pygame.draw.rect(game_display, (0, 0, 0),
                             pygame.Rect(self.calculate_button_coord[0],
                                         self.calculate_button_coord[1], self.scale, self.scale), 2)
            game_display.blit(text_obj[0], text_obj[1])

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


            text_obj = set_text('X', self.reset_button_coord[0] + self.scale // 2,
                                self.reset_button_coord[1] + self.scale // 2, 50)
            pygame.draw.rect(game_display, color,
                             pygame.Rect(self.reset_button_coord[0], self.reset_button_coord[1],
                                         self.scale, self.scale))
            pygame.draw.rect(game_display, (0, 0, 0),
                             pygame.Rect(self.reset_button_coord[0], self.reset_button_coord[1],
                                         self.scale, self.scale), 2)

            game_display.blit(text_obj[0], text_obj[1])
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
                cur_path = gen_path(arena,start,get_locations_coords(target,i),self.rows,self.cols)
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

            ou_turns = align_command + turns + drop_command

            return self.convert_to_space(path,False,None),ou_turns

        path = gen_path(arena,start,end,self.rows,self.cols)
        if path is None:
            # print("Induction None")
            return None, None
        turns = get_turns(path)
        align_command = get_align_command(bot_vector, path[:2])

        ou_turns = align_command + turns

        if ou_turns[0] == '180' and ou_turns[1] == 'right':
            ou_turns = ['left']
            path = [path[0]] + [path[-1]]

        return self.convert_to_space(path,True,target),ou_turns + ['stop']

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
            x_off, y_off = 0, 0
            if x == 0 and y == 4:
                x_off = -off
                # y_off = -off
            else:    
                if x % 2 == 0:
                    x_off = - off
                else:
                    x_off = + off

                if x > 1:
                    if y % 2 == 0:
                        y_off = + off
                    else:
                        y_off = - off
                if x == 1:
                    if y == 12:
                        y_off = + off
                    if y == 1:
                        y_off = - off

            x = point[1] * self.scale + self.scale // 2 + x_off
            y = point[0] * self.scale + self.scale // 2 + y_off
            space_points.append([x, y])

        return np.array(space_points, dtype=np.int32)


def set_text(string, coord_x, coord_y, font_size):  # Function to set text

    font = pygame.font.Font('freesansbold.ttf', font_size)
    text = font.render(string, True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (coord_x, coord_y)
    return text, text_rect


if __name__ == '__main__':
    P = PathFinder(750, 700)
    P.draw_path()