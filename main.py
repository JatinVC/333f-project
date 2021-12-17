"""
main.py version 1.1.0
this file will be for combining all the algorithms into one project
"""

import math
import random
import sys
from tkinter import *
from tkinter import messagebox

import pygame

sys.path.append('./algorithms')
from astar import *
from bfs import *
from dfs import *
from ucs import *

ROW = 50
COLUMN = 50

# node colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# start and end nodes
RED = (223, 50, 100)
PURPLE = (107, 16, 143)
# other nodes
DARK_BLUE = (52, 55, 255)
LIGHT_BLUE = (50, 173, 223)
LIGHT_ORANGE = (255, 155, 119)

pygame.init()
surface = pygame.display.set_mode((650, 650))
pygame.display.set_caption('Find The Way')


class Point:
    def __init__(self, x, y, column, row, width, weight):
        self.x = x
        self.y = y
        self.column = column
        self.row = row
        self.width = width
        self.color = WHITE
        self.weight = weight
        self.box_obj = pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.width))
        self.font = pygame.font.SysFont('Arial', 14)

    def draw(self):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.width))

    def draw_weight(self):
        text_weight = self.font.render(str(self.weight), True, WHITE)
        text_box_obj = text_weight.get_rect(center=self.box_obj.center)
        surface.blit(text_weight, text_box_obj)

    def set_source(self):
        self.color = RED

    def set_goal(self):
        self.color = PURPLE

    def set_obstacle(self):
        self.color = BLACK

    def visited_node(self):
        self.color = DARK_BLUE

    def backtrack(self):
        self.color = LIGHT_ORANGE

    def edge_color(self):
        self.color = LIGHT_BLUE

    def reset(self):
        self.color = WHITE


# build the grid of window size, the looping is
# for creating all rows and columns of small squares inside the grid
def make_grid(width):
    grid = []
    y0 = 0
    n = width
    for j in range(1, ROW + 1):
        gap = width
        x0 = 0
        grid.append([])
        for i in range(1, ROW + 1):
            point = Point(x0, y0, math.trunc(x0 / 13), math.trunc(y0 / 13), width, random.randint(1, 5))
            x0 = gap + i
            gap = gap + width
            grid[j - 1].append(point)
        y0 = n + j
        n = n + width
    return grid


def draw(grid_lines, grid):
    grid_lines.fill(BLACK)
    for row in grid:
        for spot in row:
            spot.draw()
            spot.draw_weight()

    pygame.display.flip()


"""
The window size is of total width 650.
It has 50 rows and 50 columns (a grid of N*N, N is 50 here).
13 is given by total width divided by N
650 / 50 = 13
N and window can be adjusted 
to change the number of rows and columns.
"""


# use with mouse to get the clicked position
def get_position(x, y):
    column = math.trunc(x / 13)
    row = math.trunc(y / 13)
    return column, row


def construct_path(current_node, from_list, start):
    current = current_node
    for i in range(len(from_list) - 1):
        step = from_list[current]
        if step == start:
            break
        else:
            step.backtrack()
            current = step


window = Tk()
window.title('Rules and Information')
text = Text(window, height=30, width=52)
label = Label(window, text="Find The Way: Rules and Information")
label.config(font=("Arial", 15))

rules_info_text = """
---------------------------------------------------
 ? Node colors:\n
* Red is the source
* Purple is the goal
* Black is a obstacle
* Dark blue is a explored node
* Light blue is a visited node
* Light orange is the path node(s) 
---------------------------------------------------
 ? How to mark nodes:\n
* Right click on the node to mark it.
* Left click on the node to unmark it.
* The order of marking nodes:
  1: Start node (the source)
  2: End node (the goal)
  3: Obstacle node(s)
---------------------------------------------------
 ? How to find the path:\n
  A* (Astar): press key 'a'
  BFS       : press key 'b'
  DFS       : press key 'd'
  UCS       : press key 'u'
  *********************************
* New game  : press key 'c'
* Replay    : press key 'space bar'
---------------------------------------------------
"""

text.insert(END, rules_info_text)

continue_button = Button(window, text="Continue", width=10, command=window.destroy)

label.grid(columnspan=4, row=0)
text.grid(columnspan=4, rowspan=7)
continue_button.grid(column=3, row=1)

window.update()
mainloop()


def warning_message_box():
    Tk().wm_withdraw()
    messagebox.showinfo("Error: path not found",
                        "Failed to find a path from the source to the goal.\nPerhaps it is blocked by obstacles... ")


# replay the game again with the same source, goal, random weights, and obstacles.
def replay(draw, grid, start_node, end_node):
    if start_node is not None:
        start_node.set_source()
    if end_node is not None:
        end_node.set_goal()
    for row in grid:
        for column in row:
            if column.color == DARK_BLUE or column.color == LIGHT_BLUE or column.color == LIGHT_ORANGE:
                column.color = WHITE
    draw()


def main():
    game = True
    start_node, end_node = None, None
    grid = make_grid(12)

    while game:
        draw(surface, grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False

            # left click to mark nodes with different colors
            if pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()
                column, row = get_position(x, y)
                selected_node = grid[row][column]
                if not start_node and selected_node != end_node:
                    start_node = selected_node
                    start_node.set_source()

                if not end_node and selected_node != start_node:
                    end_node = selected_node
                    end_node.set_goal()

                elif selected_node != start_node and selected_node != end_node:
                    selected_node.set_obstacle()

            # right click to unmark nodes with different colors
            elif pygame.mouse.get_pressed()[2]:
                x, y = pygame.mouse.get_pos()
                column, row = get_position(x, y)
                selected_node = grid[row][column]
                selected_node.reset()
                if selected_node == start_node:
                    start_node = None
                elif selected_node == end_node:
                    end_node = None

            # supported keys to perform different searching algorithms
            # and start a new game, or replay a game
            if event.type == pygame.KEYDOWN:
                # press key 'c' to start a new game
                if event.key == pygame.K_c:
                    start_node, end_node = None, None
                    grid = make_grid(12)
                if event.key == pygame.K_SPACE:
                    replay(lambda: draw(surface, grid), grid, start_node, end_node)

                if event.key == pygame.K_a and start_node and end_node:
                    astar(lambda: draw(surface, grid), grid, start_node, end_node, construct_path, warning_message_box)
                if event.key == pygame.K_b and start_node and end_node:
                    bfs(lambda: draw(surface, grid), grid, start_node, end_node, warning_message_box, construct_path)
                if event.key == pygame.K_d and start_node and end_node:
                    dfs(lambda: draw(surface, grid), grid, start_node, end_node, warning_message_box, construct_path)
                if event.key == pygame.K_u and start_node and end_node:
                    ucs(lambda: draw(surface, grid), grid, start_node, end_node, warning_message_box, construct_path)
    pygame.quit()


if __name__ == "__main__":
    main()
