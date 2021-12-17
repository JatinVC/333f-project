"""
astar.py version 1.0.0
the algorithm for A* Search
"""

import sys

# to import stuff from main.py
sys.path.append('./')
import time
from collections import deque
from queue import PriorityQueue

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def mh(c1, c2):
    start_x, start_y = c1
    end_x, end_y = c2
    return abs(start_x - end_x) + abs(start_y - end_y)


def astar(draw, grid, start_node, end_node, construct_path, warning_message_box):
    count = 0
    row_movement = [-1, 1, 0, 0]
    col_movement = [0, 0, -1, 1]

    open_set = PriorityQueue()

    closed_list = {}  # reached nodes minus the frontier

    g_score = {col: sys.maxsize for row in grid for col in row}
    f_score = {col: sys.maxsize for row in grid for col in row}
    g_score[start_node] = 0
    f_score[start_node] = mh((start_node.row, start_node.column), (end_node.row, end_node.column))

    open_set.put((0, count, start_node))
    open_set_hash = {start_node}

    def is_valid(row, col):
        return (row >= 0) and (row <= 49) and (col >= 0) and (col <= 49)

    while not open_set.empty():
        q = open_set.get()[2]
        open_set_hash.remove(q)

        if q == end_node:
            end_node.set_goal()
            construct_path(q, closed_list, start_node)
            return True

        for i in range(4):

            row = q.row + row_movement[i]
            col = q.column + col_movement[i]

            if is_valid(row, col) and grid[row][col].color != BLACK:
                node = grid[row][col]
                temp_g_score = g_score[q] + 1
                if temp_g_score < g_score[node]:
                    g_score[node] = temp_g_score
                    closed_list[node] = q
                    f_score[node] = temp_g_score + mh((node.row, node.column), (end_node.row, end_node.column))

                    if node not in open_set_hash:
                        count += 1
                        open_set.put((f_score[node], count, node))
                        open_set_hash.add(node)
                        node.edge_color()

                    time.sleep(0.005)
                    draw()

            if q != start_node:
                q.visited_node()

    warning_message_box()
    return False
