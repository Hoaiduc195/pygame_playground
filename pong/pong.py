import pygame
from sys import exit
from random import randint
import pygame.sprite

class Paddle(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((40, 80))
        self.image.fill("WHITE")
        self.rect = self.image.get_rect(center=position)
        self.velocity = 8
        self.friction_factor = 0.9
        
    def enable_motion(self):
        keys = pygame.key.get_pressed()
        if self.rect.centerx == 0:
            if keys[pygame.K_w]: self.rect.centery -= self.velocity
            if keys[pygame.K_s]: self.rect.centery += self.velocity
        else:
            if keys[pygame.K_UP]: self.rect.centery -= self.velocity
            if keys[pygame.K_DOWN]: self.rect.centery += self.velocity
        
    def set_border(self):
        if self.rect.top <= 0:
            self.rect.top = 1
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT - 1
            
    def update(self):
        self.set_border()
        self.enable_motion()
        

class Ball(pygame.sprite.Sprite):
    def __init__(self, position, radius, paddles):
        super().__init__()
        self.image = pygame.Surface((radius*2, radius*2))
        pygame.draw.circle(self.image, "WHITE",(radius, radius), radius)
        self.rect = self.image.get_rect(center = position)
        self.paddles = paddles
        self.radius = radius
        self.velocity = [5,randint(-2, 2)]
        
    def set_border(self):
        if self.rect.top <= 0:
            self.velocity[1] *= -1
        if self.rect.bottom >= HEIGHT:
            self.velocity[1] *= -1
    
    def enable_touch_paddle(self):
        for paddle in self.paddles:
            if abs(self.rect.centerx - paddle.rect.centerx) < self.radius + paddle.rect.width/2 and self.rect.left > 0 and self.rect.right < WIDTH and (self.rect.bottom > paddle.rect.top and self.rect.top < paddle.rect.bottom):
                self.velocity[0] *= -1
                paddle_factor = 1 if paddle.rect.x == 0 else -1
                if paddle.rect.centery - self.rect.centery: self.velocity[1] = paddle_factor*(2*max(1, self.velocity[1])*(paddle.rect.centery - self.rect.centery))/paddle.rect.width
                else:
                    self.velocity[1] = self.velocity[1]
            
 
    def enable_motion(self):
        self.rect.centerx += self.velocity[0]
        self.rect.centery += self.velocity[1]
        
    def update(self):
        self.enable_touch_paddle()
        self.enable_motion()
        self.set_border()
        self.refresh()
        
    def refresh(self):
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.rect.center = [WIDTH/2, HEIGHT/2]
            
    
        
pygame.init()
###
WIDTH = 800
HEIGHT = 400
BG_COLOR = (0,0,0)
FRAME_RATE = 60
font = pygame.font.Font(None, 50)
###
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pong")

###
paddle_left = Paddle((0, HEIGHT/2))
paddle_right = Paddle((WIDTH, HEIGHT/2))
ball = Ball((WIDTH/2, HEIGHT/2), 10, [paddle_left, paddle_right])
score_left = 0
score_right = 0
###

score_up = True
score_up_event_cooldown = pygame.USEREVENT + 1
pygame.time.set_timer(score_up_event_cooldown, 1000) 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == score_up_event_cooldown:
            score_up = True
    
    screen.fill(BG_COLOR)
    pygame.draw.line(screen, "GREY", (WIDTH/2, 0), (WIDTH/2, HEIGHT))
    paddle_left.update()
    paddle_right.update()
    screen.blit(paddle_left.image, paddle_left.rect)
    screen.blit(paddle_right.image, paddle_right.rect)
    
    score_left_surf = font.render(f"{score_left}", False, "WHITE")
    score_right_surf = font.render(f"{score_right}", False, "WHITE")
    
    score_left_rect = score_left_surf.get_rect(topright = ((WIDTH/2 - 10), 20))
    score_right_rect = score_right_surf.get_rect(topleft = ((WIDTH/2 + 10), 20))
    screen.blit(score_left_surf, score_left_rect)
    screen.blit(score_right_surf, score_right_rect)
    
    if score_up and ball.rect.centerx < 0:
        score_right += 1
        score_up = False
    if score_up and ball.rect.centerx > WIDTH:
        score_left += 1
        score_up = False
        
    # text_surf = font.render(f"V_y: {ball.velocity[1]}", False, "WHITE")
    # text_rect = text_surf.get_rect(topleft = (0,0))
    # screen.blit(text_surf, text_rect) 

    ball.update()
    screen.blit(ball.image, ball.rect)
    
    pygame.display.update()
    clock.tick(FRAME_RATE)