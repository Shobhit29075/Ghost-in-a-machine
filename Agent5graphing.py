import pygame
import random
import pandas as pd
import numpy as np
import time
from queue import PriorityQueue


start_time=time.time()
def true28_false72():
    if random.randrange(100)<28:
        return False
    else:
        return True

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
            pygame.draw.rect(sc, pygame.Color('darkgray'), (x1, y1,TILE, TILE))

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
### Check neighbors and exclude those that are even close to ghosts
    def check_neighbors(self):
        x,y=self.x,self.y
        neighbors=[]
        if mazematrix[x+1][y]["Path"]==True  and (x+1,y) not in ghostbubble: 
            neighbors.append((x+1,y))
        if mazematrix[x][y+1]["Path"]==True  and (x,y+1) not in ghostbubble:
            neighbors.append((x,y+1))
        if mazematrix[x-1][y]["Path"]==True  and (x-1,y) not in ghostbubble:
            neighbors.append((x-1,y))
        if mazematrix[x][y-1]["Path"]==True  and (x,y+1) not in ghostbubble:
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
            return [new_loc[0],new_loc[1]]     ####################chnages made for agent5
        else:
            return (x,y)

def ghost_nearby(gl):
    gb=[]
    for i in gl:
        gb.append((i[0],i[1]))
        gb.append((i[0]+1,i[1]))
        gb.append((i[0]-1,i[1]))
        gb.append((i[0],i[1]-1))
        gb.append((i[0],i[1]+1))
    return gb

def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

def run_away_nearest_ghost(current_cell):
    distance_from_ghosts=[]
    #FIND distance from all ghosts and store it in an array
    for i in ghost_locations:
        distance_from_ghosts.append(h(current_cell,i))
    #find the minimun of the distance array to determine the closest ghost
    closest_ghost=ghost_locations[distance_from_ghosts.index(min(distance_from_ghosts))]
    distance_after_move=[]
    neighbors=Cell(current_cell[0],current_cell[1]).check_neighbors()
    neighbors.append(current_cell)
    #check the distance from that closest ghost to all the neighbors of the current cell including the current cell
    for neighbor in neighbors:
        distance_after_move.append(h(closest_ghost,neighbor))
    #return the neighbor with max distance from the ghost as current cell
    if len(neighbors)>0:
        current_cell=neighbors[distance_after_move.index(max(distance_after_move))]
    return current_cell

#######for priority queue A star
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
        fullpathtraverse=False
        win_lose="success"
        simulation_data=[number_ghost]
        row=[]
        run=True
        mazematrix=[]
        #Create MAZE
        for i in range(53):
            for j in range(53):
                if i==0 or i==52:
                    row.append({"Visited":False, "Path":"BLOCK"})
                else:
                    row.append({"Visited":False, "Path":true28_false72()})
            
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
        possible_ghost_locations=[]
        ghost_locations=[]
        ghostbubble=[]
        # print(ghost_locations)
        current_cell=(1,1)
        Actualpath=[]
        mazematrix[1][1]["Visited"]=True
        path=astarsearch(current_cell)
        #### To check the existence of a path in the maze
        if path=="no possible path":
            # print(path)
            s_loop-=1
            continue
            run=False
######To store all possible ghost spawn location then spawn n ghosts randomly among these locations
        for i in range(53):
            for j in range(53):
                if mazematrix[i][j]["Path"]==True:
                    possible_ghost_locations.append((i,j))
        for i in range(number_ghost):  #number of ghost
            ghost_locations.append(random.choice(possible_ghost_locations))
        
        for i in ghost_locations:
            if astarsearch(i)=="no possible path":
                s_loop-=1
                flag=1
                run=False
                break
        if(flag==1):
            continue
        possible_ghost_locations=ghost_locations.copy()
        ghostbubble=ghost_nearby(ghost_locations)
        path=astarsearch(current_cell)
        ###### RUN the Agent after all MAZE check is passed
        while run:
            sc.fill(pygame.Color("black"))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run=False
            for i in range(53):
                for j in range(53):
                    Cell(i,j).draw()

            ####without this it takes about 2min for 300 simulations..90 sec with this
            if path=="no possible path":
                path=astarsearch(current_cell)
            elif len(list(set(path) & set(ghostbubble)))!=0:
                path=astarsearch(current_cell)

            if path=="no possible path":
                if len(list(set(ghost_nearby([(current_cell[0],current_cell[1])])) & set(ghostbubble)))!=0:
                    current_cell=run_away_nearest_ghost(current_cell)
                    print(current_cell)
                    fullpathtraverse=False
                elif fullpathtraverse==True:
                    current_cell=fullpath[-1]
                    fullpath=fullpath[:-1]
                mazematrix[current_cell[0]][current_cell[1]]["Visited"]=True
                Cell(current_cell[0],current_cell[1]).draw_current_cell()
                # pathtravelled.append(current_cell)
                ####Check if agent dies when it moves
                if current_cell in ghost_locations:
                    win_lose="Death"
                    run=False

            elif len(path)>0:
                
                Cell(path[-1][0],path[-1][1]).draw_current_cell()
                ####Check if agent dies when it moves
                if path[-1] in ghost_locations:
                    # print("Death By Ghost")
                    win_lose="Death"
                    run=False
                current_cell=path[-1]
                path=path[:-1]
                fullpath=path.copy()
                fullpathtraverse=True
                mazematrix[current_cell[0]][current_cell[1]]["Visited"]=True
            else:
                run=False
            
            k=0
            for i in ghost_locations:
                ghost_locations[k]=move_ghost(i[0],i[1])
                k=k+1
            
            k=0
            for i in ghost_locations:
                if(type(i)==tuple):
                    possible_ghost_locations[k]=i
                k=k+1
            ghostbubble=ghost_nearby(possible_ghost_locations)

            for i in ghost_locations:
                Cell(i[0],i[1]).draw_ghost()
####Check if agent dies when ghost moves
            if current_cell in ghost_locations:
                # print("Death By Ghost")
                win_lose="Death"
                run=False
            Actualpath.append(current_cell)
            if (current_cell==(51,51)):
                run=False
            pygame.display.flip()
            clock.tick(10)
        simulation_data.append(len(Actualpath))
        simulation_data.append(Actualpath)
        simulation_data.append(win_lose)
        data_export.append(simulation_data)

logdf = pd.DataFrame(data_export)
logdf.to_excel('agent5log.xlsx')

print(time.time()-start_time)