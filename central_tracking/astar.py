class Large_number_of_iterations(Exception):
    def __init__(self, count, error_message="too time consuming case"):
        self.count = count
        self.error_message = error_message
        super().__init__(self.error_message)


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


def astar(_grid, start, end, extra):
    """Returns path """

    # given grid
    grid = _grid
    # counts the number of iterations 
    count = 0
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
        for new_position in [[1, 0], [0, -1], [0, 1], [-1, 0]]:  # Adjacent squares

            # Get node position
            node_position = [current_node.position[0] + new_position[0], current_node.position[1] + new_position[1]]

            # Make sure within range
            if node_position[0] > (len(grid) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(grid[len(grid) - 1]) - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            loc_0 = int(node_position[0])
            loc_1 = int(node_position[1])
            if grid[loc_0][loc_1] != 0 and grid[loc_0][loc_1] != -2 and grid[loc_0][loc_1] != extra:
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
            first = current_node.parent
            curr = current_node
            last = child

            cost = 0
            no_turn_cost = 0 

            if first is not None:
                # check to minimize turning by changing heuritic measurement
                if ((first.position[0] == curr.position[0] and first.position[1] != curr.position[1]) and (
                        curr.position[1] == last.position[1] and curr.position[0] != last.position[0])):
                    # check for right turn
                    child.g = current_node.g + cost
                    child.h = ((pow(abs(child.position[0] - end_node.position[0]), 2)) + (
                        pow(abs(child.position[1] - end_node.position[1]), 2)))
                    child.f += child.g + child.h

                elif ((first.position[0] != curr.position[0] and first.position[1] == curr.position[1]) and (
                        curr.position[0] == last.position[0] and curr.position[1] != last.position[0])):
                    # check for right turn
                    child.g = current_node.g + cost
                    child.h = (pow(abs(child.position[0] - end_node.position[0]), 2)) + (
                        pow(abs(child.position[1] - end_node.position[1]), 2))
                    child.f += child.g + child.h
                else:
                    # no turn condition
                    child.g = current_node.g + no_turn_cost
                    child.h = (pow(abs(child.position[0] - end_node.position[0]), 2)) + (
                        pow(abs(child.position[1] - end_node.position[1]), 2))
                    child.f += child.g + child.h
            else:
                # first node case
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                        (child.position[1] - end_node.position[1]) ** 2)
                child.f += child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)

            count += 1
            # print(count)
            if count > 3000:
                raise Large_number_of_iterations(count)
