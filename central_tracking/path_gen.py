class LineSegment:
    def __init__(self,point_a,point_b):

        self.end_a = None
        self.end_b = None
        self.col = None
        self.row = None
        self.is_horizontal,self.is_vertical = False,False

        if point_a[0] == point_b[0]:
            self.is_horizontal = True
            self.end_a = point_a[1]
            self.end_b = point_b[1]

            self.row = point_a[0]

        if point_a[1] == point_b[1]:
            self.is_vertical = True
            self.end_a = point_a[0]
            self.end_b = point_b[0]

            self.col = point_a[1]

    def get_intersection(self,line_segment):
        if line_segment.is_horizontal == self.is_horizontal:
            if self.row == line_segment.row:
                return False, None
        elif line_segment.is_vertical == self.is_vertical:
            if self.col == line_segment.col:
                return False, None
        elif line_segment.is_horizontal and self.is_vertical:
            if line_segment.end_a <= self.col <= line_segment.end_b and self.end_a <= line_segment.row <= self.end_b:
                return True, [line_segment.row,self.col]
        elif line_segment.is_vertical and self.is_horizontal:
            if line_segment.end_a <= self.row <= line_segment.end_b and self.end_a <= line_segment.col <= self.end_b:
                return True, [self.row,line_segment.col]
        return False, None


def get_vertical_line(point,rows,_grid):
    r_a = point[0]
    r_b = point[0]

    found_a = False
    found_b = False
    while not found_a:
        if r_a-1 >= 0:
            if _grid[r_a-1][point[1]] != 0:
                found_a = True
                break
        elif r_a == 0:
            break
        r_a -= 1

    while not found_b:
        if r_b+1 <= rows-1:
            if _grid[r_b+1][point[1]] != 0:
                found_b = True
                break
        elif r_b == rows - 1:
            break
        r_b += 1

    return LineSegment([r_a,point[1]],[r_b,point[1]])

def get_horizontal_line(point,cols,_grid):
    c_a = point[1]
    c_b = point[1]

    found_a = False
    found_b = False
    while not found_a:
        if c_a-1 >= 0:
            if _grid[point[0]][c_a-1] != 0:
                found_a = True
                break
        elif c_a == 0:
            break
        c_a -= 1

    while not found_b:
        if c_b+1 <= cols-1:
            if _grid[point[0]][c_b+1] !=0:
                found_b = True
                break
        elif c_b == cols-1:
            break
        c_b += 1

    return LineSegment([point[0],c_a],[point[0],c_b])

def gen_path(_grid,start,end,rows,cols):

    start_vertical = get_vertical_line(start,rows,_grid)
    end_vertical = get_vertical_line(end,rows,_grid)

    start_horizontal = get_horizontal_line(start,cols,_grid)
    end_horizontal = get_horizontal_line(end,cols,_grid)



    # One Turn Path
    # Case 1 Vertical for Start and Horizontal for End
    exists, common_point = start_vertical.get_intersection(end_horizontal)

    if exists:
        if (start[0] == common_point[0] and start[1] == common_point[1]) or \
                (end[0] == common_point[0] and end[1] == common_point[1]):
            return [start, end]
        return [start, common_point, end]

    # Case 2 Horizontal for Start and Vertical for End
    exists, common_point = start_horizontal.get_intersection(end_vertical)

    if exists:
        if (start[0] == common_point[0] and start[1] == common_point[1]) or \
                (end[0] == common_point[0] and end[1] == common_point[1]):
            return [start, end]
        return [start, common_point, end]


    #Two Turn Path
    # Case 3 Vertical for Start and Vertical for End
    rows_to_use = [] # this will have the vector => [row,deviation]
    line_exists = False
    for i in range(start_vertical.end_a,start_vertical.end_b+1):
        for j in range(end_vertical.end_a,end_vertical.end_b+1):
            if i==j:
                line_exists = True
                a = min(start_vertical.col,end_vertical.col)
                b = max(start_vertical.col,end_vertical.col)
                for col in range(a,b+1):
                    if _grid[i][col] != 0:
                        line_exists = False
                        break
                if line_exists:
                    rows_to_use.append([i,abs(start[0]-i)])
    if line_exists:
        min_dev = float('inf')
        min_row = None
        for row_and_deviation in rows_to_use:
            if row_and_deviation[1] < min_dev:
                min_row = row_and_deviation[0]
                min_dev = row_and_deviation[1]
        return [start, [min_row,start[1]], [min_row,end[1]], end]

    # Case 4 Horizontal for Start and Horizontal for End
    cols_to_use = [] # this will have the vector => [col,deviation]
    line_exists = False
    for i in range(start_horizontal.end_a,start_horizontal.end_b+1):
        for j in range(end_horizontal.end_a,end_horizontal.end_b+1):
            if i==j:
                line_exists = True
                a = min(start_horizontal.row,end_horizontal.row)
                b = max(start_horizontal.row,end_horizontal.row)
                for row in range(a,b+1):
                    if _grid[row][i] != 0:
                        line_exists = False
                        break
                if line_exists:
                    cols_to_use.append([i,abs(start[1]-i)])
    if line_exists:
        min_dev = float('inf')
        min_col = None

        for col_and_deviation in cols_to_use:
            if col_and_deviation[1] < min_dev:
                min_col = col_and_deviation[0]
                min_dev = col_and_deviation[1]

        return [start, [start[0],min_col], [end[0],min_col], end]

    # raise Exception("Not a 1 or 2 turn Path")
    return None