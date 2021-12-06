import sys
# to import stuff from main.py
sys.path.append('./')
from main import message_box, construct_path
import time

BLACK = (0, 0, 0)
WHITE=(255,255,255)

def dijkstra(draw, grid, start, end):
    rowNum=[-1, 1,0,0]
    colNum=[0 ,0 ,-1 ,1]
    
    col_1=len(grid[1])
    rows_1=len(grid)
    

                
    def isValid(row, col):
        return (row>=0) and (row<=49) and (col>=0) and (col<=49)
    
    distance={col: sys.maxsize for row in grid for col in row}
    distance[start]=0
    visited_set=[]
    from_list={}
    

    
    def get_min_distance(grid, distance, visited):
#        mini=min(distance2, key=distance.get)

#        if mini not in visited and mini.color!=BLACK:
#            mini_index=mini
#        else:
#            print("nop")
#        return mini_index
            
       try:
           min = sys.maxsize
           for u in distance:
               if distance[u] < min and u not in visited and u.color!=BLACK:
                   min = distance[u]
                   min_index = u
           return min_index
       except:
           min_index=False     
           return min_index

    total_cells=col_1 * rows_1
    state=len(visited_set)!=total_cells
    while state:
        
        current=get_min_distance(grid, distance, visited_set)
        if current==False:
            message_box()
            state=False
            return False
            
        visited_set.append(current)
        
        
        if current==end:
            end.make_end()
            construct_path(current, from_list, start)
            break
        
        
            
        if current!=start:
            current.visited_cell()

        for i in range(4):
            row=current.row+ rowNum[i]
            col=current.col+ colNum[i]

            if (isValid(row, col) and grid[row][col].color!=BLACK and grid[row][col] not in visited_set ):
                temp_dist=distance[current] + 1

                if temp_dist <  distance[grid[row][col]]:
                    distance[grid[row][col]]=temp_dist
                    
                    from_list[grid[row][col]]=current
                    grid[row][col].edge_color()
                from_list[grid[row][col]]=current
                grid[row][col].edge_color()
            
            
                time.sleep(0.001)
                draw()
                        
    
    return False