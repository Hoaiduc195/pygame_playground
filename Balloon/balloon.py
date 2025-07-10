import pygame
from sys import exit
from random import randint
from math import sqrt

############ CREATED BY DUCKIE195 IN 10.7.2025 ############

pygame.init()
# 
WIDTH = 800
HEIGHT = 400
BG_COLOR = (255, 255, 255)
font = pygame.font.Font("fonts/arcadeclassic/ARCADECLASSIC.TTF", 30)
#
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FRICTION_FACTOR = 0.9

###
# FUNCTIONS
def right_mouse_pressed():
    mouse = pygame.mouse.get_pressed()
    return mouse[2]

def left_mouse_pressed():
    mouse = pygame.mouse.get_pressed()
    return mouse[0]

def apply_gravity(planet_list, gravity):
    for planet in planet_list:
        planet["position"][1] += gravity

def set_floor(planet_list):
    for planet in planet_list:
        if planet["position"][1]+planet["radius"] >= HEIGHT: planet["position"][1] = HEIGHT - planet["radius"] 
        
def display(planet_list):
    for planet in planet_list:
        pygame.draw.circle(screen, planet["color"], planet["position"], planet["radius"])
        planet["position"][0] += planet["velocity"][0]
        planet["position"][1] += planet["velocity"][1]
        planet["velocity"][0] *= FRICTION_FACTOR
        planet["velocity"][1] *= FRICTION_FACTOR
    
def compute_distance(planet, origin):
    d_x = abs(planet["position"][0] - origin[0])
    d_y = abs(planet["position"][1] - origin[1])
    return (float)(sqrt(d_x*d_x + d_y*d_y))

def compute_velocity(planet, origin, real_velocity, distance):
    d_x = planet["position"][0] - origin[0]
    d_y = planet["position"][1] - origin[1]
    planet["velocity"][0] = real_velocity * d_x / distance
    planet["velocity"][1] = real_velocity * d_y / distance
    
def apply_force(planet_list, force_origin, radius):
    for planet in planet_list:
        distance = compute_distance(planet, force_origin)
        if distance == 0: continue
        if distance <= radius:
            compute_velocity(planet, force_origin, 20, distance)
        # else: planet["velocity"] = [0, 0] 

def reset_velocity(planet_list):
    for planet in planet_list:
        planet["velocity"] = [0, 0]
        
def set_border(planet_list):
    for planet in planet_list:
        if planet["position"][0]-planet["radius"]<=0: planet["position"][0]=planet["radius"]
        if planet["position"][1]-planet["radius"]<=0: planet["position"][1]=planet["radius"]
        if planet["position"][0]+planet["radius"]>=WIDTH: planet["position"][0]=WIDTH-planet["radius"]
        if planet["position"][1]+planet["radius"]>=HEIGHT: planet["position"][1]=HEIGHT-planet["radius"]
        
def set_border_bouncable(planet_list):
    for planet in planet_list:
        if planet["position"][0]-planet["radius"]<=0: # touch left
            planet["position"][0] = planet["radius"]+1
            planet["velocity"][0] *= -1
        if planet["position"][1]-planet["radius"]<=0: # touch up
            planet["position"][1] = planet["radius"]+1
            planet["velocity"][1] *= -1
        if planet["position"][0]+planet["radius"]>=WIDTH: # touch right
            planet["position"][0] = WIDTH-planet["radius"]-1
            planet["velocity"][0] *= -1
        if planet["position"][1]+planet["radius"]>=HEIGHT: # touch down
            planet["position"][1]=HEIGHT-planet["radius"]-1
            planet["velocity"][1] *= -1
###
planet_list = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill(BG_COLOR)            

    if right_mouse_pressed():
        mouse_pos = pygame.mouse.get_pos()
        new_planet = {
            "position": list(mouse_pos),
            "radius": randint(10, 30),
            "velocity": [0, 0],
            "color": (randint(0,255),randint(0,255),randint(0,255))
        }
        planet_list.append(new_planet)
        # print(f"Create a planet, current size of planet_list: {len(planet_list)}\n")
    if left_mouse_pressed():
        mouse_pos = pygame.mouse.get_pos()
        apply_force(planet_list, list(mouse_pos), 50)
    
    display(planet_list)
    set_border(planet_list)
    set_border_bouncable(planet_list)
    pygame.display.update()
    clock.tick(60) 