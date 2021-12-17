"""
dfs.py version 1.1.0
the algorithm for Uniform Cost Search
"""
import sys
import time

sys.path.append('./')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def ucs(draw, grid, start_node, end_node, warning_message_box, construct_path):
    print(f"The start point is at [x,y] {start.row}, {start.col}.")
    print(f"The end point is at [x,y] {end.row}, {end.col}.")

    col = len(grid[0])
    rows = len(grid)

    def is_valid(row, col):
        return (row >= 0) and (row <= 49) and (col >= 0) and (col <= 49)

    # set the distance to infinity due to unknown
    distance = {col: sys.maxsize for row in grid for col in row}
    distance[start_node] = 0
    visited = []
    closed_list = {}

    # below are two lists determine the movement direction
    row_movement = [-1, 1, 0, 0]
    col_movement = [0, 0, -1, 1]

    def get_min_distance(distance, visited):
        try:
            min = sys.maxsize
            for i in distance:
                if distance[i] < min and i not in visited and i.color != BLACK:
                    min = distance[i]
                    min_index = i
            return min_index
        except:
            min_index = False
            return min_index

    total_nodes = col * rows
    state = len(visited) != total_nodes

    while state:
        current = get_min_distance(distance, visited)
        if not current:
            # cannot reach the goal
            warning_message_box()
            return False

        visited.append(current)

        if current == end_node:
            end_node.set_goal()
            construct_path(current, closed_list, start_node)
            break

        for i in range(4):
            row = current.row + row_movement[i]
            col = current.column + col_movement[i]

            if is_valid(row, col) and grid[row][col].color != BLACK and grid[row][col] not in visited:
                neighbour = grid[row][col]
                temp_dist = distance[current] + neighbour.weight

                if temp_dist < distance[neighbour]:
                    distance[neighbour] = temp_dist
                    closed_list[neighbour] = current
                    neighbour.edge_color()

                time.sleep(0.0005)
                draw()
        if current != start_node:
            current.visited_node()

    # cannot reach the goal
    return False
