'''
bfs.py version 1.0.0
the algorithm for breadth first Search
'''

import sys
# to import stuff from main.py
sys.path.append('./')
import time
from collections import deque

BLACK = (0, 0, 0)
WHITE=(255,255,255)

def bfs(draw, grid, start, end, message_box, construct_path):
    
    print(end.row, end.col)
    col=len(grid[1])
    rows=len(grid)
    visited=[[False for i in range(col)] for j in range(rows)]
    visited[start.row][start.col]=True

    queue=deque()
    queue.append(start)

    def isValid(row, col):
        return (row>=0) and (row<=49) and (col>=0) and (col<=49) 

    prev={}
    
    rowNum=[-1, 1,0,0]
    colNum=[0 ,0 ,-1 ,1]
    
    while queue:
                    
        curr=queue.popleft()
        
        if curr!=start :
            curr.visited_cell()
                
            
        if curr==end:
            curr.make_end()
            construct_path(curr, prev, start)
            return True

        else:
            for i in range(4):
                row=curr.row+ rowNum[i]
                col=curr.col+ colNum[i]

                if (isValid(row, col) and grid[row][col].color!=BLACK and not visited[row][col]):
                    node=grid[row][col]
                    queue.append(node) 
                    visited[row][col] =True
                    node.edge_color()
                    prev[node]=curr
                time.sleep(0.001) 
                draw()
    message_box()   