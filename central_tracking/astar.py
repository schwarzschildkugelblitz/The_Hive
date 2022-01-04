""" this code was written by Harshit Batra and Rohan Deswal 

as part of hive round 2 """
import numpy as np
import pygame

locations = {
    'mumbai': 1,
    'delhi': 2,
    'kolkata': 3,
    'chennai': 4,
    'bengaluru': 5,
    'hyderabad': 6,
    'pune': 7,
    'ahmedabad': 8,
    'jaipur': 9
}

colors = {
    -1: (0, 0, 0),
    0: (255, 255, 255),
    1: (171, 169, 166),
    2: (25, 98, 224),
    3: (252, 223, 76),
    4: (252, 158, 76),
    5: (243, 116, 247),
    6: (242, 19, 49),
    7: (51, 135, 68),
    8: (145, 81, 35),
    9: (119, 67, 191)
}
arena = np.array([[-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
                  [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])


class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def set_text(string, coordx, coordy, font_size):  # Function to set text

    font = pygame.font.Font('freesansbold.ttf', font_size)
    # (0, 0, 0) is black, to make black text
    text = font.render(string, True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (coordx, coordy)
    return text, text_rect


def astar(start, end, _grid):
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
            return path[::-1]  # Return reversed path

        # finding children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:  # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(grid) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(grid[len(grid) - 1]) - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if grid[node_position[0]][node_position[1]] != 0:
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


# def bot_path(induction_centre , destination ):

#     path = astar(grid , start, end)
#     return path

def draw_path():
    pygame.init()

    rows = 14
    cols = 15
    scale = 50

    game_display = pygame.display.set_mode((750, 750))
    pygame.display.set_caption('A* Path Show')

    clock = pygame.time.Clock()

    crashed = False
    calculate_path = False
    # TODO
    points_to_visit = []
    calculate_button_coord = (3 * scale, rows * scale)
    reset_button_coord = (11 * scale, rows * scale)

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
                    pass
                if event.button == 1:  # Find Path Button or Reset
                    x, y = pygame.mouse.get_pos()
                    if calculate_button_coord[0] <= x <= calculate_button_coord[0] + scale and \
                            calculate_button_coord[1] <= y <= calculate_button_coord[1] + scale:
                        calculate_path = True

            # Release Events
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:  # Set Nodes to Visit In Order
                    pass
                if event.button == 1 and calculate_path:  # Find Path Button or Reset
                    x, y = pygame.mouse.get_pos()
                    if calculate_button_coord[0] <= x <= calculate_button_coord[0] + scale and \
                            calculate_button_coord[1] <= y <= calculate_button_coord[1] + scale:
                        # Perform Calculation Here
                        print("Yeah")
                        pass

        game_display.fill((255, 255, 255))
        for i in range(rows):
            for j in range(cols):
                color = colors[arena[i][j]]
                pygame.draw.rect(game_display, color, pygame.Rect(j * scale, i * scale, scale, scale))

                pygame.draw.rect(game_display, (0, 0, 0), pygame.Rect(j * scale, i * scale, scale, scale), 2)

        # Calculate Path Button
        x, y = pygame.mouse.get_pos()
        if calculate_button_coord[0] <= x <= calculate_button_coord[0] + scale and \
                calculate_button_coord[1] <= y <= calculate_button_coord[1] + scale:
            color = (0, 255, 0)
        else:
            color = (224, 189, 139)
        textobj = set_text('O', calculate_button_coord[0] + scale // 2, calculate_button_coord[1] + scale // 2, 50)
        pygame.draw.rect(game_display, color,
                         pygame.Rect(calculate_button_coord[0], calculate_button_coord[1], scale, scale))
        pygame.draw.rect(game_display, (0, 0, 0),
                         pygame.Rect(calculate_button_coord[0], calculate_button_coord[1], scale, scale), 2)
        game_display.blit(textobj[0], textobj[1])

        # Reset Path Button
        x, y = pygame.mouse.get_pos()
        if reset_button_coord[0] <= x <= reset_button_coord[0] + scale and \
                reset_button_coord[1] <= y <= reset_button_coord[1] + scale:
            color = (255, 0, 0)
        else:
            color = (224, 189, 139)
        textobj = set_text('X', reset_button_coord[0] + scale // 2, reset_button_coord[1] + scale // 2, 50)
        pygame.draw.rect(game_display, color, pygame.Rect(reset_button_coord[0], reset_button_coord[1], scale, scale))
        pygame.draw.rect(game_display, (0, 0, 0),
                         pygame.Rect(reset_button_coord[0], reset_button_coord[1], scale, scale), 2)
        game_display.blit(textobj[0], textobj[1])
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    quit()


if __name__ == '__main__':
    draw_path()
