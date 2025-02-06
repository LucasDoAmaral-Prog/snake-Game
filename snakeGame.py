import time;
import random;

import pygame;
from pygame.locals import *

pygame.init();

WINDOW_WIDTH  = 600;
WINDOW_HEIGHT = 600;

block_Space = 10;

snake_Running = True;

pygame.display.set_caption("Snake Game");
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT));
clock_FPS = pygame.time.Clock()

X, Y = 0, 1

border_MAX = 596;
border_MIN = 4;

pos_Initial_X = WINDOW_WIDTH/2;
pos_Initial_Y = WINDOW_HEIGHT/2;

pos_Snake = [(pos_Initial_X, pos_Initial_Y), (pos_Initial_X  + block_Space, pos_Initial_Y), (pos_Initial_X + 2*block_Space, pos_Initial_Y), (pos_Initial_X + 4*block_Space, pos_Initial_Y) ];
snake_Surface = pygame.Surface((block_Space, block_Space));
velocity_Snake = 0.1;
direction_Snake = pygame.K_w;

time_Initial = time.time();

def sortApple():

    return random.randint(15, 585), random.randint(15, 585);

apple_Surface = pygame.Surface((block_Space, block_Space));
num_MaxApples = 5;
pos_Apple = [sortApple() for _ in range(num_MaxApples)]
initial_TimeApple = time.time();
apple_Timer = 10;
points_Apple = 0;
len_ListApple = len(pos_Apple);

font_PointsApple = pygame.font.SysFont('arial', 35, True, True);

def sortObstacle():

    coords_Verify = (random.randint(15, 585), random.randint(15, 585));
     
    for index in range(num_MaxApples):
        if (coords_Verify in pos_Apple) and (abs(coords_Verify[X] - pos_Apple[index][X]) < 10) and (abs(coords_Verify[Y] - pos_Apple[index][Y]) < 10) :
            sortApple();
        
    return coords_Verify;

coords_Obstacles = [];

obstacle_Surface = pygame.Surface((block_Space, block_Space));

while snake_Running:

    window.fill((68, 189,50));

    delta_Time = clock_FPS.tick(30);
    form_MRU = int((velocity_Snake * delta_Time));

    message_Points = f'Pontos: {points_Apple}'
    showText_Points = font_PointsApple.render(message_Points, True, (255, 255, 255));

    if (((not abs(pos_Snake[0][X] - WINDOW_WIDTH) < border_MIN ) and (not abs(pos_Snake[0][X] - WINDOW_WIDTH) > border_MAX)) and ((not abs(pos_Snake[0][Y] - WINDOW_HEIGHT) < border_MIN) and (not abs(pos_Snake[0][Y] - WINDOW_HEIGHT) > border_MAX))):
        snake_Running = True;
    else:
        snake_Running = False;

    for event in pygame.event.get():
        if (event.type == QUIT):

            pygame.quit();
            quit();

        if(event.type == pygame.KEYDOWN):
            if event.key in [pygame.K_a, pygame.K_s, pygame.K_w, pygame.K_d]: 
                if (event.key == pygame.K_a and direction_Snake == pygame.K_d):
                    continue;
                elif (event.key == pygame.K_w and direction_Snake == pygame.K_s):
                    continue;
                elif(event.key == pygame.K_s and direction_Snake == pygame.K_w):
                    continue;
                elif(event.key == pygame.K_d and direction_Snake == pygame.K_a):
                    continue
            
                direction_Snake = event.key;       

    if(direction_Snake == pygame.K_a):
        pos_Snake[0] = pos_Snake[0][X] - form_MRU, pos_Snake[0][Y];
    elif(direction_Snake == pygame.K_d):
        pos_Snake[0] = pos_Snake[0][X] + form_MRU, pos_Snake[0][Y];
    elif(direction_Snake == pygame.K_w):
        pos_Snake[0] = pos_Snake[0][X], pos_Snake[0][Y] - form_MRU;
    elif(direction_Snake == pygame.K_s):
        pos_Snake[0] = pos_Snake[0][X], pos_Snake[0][Y] + form_MRU;

            
    if((time.time() - initial_TimeApple > apple_Timer) and (len_ListApple == num_MaxApples)):

        pos_Apple.pop(1);
        pos_Apple.append(sortApple());
        initial_TimeApple = time.time();
    

    for index in range(len(pos_Snake) -1,0, -1):

        if(pos_Snake[0] == pos_Snake[index]):
            snake_Running = False;
            
        pos_Snake[index] = pos_Snake[index-1]


    for coords in pos_Snake:
         
        window.blit(snake_Surface, coords);
    
    for index in range(num_MaxApples):

        window.blit(apple_Surface, pos_Apple[index]);
        apple_Surface.fill((255, 0, 0));

        if (abs(pos_Apple[index][X] - pos_Snake[0][X]) < 6) and ( abs(pos_Apple[index][Y] - pos_Snake[0][Y]) < 6):

            pos_Snake.append((block_Space,block_Space))
            pos_Apple[index] = sortApple();
            points_Apple += 1;

            velocity_Snake = min(0.1 + (points_Apple/5) * 0.02, 0.5);
            if(points_Apple % 5 == 0 and points_Apple != 0):
                print("ola");
                coords_Obstacles.append(sortObstacle());
            break;
    
    for indexObs in range(len(coords_Obstacles)):
        window.blit(obstacle_Surface, coords_Obstacles[indexObs]);
        obstacle_Surface.fill((0, 0, 0));
    
    window.blit(showText_Points, (420,30))

    pygame.display.update();     

