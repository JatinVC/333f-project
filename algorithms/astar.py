'''
astar.py version 1.0.0
the algorithm for A* Search
'''

import sys
# to import stuff from main.py
sys.path.append('./')
import time
from collections import deque
from queue import PriorityQueue

BLACK = (0, 0, 0)
WHITE=(255,255,255)

def mh(c1, c2):
    start_x, start_y=c1
    end_x, end_y=c2
    return abs(start_x - end_x)+ abs(start_y-end_y)

            
def astar(draw, grid, start, end, construct_path, message_box):
    count=0
    rowNum=[-1, 1, 0, 0]
    colNum=[0 ,0 ,-1 ,1]
    
    open_set=PriorityQueue()
   
    parent={}

    g_score={col: sys.maxsize for row in grid for col in row}
    f_score={col: sys.maxsize for row in grid for col in row}
    g_score[start]=0
    f_score[start]=mh((start.row, start.col),(end.row, end.col))

    open_set.put((0, count, start))
    open_set_hash={start}
    
    def isValid(row, col):
        return (row>=0) and (row<=49) and (col>=0) and (col<=49)
    
    
    while not open_set.empty() :
        q=open_set.get()[2]
        open_set_hash.remove(q)
        
        if q==end:
            end.make_end()
            construct_path(q, parent, start)
            return True
            
        
        for i in range(4):
            
            row=q.row+ rowNum[i]
            col=q.col+ colNum[i]

            
            if (isValid(row, col) and grid[row][col].color!=BLACK ):
                node=grid[row][col]
                temp_g_score=g_score[q]+1
                if temp_g_score<g_score[node]:
                    g_score[node]=temp_g_score
                    parent[node]=q
                    f_score[node]=temp_g_score+ mh((node.row, node.col),(end.row, end.col))

                    if node not in open_set_hash:
                        count+=1
                        open_set.put((f_score[node], count, node))
                        open_set_hash.add(node)
                        node.edge_color()
                        
                    time.sleep(0.005)
                    draw()

            if q!=start:
                q.visited_cell()
                
    
    message_box()
    return False  