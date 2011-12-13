#!/usr/bin/env python

import pygame
import random
import sys

# init all
pygame.init()

screen_x = 320 # in future use size of BG
screen_y = 200
screen = pygame.display.set_mode((screen_x, screen_y))

pygame.mouse.set_visible(0)

bg = []
bg.append(pygame.image.load("img/forrest1.png").convert_alpha())
bg.append(pygame.image.load("img/forrest2.png").convert_alpha())
bg.append(pygame.image.load("img/forrest3.png").convert_alpha())
bg.append(pygame.image.load("img/forrest4.png").convert_alpha())

shadow = pygame.Surface((screen_x, screen_y), pygame.SRCALPHA)
shadow.fill((0,0,0,100))

deer_img = pygame.image.load("img/deer.png").convert_alpha()
leaf_img = pygame.image.load("img/leaf.png").convert_alpha()

pygame.display.set_caption('Forrest')
pygame.display.set_icon(leaf_img)

timer = pygame.time.Clock()

print "init done"

class Leaf:
    def __init__(self, position, speed, image):
        self.position = position
        self.speed = speed
        self.image = image
        self.image_w = self.image.get_size()[0]/2
        self.image_h = self.image.get_size()[1]/2
        self.angle = 0

    def move(self):
        self.position[0] += self.speed[0]*random.randrange(0,3)
        self.position[1] += self.speed[1]

    def draw(self):
        self.angle -= 5

        screen.blit (pygame.transform.rotate(self.image, self.angle), (self.position[0]-self.image_w, self.position[1]-self.image_h)) # with rotation
        
    def crash(self, pos):
        limit = (self.position[0]-pos[0])**2 + (self.position[1]-pos[1])**2
        if limit < ((self.image_w + self.image_w)/2) **2:
            return 1


def main():
    leaves = []
    for member in bg:
        leaves.append([])

    x = 0
    y = 0
    deep = 1
    
    step = 2
    
    counter = 0

    while(1):
        counter += 1
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if keys[pygame.K_ESCAPE]:
                sys.exit()
            if keys[pygame.K_f]:
                pygame.display.toggle_fullscreen()
            if keys[pygame.K_UP]:
                if deep < len(bg)-1:
                    deep += 1
            if keys[pygame.K_DOWN]:
                if deep > 1:
                    deep -= 1
        if keys[pygame.K_RIGHT]:
            x -= step
        if keys[pygame.K_LEFT]:
            x += step

        # drawing forrest
        for i,img in reversed(list(enumerate(bg))):
            #trees
            screen.blit( img, ( (x//(i+2))%img.get_width(), y) )
            screen.blit( img, ( (x//(i+2))%img.get_width()-img.get_width(), y) )
            
            #leaves
            for one in leaves[i][:]:
                one.move()
                # check of screen limits
                if one.position[1] > screen_y+leaf_img.get_size()[1]:
                    leaves[i].remove(one)
                # check of hit
                else:
                    one.draw()
            
            #shadow
            screen.blit(shadow, (0,0))
        
            #player
            if i == deep:
                #pygame.draw.circle( screen, (255,100,100), (screen_x//2, screen_y//2 +90 -25*deep), 30-deep**2 )
                #screen.blit(deer_img, (screen_x/2, screen_y/2 +20 -25*deep) )
                screen.blit( pygame.transform.scale(deer_img, (int(deer_img.get_size()[0]//(1+deep/5.)), int(deer_img.get_size()[1]//(1+deep/5.))) ), (screen_x//2, screen_y//2 +35 -20*deep) )
                
        #adding leaves
        if counter%10 == 0:
            leaves[random.randrange(0,len(leaves))].append(Leaf([random.randrange(leaf_img.get_size()[0], screen_x-leaf_img.get_size()[0]), -leaf_img.get_size()[1]], [random.randrange(-1,2),random.randrange(1,3)], leaf_img))

        
        pygame.display.flip()
        
        timer.tick(100)
        if counter > 100:
            print "fps", int(timer.get_fps())
            counter = 0

main()