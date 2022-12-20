import pygame


import math

pygame.init()
fps = 60 # frame rate
timer =pygame.time.Clock()
font = pygame.font.Font('freeansbold.ttf',32) # this is a free font
WIDTH = 900
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH,HEIGHT])
bgs = []
banners = []
guns= []
level = 1

for i in range(1,4): # from 1 to 3
    bgs.append(pygame.image.load(f'assetns/bgs/{i}.png'))
    bgs.append(pygame.image.load(f'assetns/banners/{i}.png'))
    bgs.append(pygame.image.load(f'assetns/guns/{i}.png'))

run = True
while run:
    timer.tick(fps)

    screen.fill('black')
    screen.blit(bgs[level-1], (0,0)) # placing in the top left corner
    screen.blit(banners[level - 1],(0, HEIGHT-200))

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run = False
    
    pygame.display.flip()