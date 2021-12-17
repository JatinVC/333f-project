"""
bfs.py version 1.0.0
the algorithm for breadth first Search
"""
import sys
import time
from collections import deque

sys.path.append('./')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def bfs(draw, grid, start_node, end_node, warning_message_box, construct_path):
    print(end_node.row, end_node.column)
    col = len(grid[1])
    rows = len(grid)
    visited = [[False for _ in range(col)] for _ in range(rows)]
    visited[start_node.row][start_node.column] = True

    queue = deque()
    queue.append(start_node)

    def is_valid(row, col):
        return (row >= 0) and (row <= 49) and (col >= 0) and (col <= 49)

    closed_list = {}  # reached nodes minus the frontier

    row_movement = [-1, 1, 0, 0]
    col_movement = [0, 0, -1, 1]

    while queue:

        current = queue.popleft()

        if current != start_node:
            current.visited_node()

        if current == end_node:
            current.set_goal()
            construct_path(current, closed_list, start_node)
            return True

        for i in range(4):
            row = current.row + row_movement[i]
            col = current.column + col_movement[i]

            if is_valid(row, col) and grid[row][col].color != BLACK and not visited[row][col]:
                node = grid[row][col]
                queue.append(node)
                visited[row][col] = True
                node.edge_color()
                closed_list[node] = current
            time.sleep(0.00005)
            draw()
    warning_message_box()
    return False
