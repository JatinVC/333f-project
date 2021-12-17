import sys
import time

sys.path.append('./')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def ucs(draw, grid, start_node, end_node, warning_message_box, construct_path):
    row_movement = [-1, 1, 0, 0]
    col_movement = [0, 0, -1, 1]

    col_1 = len(grid[1])
    rows_1 = len(grid)

    def is_valid(row, col):
        return (row >= 0) and (row <= 49) and (col >= 0) and (col <= 49)

    distance = {col: sys.maxsize for row in grid for col in row}
    distance[start_node] = 0
    visited = []
    closed_list = {}

    def get_min_distance(distance, visited):
        try:
            min = sys.maxsize
            for u in distance:
                if distance[u] < min and u not in visited and u.color != BLACK:
                    min = distance[u]
                    min_index = u
            return min_index
        except:
            min_index = False
            return min_index

    total_nodes = col_1 * rows_1
    state = len(visited) != total_nodes
    while state:

        current = get_min_distance(distance, visited)
        if not current:
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
                temp_dist = distance[current] + grid[row][col].weight

                if temp_dist < distance[grid[row][col]]:
                    distance[grid[row][col]] = temp_dist

                    closed_list[grid[row][col]] = current
                    grid[row][col].edge_color()

                time.sleep(0.0005)
                draw()
        if current != start_node:
            current.visited_node()

    return False
