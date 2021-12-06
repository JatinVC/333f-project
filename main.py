'''
main.py version 1.0.0
this file will be for combining all the algorithms into one project
'''

import pygame
import math
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from collections import deque
from queue import PriorityQueue
import time
import sys
sys.path.append('./algorithms')
from djikstra import *
from astar import *
from bfs import *
from dfs import *
from ids import *
from ucs import *


ROW=50
COLUMN=50

pygame.init()
surface=pygame.display.set_mode((650, 650))
pygame.display.set_caption('Pathfinding Visualizer')
done = False

#colors
BLACK = (0, 0, 0)
WHITE=(255,255,255)
#start and end node
red=(222, 49, 99)
purple=(106, 15, 142)
#other nodes
light_blue=(49, 172, 222)
light_orange=(255, 154, 118)
dark_blue=(51, 54, 255 )


y0=0
x1=20
y1=20
spacing=5
x0=0

y=0
n=20

class Spot:
    def __init__(self, x, y, col, row, width):
        self.x=x
        self.y=y
        self.col=col
        self.row=row
        self.width=width
        self.color = WHITE

    def draw(self):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.width))

    def make_start(self):
        self.color=red

    def make_end(self):
        self.color=purple

    def make_barrier(self):
        self.color=BLACK
        
    def visited_cell(self):
        self.color=dark_blue

    def backtrack(self):
        self.color=light_orange

    def edge_color(self):
        self.color=light_blue

    def reset(self):
        self.color=WHITE


def grid_make(width):
    grid=[]
    y0=0
    n=width
    for j in range(1 ,ROW+1):
        gap=width
        x0=0
        grid.append([])
        for i in range(1, ROW+1):
            spot=Spot(x0, y0,math.trunc(x0/13),math.trunc(y0/13), width)
            x0=gap+i
            gap=gap+width
            grid[j-1].append(spot)
        y0=n+j
        n=n+width
    return grid

def draw(win, grid):
    win.fill(BLACK)
    for row in grid:
        for spot in row:
            spot.draw()
            
    pygame.display.flip()

'''this will get us the row and column position because
total width is 650. and number of row and column is 50.
650/50=13 .so you can always adjust the number of column and rows by changing
some values like down here. Always keep in mind, if you want
to change the width and height by some number, then multiply it with 13 and 
give the final value as the window size, because 13 is the default size after 
adding the spacing etc of the cell here.'''

def get_position(x, y):
    col=math.trunc(x/13)
    row=math.trunc(y/13)
    return col, row

def construct_path(curr_node, from_list, start):
    r=curr_node
    for i in range(len(from_list)-1):
        t=from_list[r]
        if t==start:
            break
        else:
            t.backtrack()
            r=t
            
window=Tk()
window.title('tutorial window')
t=Text(window, height=30, width=52)
label=Label(window, text="PathFinding Visualizer Tutorial")
label.config(font=("Courier", 14))

text="""-----------------------------------------
 ? node Info:\n
* Red is the Start node
* Purple is the End node
* Black is the Barrier node
* Dark blue is the already visited node
* Light blue is the currently visiting node
* light Orange is the Path node 
-------------------------------------------
 ? how to mark node:\n
* Right click on the cell to mark the node.
* Left click on the cell to unmark the node.
* The order of nodes are:
  1: Start node
  2: End node
  3: Barrier node
-------------------------------------------
 ? How to visualize algorithms:\n
* Algorithms which are currently implemented:
  1: BFS
  2: Dijakstra
  3: A star
  4: DFS
  5: IDS
  6: UCS
  
  To run-
  BFS       : press 'b'
  Dijkstra  : press 'd'
  A* Search : press 'a'
  DFS       : press 'd'
  IDS       : press 'i'
  UCS       : press 'u'
---------------------------------------------
 ? Additional info:\n
* To clear out the board :Press 'c'
* To clear out only the visualization:
  Press the space bar
---------------------------------------------
"""

t.insert(END, text)

skip_button=Button(window, text="Skip",width=10, command=window.destroy)

label.grid(columnspan=4, row=0)
t.grid(columnspan=4, rowspan=7)
skip_button.grid(column=3, row=1)

window.update()
mainloop()

def message_box():
    Tk().wm_withdraw()
    messagebox.showinfo("error", ('oops!! couldn\'t find a path.\n Maybe it is blocked by barriers. '))

def leave(draw, grid, start, end):
    if start!=None:
        start.make_start()
    if end!=None:
        end.make_end()
    for row in grid:
        for col in row:
            if col.color ==dark_blue or col.color==light_blue or col.color==light_orange:
                col.color=WHITE
    draw()
             
def main():
    run = True

    start=None
    end=None
    
    grid=grid_make(12)

    while run:
        draw(surface, grid)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
                

            if pygame.mouse.get_pressed()[0]:
                x, y=pygame.mouse.get_pos()
                col, row=get_position(x,y)
                node=grid[row][col]
                if not start and node!=end:
                    start=node
                    start.make_start()
                    
                if not end and node!=start:
                    end=node
                    end.make_end()

                elif node!=start and node!=end:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                x,y=pygame.mouse.get_pos()
                col, row=get_position(x, y)
                node=grid[row][col]
                node.reset()
                if node==start:
                    start=None
                elif node==end:
                    end=None
                    
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_b and start and end:
                    pass
                    # bfs(lambda: draw(surface, grid), grid, start, end)

                if event.key==pygame.K_c:
                    start=None
                    end=None
                    grid=grid_make(12)

                if event.key==pygame.K_SPACE:
                     leave(lambda: draw(surface, grid),grid, start, end)
                    
                if event.key==pygame.K_d and start and node:
                    dijkstra(lambda: draw(surface, grid),grid, start, end)
                    
                if event.key==pygame.K_a and start and node:
                    pass
                    # astar(lambda: draw(surface, grid),grid, start, end)
    pygame.quit()
    


if __name__=="__main__":
    main()
   