""" this code was written by Harshit Batra and Rohan Deswal 

as part of hive round 2 """
import pygame

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
    'Mumbai1': (2, 3),
    'Mumbai2': (2, 4),
    'Mumbai3': (3, 3),
    'Mumbai4': (3, 4),
    'Delhi1': (2, 7),
    'Delhi2': (2, 8),
    'Delhi3': (3, 7),
    'Delhi4': (3, 8),
    'Kolkata1': (2, 11),
    'Kolkata2': (2, 12),
    'Kolkata3': (3, 11),
    'Kolkata4': (3, 12),
    'Chennai1': (6, 3),
    'Chennai2': (6, 4),
    'Chennai3': (7, 3),
    'Chennai4': (7, 4),
    'Bengaluru1': (6, 7),
    'Bengaluru2': (6, 8),
    'Bengaluru3': (7, 7),
    'Bengaluru4': (7, 8),
    'Hyderabad1': (6, 11),
    'Hyderabad2': (6, 12),
    'Hyderabad3': (7, 11),
    'Hyderabad4': (7, 12),
    'Pune1': (10, 3),
    'Pune2': (10, 4),
    'Pune3': (11, 3),
    'Pune4': (11, 4),
    'Ahmedabad1': (10, 7),
    'Ahmedabad2': (10, 8),
    'Ahmedabad3': (11, 7),
    'Ahmedabad4': (11, 8),
    'Jaipur1': (10, 11),
    'Jaipur2': (10, 12),
    'Jaipur3': (11, 11),
    'Jaipur4': (11, 12)
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
                        if self.calculate_button_coord[0] <= x <= self.calculate_button_coord[0] + self.scale and \
                                self.calculate_button_coord[1] <= y <= self.calculate_button_coord[1] + self.scale and \
                                self.calculate_path:

                            print('\nNodes:', self.points_to_visit)
                            self.path = astar(arena, self.points_to_visit[0], self.points_to_visit[1])
                            print('Path:', self.path)

                        if self.reset_button_coord[0] <= x <= self.reset_button_coord[0] + self.scale and \
                                self.reset_button_coord[1] <= y <= self.reset_button_coord[1] + self.scale:
                            self.calculate_path = False
                            for point in self.points_to_visit:
                                arena[point[0]][point[1]] = 0
                            self.points_to_visit = []
                            self.path = []

                            print("Nodes after Reset:", self.points_to_visit)
                            print("Path after Reset:", self.path)

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
        min_turns = 10000000000000000000000000000000000000
        min_ind = 0
        
        # If bot is at an induction point
        if bot_coords[0] == start[0] and bot_coords[1] == start[1]:
            for i in range(1,5):
                end = locations_coords[target + str(i)]
                path = astar(start, end, arena)

                path = get_turns_only(path)
                turns = get_turns(path)
                curr_min = len(turns)
                paths.append(path)
                all_turns.append(turns)

                if curr_min < min_turns:
                    min_turns = curr_min
                    min_ind = i
            return convert_to_space(paths[min_ind-1][0:]),all_turns[min_ind-1]

        # Path from bot to induction
        path_1 = get_turns_only(astar(bot_coords, locations_coords[induction], arena))
        turns_1 = get_turns(path)

        # Path from induction to location
        path_2 = get_path(induction,target,indcution)
        turns_2 = get_turns(path_2)

        return convert_to_space(path_1[0:] + path_2[0:]),turns_1 + ['right','right'] + turns_2
    
    def get_turns_only(self,path):
        # print('Full Path:',path)
        out = [path[0]]
        i = 0
        j = 1
        while i < len(path) - 1:
            while j < len(path):
                if path[i][0] != path[j][0] and path[i][1] != path[j][1]:
                    out.append(path[j-1])
                    break
                j+=1
            i = j-1
            j = i+1

        return out+[path[-1]]

    def get_turns(self,turns_only_path):

        turns = []

        for i in range(1,len(turns_only_path)-1):

            a = (turns_only_path[i][0] - turns_only_path[i-1][0], turns_only_path[i][1] - turns_only_path[i-1][1])
            b = (turns_only_path[i+1][0] - turns_only_path[i][0], turns_only_path[i+1][1] - turns_only_path[i][1])

            angle = atan2(a[0]*b[1] - a[1]*b[0], a[0]*b[0] + a[1]*b[1])
            # print(angle)
            if angle > 0:
                turns.append('left')
            else:
                turns.append('right')
        return turns

    def set_blocks(self,blocks):

        for block in blocks:
            arena[block[1]//self.scale][block[0]//self.scale] = -3
            self.new_blocks.append([block[1]//self.scale,block[0]//self.scale])

    def reset_arena(self):

        for block in self.new_blocks:
            arena[block[0]][block[1]] = 0
        self.new_blocks = []

    def convert_to_space(self,points):
        space_points = []
        for point in points:
            space_points.append([point[1]*self.scale + self.scale//2,point[0]*self.scale + self.scale//2])
        return space_points

class Node:
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position[0] == other.position[0] and self.position[1] == other.position[1]


def astar(_grid, start, end):
    """Returns path """

    # given grid
    grid = _grid

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = 0
    start_node.h = 0
    start_node.f = 0
    end_node = Node(None, end)
    end_node.g = 0
    end_node.h = 0
    end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Adding start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Trivial case
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1].copy()  # Return reversed path

        # finding children
        children = []
        for new_position in [[0, -1], [0, 1], [1, 0], [-1, 0]]:  # Adjacent squares

            # Get node position
            node_position = [current_node.position[0] + new_position[0], current_node.position[1] + new_position[1]]

            # Make sure within range
            if node_position[0] > (len(grid) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(grid[len(grid) - 1]) - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if grid[node_position[0]][node_position[1]] != 0 and grid[node_position[0]][node_position[1]] != -2:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                    (child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


def set_text(string, coordx, coordy, font_size):  # Function to set text

    font = pygame.font.Font('freesansbold.ttf', font_size)
    # (0, 0, 0) is black, to make black text
    text = font.render(string, True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (coordx, coordy)
    return text, text_rect


if __name__ == '__main__':
    P = PathFinder(750, 700)
    P.get_path()
