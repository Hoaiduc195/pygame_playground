import pygame
import sys
import time
from queue import Queue

##################################################################
# INIT
pygame.init()
WIDTH = 800
HEIGHT = 400
BG_COLOR = (64, 64, 64)
# font = pygame.font.Font("fonts/arcadeclassic/ARCADECLASSIC.TTF", 30)
PIXEL_SIZE = 20
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("maze_solver")
##################################################################


##################################################################
#FUNCTIONS 
def display_pixels():
    for i in range(len(pixels)):
        for j in range(len(pixels[i])):
            if(pixels[i][j] == 0): pygame.draw.rect(screen, "BLACK", (j*PIXEL_SIZE, i*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE), 1) #nothing
            elif(pixels[i][j] == 1): pygame.draw.rect(screen, "GREY", (j*PIXEL_SIZE, i*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)) #hurdle
            elif(pixels[i][j] == 2): pygame.draw.rect(screen, "GREEN", (j*PIXEL_SIZE, i*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)) #startpoint
            elif(pixels[i][j] == 3): pygame.draw.rect(screen, "RED", (j*PIXEL_SIZE, i*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)) #endpoint
            elif(pixels[i][j] == 4): pygame.draw.rect(screen, "BLUE", (j*PIXEL_SIZE, i*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)) # path
            elif(pixels[i][j] == 5): pygame.draw.rect(screen, "PINK", (j*PIXEL_SIZE, i*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)) # shortest path
            
def compute_shortest_path():
    shortest_path = []
    current_point = endpoint
    while current_point != startpoint:
        current_point = parent[current_point]
        if(current_point != startpoint): shortest_path.append(current_point)
    shortest_path.reverse()
    return shortest_path

##################################################################

GAMESTATE = "STOPMODE"
rows = (int)(HEIGHT/PIXEL_SIZE)
cols = (int)(WIDTH/PIXEL_SIZE)
pixels = [[0 for _ in range(cols)] for _ in range(rows)]
visited = [[False for _ in range(cols)] for _ in range(rows)]
##################################################################
startpoint = (-1, -1)
endpoint = (-1, -1)
dir_x = [1, 0, -1, 0]
dir_y = [0, 1, 0, -1]
##################################################################
# Using stack and queue for iterating dfs and bfs
stack = []
queue = []
parent = {}
Shortest_path = list()
##################################################################

##################################################################
# GAME LOOP
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
    screen.fill("white")
    if GAMESTATE == 'STOPMODE':
        keys = pygame.key.get_pressed()
        if(pygame.mouse.get_pressed() == (True, False, False)):
            if(keys[pygame.K_s]):
                mouse_pos = pygame.mouse.get_pos()
                j = (int)(mouse_pos[0] / PIXEL_SIZE)
                i = (int)(mouse_pos[1] / PIXEL_SIZE) 
                if(startpoint != (-1, -1)):
                    pixels[startpoint[0]][startpoint[1]] = 0
                pixels[i][j] = 2
                startpoint = (i, j)
            elif(keys[pygame.K_e]):
                mouse_pos = pygame.mouse.get_pos()
                j = (int)(mouse_pos[0] / PIXEL_SIZE)
                i = (int)(mouse_pos[1] / PIXEL_SIZE) 
                if(endpoint != (-1, -1)):
                    pixels[endpoint[0]][endpoint[1]] = 0
                pixels[i][j] = 3
                endpoint = (i, j)
            elif(keys[pygame.K_z]):
                mouse_pos = pygame.mouse.get_pos()
                j = (int)(mouse_pos[0] / PIXEL_SIZE)
                i = (int)(mouse_pos[1] / PIXEL_SIZE)
                if(pixels[i][j] == 3):
                    endpoint = (-1, -1)
                elif(pixels[i][j] == 2):
                    startpoint = (-1, -1)
                pixels[i][j] = 0
            else:    
                mouse_pos = pygame.mouse.get_pos()
                j = (int)(mouse_pos[0] / PIXEL_SIZE)
                i = (int)(mouse_pos[1] / PIXEL_SIZE) 
                if(pixels[i][j] == 2): startpoint = (-1, -1)
                if(pixels[i][j] == 3): endpoint = (-1, -1)
                pixels[i][j] = 1
        display_pixels()    
        
        if(keys[pygame.K_SPACE] and keys[pygame.K_LSHIFT]):
            GAMESTATE = "BFSMODE"
            queue.append(startpoint)
            continue
        
        if(keys[pygame.K_SPACE]):
            GAMESTATE = "DFSMODE"
            stack.append(startpoint)
            continue
            
    elif GAMESTATE == 'DFSMODE': # DFS
        if(startpoint == (-1, -1) or endpoint == (-1, -1)):
            print("Require startpoint and endpoint")
            stack.clear()
            GAMESTATE = "STOPMODE"
        else:
            if len(stack) == 0:
                print("No path found")
                GAMESTATE = "STOPMODE"
                pixels = [[0 for _ in range(cols)] for _ in range(rows)]
                visited = [[False for _ in range(cols)] for _ in range(rows)]
                continue
            current_point = stack.pop()
            if(current_point == endpoint):
                print("Path found")
                time.sleep(1)
                pixels = [[0 for _ in range(cols)] for _ in range(rows)]
                visited = [[False for _ in range(cols)] for _ in range(rows)]
                GAMESTATE = "STOPMODE"
                continue
            if visited[current_point[0]][current_point[1]]: continue
            visited[current_point[0]][current_point[1]] = True
            if current_point != startpoint: pixels[current_point[0]][current_point[1]] = 4
            for i in range(4):
                nx = current_point[0] + dir_x[i]
                ny = current_point[1] + dir_y[i]
                if(0<=nx<rows and  0<=ny<cols and pixels[nx][ny]!=1 and visited[nx][ny] == False):
                    stack.append((nx, ny))
            display_pixels()
            
    elif GAMESTATE == 'BFSMODE': # BFS 
        if(startpoint == (-1, -1) or endpoint == (-1, -1)):
            print("Require startpoint and endpoint")
            queue.clear()
            GAMESTATE = "STOPMODE"
        else:
            if(len(queue) == 0):
                print("No path found")
                GAMESTATE = "STOPMODE"
                pixels = [[0 for _ in range(cols)] for _ in range(rows)]
                visited = [[False for _ in range(cols)] for _ in range(rows)]
                parent = {}
                continue
            else:
                current_point = queue.pop(0)
                if current_point == endpoint:
                    print("Path found")
                    GAMESTATE = "SHORTESTPATH"
                    queue.clear()
                    Shortest_path = compute_shortest_path()
                    continue
                
                if visited[current_point[0]][current_point[1]]: continue
                visited[current_point[0]][current_point[1]] = True
                if current_point != startpoint:
                    pixels[current_point[0]][current_point[1]] = 4
                for i in range(4):
                    nx = current_point[0] + dir_x[i]
                    ny = current_point[1] + dir_y[i]
                    if 0 <= nx < rows and 0 <= ny < cols and pixels[nx][ny]!=1 and visited[nx][ny]==False:
                        queue.append((nx, ny))
                        parent[(nx, ny)] = current_point
                display_pixels()
    elif GAMESTATE == "SHORTESTPATH":
        if(len(Shortest_path) == 0):
            time.sleep(3)
            GAMESTATE = "STOPMODE"
            pixels = [[0 for _ in range(cols)] for _ in range(rows)]
            visited = [[False for _ in range(cols)] for _ in range(rows)]
            parent = {}
            continue
        current_point = Shortest_path[0]
        pixels[current_point[0]][current_point[1]] = 5
        Shortest_path.pop(0)
        display_pixels()
        
        
    pygame.display.update()
    clock.tick(60)
##################################################################






