"""
dfs.py version 1.0.0
the algorithm for Depth First Search
"""

import sys
import time

sys.path.append('./')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

"""
It is a buggy DFS, the "not visited[row][col]" in
    if is_valid(row, col) and grid[row][col].color != BLACK and not visited[row][col]:
make it travel every other line. Hence it could miss the goal.

Attempts made:
    1. add break in the movement for loop
        - it only works like normal DFS under a limited case.
        - it always have stack length of 1.
        - it will trap in a dead end.
    2. add a short-cut in the for loop
        - it will stop if the neighbor is the goal, hence it will not skip the goal.

Make it a normal DFS needs:
    1. a way to add enough neighbours to keep it running, so it can backtrack 
        - need another list?
        - or start with a stack, which alrealy has some things in it and add the start point?
"""


def dfs(draw, grid, start_node, end_node, warning_message_box, construct_path):
    # print(f"The start point is at [x,y] {start.row}, {start.col}.")
    # print(f"The end point is at [x,y] {end.row}, {end.col}.")

    col = len(grid[1])
    rows = len(grid)
    visited = [[False for _ in range(col)] for _ in range(rows)]
    # visited[start.row][start.col] = True
    # visited = [[False for i in range(len(grid[0]))] for j in range(len(grid))]

    visited[start_node.row][start_node.column] = True
    stack = [start_node]  # put the starting point into the stack

    # print(len(stack), stack)

    def is_valid(row, col):
        return (row >= 0) and (row <= 49) and (col >= 0) and (col <= 49)

    closed_list = {}  # reached nodes minus the frontier
    # movement
    # row_movement = [-1, 1, 0, 0]
    # col_movement = [0, 0, -1, 1]

    # below can travel all grids with order: 1. up, 2. left, 3. down, 4. right
    row_movement = [0, 1, 0, -1]
    col_movement = [1, 0, -1, 0]
    # reverse order to get the same directions as above: 1. up, 2. left, 3. down, 4. right
    # since using break, and stack is LIFO:
    # row_movement = [-1, 0, 1, 0]
    # col_movement = [0, -1, 0, 1]

    while len(stack) > 0:
        print(f"stack length: {len(stack)}")
        current = stack.pop()  # stack.pop(0) work as BFS
        if current != start_node:
            current.visited_node()
        if current == end_node:
            current.set_goal()
            construct_path(current, closed_list, start_node)
            return True
        # else:
        for i in range(4):
            row = current.row + row_movement[i]
            col = current.column + col_movement[i]
            if is_valid(row, col) and grid[row][col].color != BLACK and not visited[row][col]:
                # if (isValid(row, col) and visited[row][col] != True):
                neighbour = grid[row][col]
                closed_list[neighbour] = current
                stack.append(neighbour)
                neighbour.edge_color()
                visited[row][col] = True

                # short-cut: the buggy DFS travel every second line,
                # this trick make sure the frontier will not skip the ending point.
                if neighbour == end_node:
                    neighbour.set_goal()
                    construct_path(neighbour, closed_list, start_node)
                    return True

                time.sleep(0.00003)
                draw()
                # break  # this will make stack length always 1, hence cannot backtrack to continue DFS
        # else:
        #     stack.append(curr)

    warning_message_box()  # display error message: cannot find path! same as return False.
    return False
