""" this code was hritten by Harshit Batra 

as part of hive round 2 """
import numpy as np 

class Node() :
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar( start, end):
    """Returns path """
    
    # given grid 
    grid  = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0],
                      [1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0 ,0],
                      [1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0 ,0],
                      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0],
                      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0],
                      [1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0 ,0],
                      [1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0 ,0],
                      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0],
                      [1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0 ,0],
                      [1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0 ,0],
                      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0],
                      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0]])

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
            return path[::-1] # Return reversed path

        # finding childerns 
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(grid) - 1) or node_position[0] < 0 or node_position[1] > (len(grid[len(grid)-1]) -1) or node_position[1] < 0:
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
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


def bot_path(induction_centre , destination ):

    path = astar(grid , start, end)
    return path