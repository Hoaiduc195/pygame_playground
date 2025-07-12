import pygame
from sys import exit
import random

pygame.init()

# ________________________________ #
FRAME_RATE = 60
WIDTH = 800
HEIGHT = 400
BG_COLOR = (44, 62, 80)
BAR_N = 30
BAR_W = WIDTH / BAR_N
BAR_H_FACTOR = 3
font = pygame.font.Font(None, 30)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
GAMESTATE = "STOPMODE"
# ________________________________ #


# ___________FUNCTIONS____________ #
def display(bars):
    index = 0
    for bar in bars:
        left = index*BAR_W
        top = HEIGHT - bar["height"]
        bar_surf = pygame.Rect(left, top, BAR_W, bar["height"])
        pygame.draw.rect(screen, bar["color"], bar_surf)
        pygame.draw.rect(screen, "BLACK", bar_surf,1)
        bar["color"] = "WHITE"
        index += 1
    pygame.time.delay(20)
            
def draw_swap(bars, i, j):
    bars[i], bars[j] = bars[j], bars[i]
    bars[i]["color"] = bars[j]["color"] = "GREEN"
    
def scramble(bars):
    random.shuffle(bars)
    display(bars)
    
    
def merge(bars, bars_A, bars_B):
    i = 0
    j = 0
    k = 0
    while i<len(bars_A) and j<len(bars_B):
        if bars_A[i]["height"] < bars_B[j]["height"]:
            bars[k] = bars_A[i]
            k += 1
            i += 1
        else:
            bars[k] = bars_B[j]
            k += 1
            j += 1
    while i < len(bars_A):
        bars[k] = bars_A[i]
        k += 1
        i += 1
    while j < len(bars_B):
        bars[k] = bars_B[j]
        k += 1
        j += 1
        
def merge_sort(bars, l, r):
    if (l<r):
        m = (l+r)//2
        merge_sort(bars, l, m)
        merge_sort(bars, m+1, r)
        
        bars_A = bars[l:m]
        bars_B = bars[m+1:r]
        merge(bars, bars_A, bars_B)
# ________________________________ #



# _____________INIT_______________ #
bars = []
for i in range(BAR_N):
    bar = {
        "height":(i+1)*BAR_H_FACTOR,
        "color": "WHITE",
        "position": [i*BAR_W,HEIGHT]
    }
    bars.append(bar)
# ________________________________ #


# ____________SLT_SORT____________ #
slt_current_bar_idx = 0
slt_current_index = 0
slt_running_idx = 1
# ________________________________ #


#_____________INS_SORT____________ #
ins_current_bar_idx = 1
ins_running_idx = 1
# ________________________________ #


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
    screen.fill(BG_COLOR)
    keys = pygame.key.get_pressed()
    if GAMESTATE == "STOPMODE":
        if(keys[pygame.K_SPACE]):
            # print("SPace")
            scramble(bars)
        if keys[pygame.K_s]:
            GAMESTATE = "SLT_SORT"
            continue
        if keys[pygame.K_i]:
            GAMESTATE = "INS_SORT"
            continue
        
    elif GAMESTATE == "SLT_SORT":
        if keys[pygame.K_ESCAPE]:
            GAMESTATE = "STOPMODE"
            slt_current_bar_idx = 0
            slt_current_index = 0
            slt_running_idx = 1
            continue
        if slt_current_bar_idx == BAR_N - 1:
            GAMESTATE = "STOPMODE"
            slt_current_bar_idx = 0
            slt_current_index = 0
            slt_running_idx = 1
            continue
        
        if slt_running_idx == BAR_N:
            if slt_current_index != slt_current_bar_idx:
                draw_swap(bars, slt_current_index, slt_current_bar_idx)
            slt_running_idx = slt_current_bar_idx + 1
            slt_current_bar_idx += 1
            slt_current_index = slt_current_bar_idx
            continue
        
        bars[slt_running_idx]["color"] = "BLUE"
        if bars[slt_running_idx]["height"] < bars[slt_current_index]["height"]:
            slt_current_index = slt_running_idx
        slt_running_idx += 1
    
    elif GAMESTATE == "INS_SORT":
        if keys[pygame.K_ESCAPE]: 
            ins_current_bar_idx = 1
            ins_running_idx = 1
            GAMESTATE = "STOPMODE"
            continue
        
        if ins_current_bar_idx == BAR_N:
            ins_current_bar_idx = 1
            ins_running_idx = 1
            GAMESTATE = "STOPMODE"
            continue
        
        if ins_running_idx == 0 or bars[ins_running_idx - 1]["height"] < bars[ins_running_idx]["height"]:
            ins_current_bar_idx += 1
            ins_running_idx = ins_current_bar_idx
        else:
            draw_swap(bars, ins_running_idx, ins_running_idx-1)
            ins_running_idx -= 1
        

    
    display(bars)
    pygame.display.update()
    clock.tick(FRAME_RATE)

 