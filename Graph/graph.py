import pygame
from sys import exit
from random import randint
from math import sqrt

pygame.init()
#
WIDTH = 1000
HEIGHT = 600
BG_COLOR = (0,0,0)
font = pygame.font.Font(None, 30)
FRAME_RATE = 60
#
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FRICTION_FACTOR = 0.9

###
# FUNCTION
def read_file(filename, edges):
    with open(filename, "r") as file:
        for line in file:
            edge = [int(x) for x in line.strip().split()]
            edges.append(edge)
    
def retrieve_node(edges, adjacency_list, nodes):
    for edge in edges:
        u, v = edge
        if u not in adjacency_list:
            adjacency_list[u] = []
        if v not in adjacency_list:
            adjacency_list[v] = []
        adjacency_list[u].append(v)
        adjacency_list[v].append(u)

    for key in adjacency_list:
        node = {
            "name": key,
            "color": (randint(100, 255), randint(100, 255), randint(100, 255)),
            "radius": randint(30, 40),
            "position": [randint(40, WIDTH - 40), randint(40, HEIGHT - 40)],
            "adj":adjacency_list[key], 
            "velocity": [randint(-5, 5), randint(-5, 5)]
        }
        nodes[key] = node
        
def draw_node(nodes):
    # draw lines
    for node_id in nodes:
        node = nodes[node_id]
        for adj_node_id in node["adj"]:
            adj_node = nodes[adj_node_id]
            adj_node_pos = adj_node["position"]
            pygame.draw.line(screen, "GREY", node["position"], adj_node_pos, 5)
        
    # draw nodes
    for node_id in nodes:
        node = nodes[node_id]
        pygame.draw.circle(screen, node["color"], node["position"], node["radius"])
        node_name_text = font.render(f"{node['name']}", False, "black")
        node_name_rect = node_name_text.get_rect(center = node["position"])
        screen.blit(node_name_text, node_name_rect)
        node["position"][0] += node["velocity"][0]
        node["position"][1] += node["velocity"][1]
        node["velocity"][0] *= FRICTION_FACTOR
        node["velocity"][1] *= FRICTION_FACTOR
        
def compute_distance(position_1, position_2):
    dx = position_1[0] - position_2[0]
    dy = position_1[1] - position_2[1]
    return sqrt(dx*dx + dy*dy)

def interact_with_node(nodes):
    mouse_pos = pygame.mouse.get_pos()
    for node_id in nodes:
        node = nodes[node_id]
        surrounding = 20
        if pygame.mouse.get_pressed() == (1, 0, 0) and compute_distance(node["position"], mouse_pos) < node["radius"] + surrounding:
            # v_x = list(mouse_pos)[0] - node["position"][0]
            # v_y = list(mouse_pos)[1] - node["position"][1]
            # node["velocity"] = [v_x, v_y]
            node["position"] = list(mouse_pos)

def solid_node(nodes):
    for node_id in nodes:
        for another_node_id in nodes:
            if node_id == another_node_id: continue
            node = nodes[node_id]
            another_node = nodes[another_node_id]
            if compute_distance(node["position"], another_node["position"]) <= node["radius"] + another_node["radius"]:
                v_x = node["position"][0] - another_node["position"][0]
                v_y = node["position"][1] - another_node["position"][1]
                if(not v_x and not v_y ):
                    rand_v = [randint(-5, 5), randint(-5, 5)]
                    _rand_v = [-_ for _ in rand_v]
                    node["velocity"] = rand_v
                    another_node["velocity"] = _rand_v
                else:
                    real_velocity_factor = 0.05
                    node["velocity"] = [v_x*real_velocity_factor, v_y*real_velocity_factor]
                    another_node["velocity"] = [-v_x*real_velocity_factor, -v_y*real_velocity_factor]

def set_border(nodes):
    for node_id in nodes:
        node = nodes[node_id]
        r = node["radius"]
        x = node["position"][0]
        y = node["position"][1]
        if x - r <= 0:
            node["position"][0] = r+1
            node["velocity"][0] *= -1
        if x + r >= WIDTH:
            node["position"][0] = WIDTH-r-1
            node["velocity"][0] *= -1
        if y - r <= 0:
            node["position"][1] = r+1
            node["velocity"][1] *= -1
        if y + r >= HEIGHT:
            node["position"][1] = HEIGHT-r+1
            node["velocity"][1] *= -1

###
adjacency_list = {}
edges = []
nodes = {}

read_file("graph.txt", edges)
retrieve_node(edges, adjacency_list, nodes)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
    screen.fill(BG_COLOR)
    draw_node(nodes)
    interact_with_node(nodes)
    solid_node(nodes)
    set_border(nodes)
    pygame.display.update()
    clock.tick(FRAME_RATE)