import pygame
import random
import pandas as pd
import numpy as np
import time
from queue import PriorityQueue

#Generate True and False with a probablity of 28:72
start_time=time.time()
def true22_false78():
    if random.randrange(100)<28:
        return False
    else:
        return True

path=[]
fullpath=[]
mazematrix=[]
##########################################
RES = WIDTH, HEIGHT = 848, 848
TILE = 16
cols, rows = WIDTH // TILE, HEIGHT // TILE

pygame.init()
sc= pygame.display.set_mode(RES)
clock=pygame.time.Clock()
pac = pygame.image.load("mario.png").convert()
pac = pygame.transform.scale(pac, (16, 16))

ghost = pygame.image.load("ghost.png").convert()
ghost = pygame.transform.scale(ghost, (16, 16))

wall = pygame.image.load("brick.png").convert()
wall = pygame.transform.scale(wall, (16, 16))

##Class to draw the pygame
class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.Block = mazematrix[x][y]["Path"]
        self.visited = mazematrix[x][y]["Visited"]

    def draw(self):
        possiblepath=0
        x1, y1 = self.x*TILE, self.y*TILE        
        if (self.x,self.y) in fullpath:    
            pygame.draw.rect(sc, pygame.Color('orange'), (x1, y1,TILE, TILE))
            possiblepath=1

        if self.visited:
            pygame.draw.rect(sc, pygame.Color('darkgrey'), (x1, y1,TILE, TILE))

        if not self.Block:
            pygame.draw.rect(sc, pygame.Color('brown'), (x1, y1,TILE, TILE))
        if self.Block=="BLOCK":
            sc.blit(wall, (x1, y1))

    def draw_current_cell(self):
        x,y=self.x*TILE,self.y*TILE
        sc.blit(pac, (x, y))
        # pygame.draw.rect(sc, pygame.Color('blue'), (x, y,TILE, TILE))
    def draw_ghost(self):
        x,y=self.x*TILE,self.y*TILE
        sc.blit(ghost, (x, y))
####will return the neighbors for any given cell including cells with ghosts
    def check_neighbors(self):
        x,y=self.x,self.y
        neighbors=[]
        if mazematrix[x+1][y]["Path"]==True: 
            neighbors.append((x+1,y))
        if mazematrix[x][y+1]["Path"]==True:
            neighbors.append((x,y+1))
        if mazematrix[x-1][y]["Path"]==True:
            neighbors.append((x-1,y))
        if mazematrix[x][y-1]["Path"]==True:
            neighbors.append((x,y-1))
        return neighbors
##Random Ghost movement
def move_ghost(x,y):
    pp=[]
    top = mazematrix[x][y+1]["Path"]
    right = mazematrix[x+1][y]["Path"]
    bottom = mazematrix[x][y-1]["Path"]
    left = mazematrix[x-1][y]["Path"]
    if top!="BLOCK":
        pp.append((x,y+1))
    if right!="BLOCK":
        pp.append((x+1,y))
    if bottom!="BLOCK":
        pp.append((x,y-1))
    if left!="BLOCK":
        pp.append((x-1,y))
    new_loc=random.choice(pp)
    if mazematrix[new_loc[0]][new_loc[1]]["Path"]:
        return new_loc
    else:
        if random.choice([0,1])==1:
            return new_loc
        else:
            return (x,y)

###Function to return manhattan distance between 2 points
def h(p1, p2):
	return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

#######for priority queue A star path
def astarsearch(start):
    count=0
    PQ = PriorityQueue()
    PQ.put((0, count, start))
    came_from = {}
    g = {(col, row): float("inf") for row in range(rows) for col in range(cols)}
    g[start] = 0
    f = {(col, row): float("inf") for row in range(rows) for col in range(cols)}
    f[start] = h(start, (51,51))
    PQ_list = {start}
    while True:
        current = PQ.get()[2]
        PQ_list.remove(current)
        Cell(current[0],current[1]).visited = True
        if current == (51,51):
            l=0
            patha=[]
            while current in came_from:
                current = came_from[current]
                patha.append(current)
                l=l+1
            patha.insert(0,(51,51))
            patha=patha[:-1]
            return patha

        for neighbor in Cell(current[0],current[1]).check_neighbors():
            temp_g = g[current] + 1
            if temp_g < g[neighbor]:
                came_from[neighbor] = current
                g[neighbor] = temp_g
                f[neighbor] = temp_g + h(neighbor, (51,51))
                if neighbor not in PQ_list:
                    count += 1
                    PQ.put((f[neighbor], count, neighbor))
                    PQ_list.add(neighbor)
            
        if len(PQ_list)==0:
            return "no possible path"

####To run the agent multiple times and store the result in pandas dataframe
data_export=[["number of ghost","number of steps taken","PATH","success/failure"]]
number_ghost=0
while (number_ghost!=200):
    number_ghost=number_ghost+5   ######increment value of ghost =5
    print(number_ghost)
    s_loop=0
    while s_loop<50:    #####number of simulations for each number of ghosts
        s_loop+=1
        flag=0
        print(s_loop)
        win_lose="success"
        simulation_data=[number_ghost]
        mazematrix=[]
        row=[]
        run=True
        #Create MAZE
        for i in range(53):
            for j in range(53):
                if i==0 or i==52:
                    row.append({"Visited":False, "Ghost":False,"Path":"BLOCK"})
                else:
                    row.append({"Visited":False, "Ghost":False,"Path":true22_false78()})
            
            row[0]["Path"]="BLOCK"
            row[-1]["Path"]="BLOCK"    
            mazematrix.append(row)
            row=[]
        #check the existence of a path in the maze
        if mazematrix[1][1]["Path"]==False or mazematrix[51][51]["Path"]==False:
            s_loop-=1
            continue
            run=False
        mazematrix=np.array(mazematrix)
        # print(mazematrix)
        ######To store all possible ghost spawn location then spawn n ghosts randomly among these locations
        possible_ghost_locations=[]
        ghost_locations=[]
        for i in range(53):
            for j in range(53):
                if mazematrix[i][j]["Path"]==True:
                    possible_ghost_locations.append((i,j))
        for i in range(number_ghost):  #number of ghost
            ghost_locations.append(random.choice(possible_ghost_locations))

        # print(ghost_locations)
        #####Check if all ghosts can reach the agent
        for i in ghost_locations:
            if astarsearch(i)=="no possible path":
                s_loop-=1
                flag=1
                run=False
                break
        if(flag==1):
            continue
        
        current_cell=(1,1)
        mazematrix[1][1]["Visited"]=True
        #### To check the existence of a path in the maze
        path=astarsearch(current_cell)
        if path=="no possible path":
            # print(path)
            s_loop-=1
            continue
            run=False
        else:
            simulation_data.append(len(path))
            simulation_data.append(path)
###### RUN the Agent after all MAZE check is passed
        while run:
            ### DRAW pygame
            sc.fill(pygame.Color("black"))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run=False
            for i in range(53):
                for j in range(53):
                    Cell(i,j).draw()

            if len(path)>0:
                fullpath=path
                Cell(path[-1][0],path[-1][1]).draw_current_cell()
                ####Check if agent dies when it moves
                if path[-1] in ghost_locations:
                    # print("Death By Ghost")
                    win_lose="Death"
                    run=False
                current_cell=path[-1]
                mazematrix[current_cell[0]][current_cell[1]]["Visited"]=True
            else:
                run=False
            #### Draw the ghosts
            for i in ghost_locations:
                Cell(i[0],i[1]).draw_ghost()
            #### move the ghosts and store in a new location
            k=0
            for i in ghost_locations:
                ghost_locations[k]=move_ghost(i[0],i[1])
                k=k+1
            #### Check if agent dies when ghost moves
            if current_cell in ghost_locations:
                # print("Death By Ghost")
                win_lose="Death"
                run=False
            path=path[:-1]
            pygame.display.flip()
            clock.tick(6)
        simulation_data.append(win_lose)
        data_export.append(simulation_data)


logdf = pd.DataFrame(data_export)
logdf.to_excel('agent1log.xlsx')

print(time.time()-start_time)