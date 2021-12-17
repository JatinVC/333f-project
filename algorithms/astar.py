"""
astar.py version 1.1.0
the algorithm for A* Search
"""
import sys
import time
from queue import PriorityQueue

sys.path.append('./')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def find_h_value(v1, v2):
    start_x, start_y = v1
    end_x, end_y = v2
    return abs(start_x - end_x) + abs(start_y - end_y)


def astar(draw, grid, start_node, end_node, construct_path, warning_message_box):
    print(f"The start point is at [x,y] {start_node.row}, {start_node.col}.")
    print(f"The end point is at [x,y] {end_node.row}, {end_node.col}.")

    count = 0
    open_list = PriorityQueue()

    closed_list = {}  # reached nodes minus the frontier

    # set the g_value and f_value to infinity due to unknown
    g_value = {col: sys.maxsize for row in grid for col in row}
    f_value = {col: sys.maxsize for row in grid for col in row}
    g_value[start_node] = 0
    f_value[start_node] = find_h_value((start_node.row, start_node.column), (end_node.row, end_node.column))

    open_list.put((0, count, start_node))
    open_list_hash = {start_node}

    def is_valid(row, col):
        return (row >= 0) and (row <= 49) and (col >= 0) and (col <= 49)

    # below are two lists determine the movement direction
    row_movement = [-1, 1, 0, 0]
    col_movement = [0, 0, -1, 1]

    while not open_list.empty():
        q = open_list.get()[2]
        open_list_hash.remove(q)

        if q == end_node:
            end_node.set_goal()
            construct_path(q, closed_list, start_node)
            return True

        for i in range(4):

            row = q.row + row_movement[i]
            col = q.column + col_movement[i]

            if is_valid(row, col) and grid[row][col].color != BLACK:
                neighbour = grid[row][col]
                # it is not weighted, so only plus 1 unit cost
                temp_g_value = g_value[q] + 1
                if temp_g_value < g_value[neighbour]:
                    # this path from the source to the neighbour is better than all previous one
                    g_value[neighbour] = temp_g_value
                    closed_list[neighbour] = q
                    # f(x) = g(x) + h(x)
                    # estimated cost of the best path from node x to the goal
                    # = path cost from the source to node x + estimated cost of the shortest path from x to the goal
                    f_value[neighbour] = temp_g_value + find_h_value((neighbour.row, neighbour.column),
                                                                     (end_node.row, end_node.column))

                    if neighbour not in open_list_hash:
                        count += 1
                        open_list.put((f_value[neighbour], count, neighbour))
                        open_list_hash.add(neighbour)
                        neighbour.edge_color()

                    time.sleep(0.0005)
                    draw()

            if q != start_node:
                q.visited_node()

    # cannot reach the goal
    warning_message_box()
    return False
