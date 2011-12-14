#!/usr/bin/env python

import pygame
import random
import sys
import glob

def toshow(image, deep):
    return pygame.transform.scale(image, (int(image.get_size()[0]//(1+deep/5.)), int(image.get_size()[1]//(1+deep/5.))) )

class Drop:
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

    def draw(self, screen, x):
        self.angle -= 5

        screen.blit( pygame.transform.rotate(self.image, self.angle), (x+ self.position[0]-self.image_w, self.position[1]-self.image_h) ) # with rotation
        
    def crash(self, pos):
        limit = (self.position[0]-pos[0])**2 + (self.position[1]-pos[1])**2
        if limit < ((self.image_w + self.image_w)/2) **2:
            return 1

class Animal:
    def __init__(self, position, direction, speed, image):
        self.position = position
        self.direction = direction
        self.speed = speed
        self.image = image

        if self.direction == 1:
            self.image = pygame.transform.flip( image, 1, 0)

    def move(self):
        if self.direction == 1:
            self.position[0] += self.speed
        else:
            self.position[0] -= self.speed

    def draw(self, screen, x):
        screen.blit( self.image, (x+ self.position[0], self.position[1]) )


def main():
    
    # init all
    pygame.init()

    screen_x = 320 # in future use size of BG
    screen_y = 200
    #screen = pygame.display.set_mode((screen_x, screen_y), pygame.FULLSCREEN)
    screen = pygame.display.set_mode((screen_x, screen_y))

    pygame.mouse.set_visible(0)

    bg = []
    bg.append(pygame.image.load("img/forrest1.png").convert_alpha())
    bg.append(pygame.image.load("img/forrest2_test.png").convert_alpha())
    bg.append(pygame.image.load("img/forrest3.png").convert_alpha())
    bg.append(pygame.image.load("img/forrest4.png").convert_alpha())
    
    #bg.append(pygame.image.load("img/snowforrest1.png").convert_alpha())
    #bg.append(pygame.image.load("img/snowforrest2.png").convert_alpha())
    #bg.append(pygame.image.load("img/snowforrest3.png").convert_alpha())
    #bg.append(pygame.image.load("img/snowforrest4.png").convert_alpha())

    #loading animals
    #animals_images_filenames = ["img/animals/weasel.png"]
    animals_images_filenames = glob.glob("img/animals/*.png")
    
    animals_images = []
    for filename in animals_images_filenames:
        animals_images.append( pygame.image.load( filename ).convert_alpha() )
    
    shadow = pygame.Surface((screen_x, screen_y), pygame.SRCALPHA)
    shadow.fill((0,0,0,110))

    player_img_left = pygame.image.load("img/animals/deer.png").convert_alpha()
    player_img = player_img_left

    drop_img = pygame.image.load("img/leaf.png").convert_alpha()
    #drop_img = pygame.image.load("img/snowflake.png").convert_alpha()

    cursor_img = pygame.image.load("img/cursor.png").convert_alpha()

    pygame.display.set_caption('Forrest')
    pygame.display.set_icon(drop_img)

    timer = pygame.time.Clock()

    print "init done"
    
    #global position
    x = 0
    y = 0
    deep = 1
    step = 2
    
    drops = []
    for member in bg:
        drops.append([])

    animals = []
    for member in bg:
        animals.append([])

    counter = 0
    mouseclick = False
    
    while(1):
        counter += 1

        adept_to_die = None

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if keys[pygame.K_ESCAPE]:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouseclick = True
                hitforrest = []

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
            player_img = pygame.transform.flip( player_img_left, 1, 0)
        if keys[pygame.K_LEFT]:
            x += step
            player_img = player_img_left

        # drawing forrest
        for i,img in reversed(list(enumerate(bg))):
            #trees
            forrest_draw_pos1 = (x//(i+2))%img.get_width(), y
            forrest_draw_pos2 = (x//(i+2))%img.get_width()-img.get_width(), y

            #screen.blit( img, ( (x//(i+2))%img.get_width(), y) )
            #screen.blit( img, ( (x//(i+2))%img.get_width()-img.get_width(), y) )
            screen.blit( img, ( (x//(i+2))%img.get_width(), y) )
            screen.blit( img, ( (x//(i+2))%img.get_width()-img.get_width(), y) )

            #hit forrest
            if mouseclick:
                #hitforrest.append(  )
                #print i, img.get_at( ( forrest_draw_pos1[0]+pygame.mouse.get_pos()[0], forrest_draw_pos1[1]+pygame.mouse.get_pos()[1]) )
                #print i, img.get_at( ( forrest_draw_pos2[0]+pygame.mouse.get_pos()[0], forrest_draw_pos2[1]+pygame.mouse.get_pos()[1]) )
                
                #print "==", img.get_width()+ forrest_draw_pos1[0]+pygame.mouse.get_pos()[0], "x", img.get_width()+ forrest_draw_pos2[0]+pygame.mouse.get_pos()[0], "=="
                
                #print -forrest_draw_pos1[0]+pygame.mouse.get_pos()[0], -forrest_draw_pos2[0]+pygame.mouse.get_pos()[0]
                
                if -forrest_draw_pos1[0]+pygame.mouse.get_pos()[0] >= 0 and -forrest_draw_pos1[0]+pygame.mouse.get_pos()[0] < img.get_size()[0]:
                    #print i, img.get_at( ( -forrest_draw_pos1[0]+pygame.mouse.get_pos()[0], forrest_draw_pos1[1]+pygame.mouse.get_pos()[1]) )
                    hitforrest.append( img.get_at( ( -forrest_draw_pos1[0]+pygame.mouse.get_pos()[0], forrest_draw_pos1[1]+pygame.mouse.get_pos()[1]) ) )
                else:
                    #print i, img.get_at( ( -forrest_draw_pos2[0]+pygame.mouse.get_pos()[0], forrest_draw_pos2[1]+pygame.mouse.get_pos()[1]) )
                    hitforrest.append( img.get_at( ( -forrest_draw_pos2[0]+pygame.mouse.get_pos()[0], forrest_draw_pos2[1]+pygame.mouse.get_pos()[1]) ) )
                
                #if forrest_draw_pos1[0]+pygame.mouse.get_pos()[0] > img.get_size()[0]:
                #    print i, img.get_at( ( forrest_draw_pos2[0]+pygame.mouse.get_pos()[0], forrest_draw_pos2[1]+pygame.mouse.get_pos()[1]) )
                #else:
                #    print i, img.get_at( ( forrest_draw_pos1[0]+pygame.mouse.get_pos()[0], forrest_draw_pos1[1]+pygame.mouse.get_pos()[1]) )
                
                    
            #drops
            for one in drops[i][:]:
                one.move()
                # check of screen limits
                if one.position[1] > screen_y+one.image.get_size()[1]:
                    drops[i].remove(one)
                else:
                    one.draw(screen, (x//(i+2)))
            
            #shadow
            screen.blit(shadow, (0,0))

            #player
            if i == deep:
                player_img_toshow = toshow(player_img, deep)

                #screen.blit( player_img_toshow, (screen_x//2 - player_img_toshow.get_size()[0]//2, screen_y -player_img_toshow.get_size()[1] -35*(deep-1)) )

            #animals
            for one in animals[i][:]:

                #shooting
                if mouseclick:
                    #print pygame.mouse.get_pos(), ((x//(i+2))+one.position[0],one.position[1])
                    #print one.image.get_size()
                    if pygame.mouse.get_pos()[0] > (x//(i+2))+one.position[0] and pygame.mouse.get_pos()[0] < (x//(i+2))+one.position[0]+one.image.get_size()[0]: #x
                        if pygame.mouse.get_pos()[1] > one.position[1] and pygame.mouse.get_pos()[1] < one.position[1]+one.image.get_size()[1]: #y
                            #checking pixels for hit
                            #print pygame.mouse.get_pos()[0]-((x//(i+2))+one.position[0]), pygame.mouse.get_pos()[1]-one.position[1]
                            hitpixel = one.image.get_at( (int(pygame.mouse.get_pos()[0]-((x//(i+2))+one.position[0])), pygame.mouse.get_pos()[1]-one.position[1]) )
                            #print hitpixel
                            if hitpixel != (0,0,0,0):
                                #checking for block in way
                                
                                ###screen.blit( img, ( (x//(i+2))%img.get_width(), y) )
                                ###screen.blit( img, ( (x//(i+2))%img.get_width()-img.get_width(), y) )
                                #for layer in bg[:i]:
                                #    #print i, layer.get_at( pygame.mouse.get_pos() )
                                #    print i, layer.get_at( ((x//(i+2))%layer.get_width() +pygame.mouse.get_pos()[0], y +pygame.mouse.get_pos()[1]) ), layer.get_at( ((x//(i+2))%layer.get_width()-img.get_width() +pygame.mouse.get_pos()[0], y +pygame.mouse.get_pos()[1]) )
                                #print "================="
                                #for pixel in hitforrest:
                                    
                                #print "HIT"
                                #animals[i].remove(one)
                                adept_to_die = one
                                hitforrest = []
                                
                one.move()
                # check of screen limits
                #print one.position[0], (-(x//(i+2))+screen_x//2 - player_img_toshow.get_size()[0]//2)
                #print one.position[0]- (-(x//(i+2))+screen_x//2 - player_img_toshow.get_size()[0]//2)
                if abs(one.position[0]- (-(x//(i+2))+screen_x//2 - player_img_toshow.get_size()[0]//2)) > 2*screen_x+one.image.get_size()[0]:
                    animals[i].remove(one)
                else:
                    one.draw(screen, (x//(i+2)))
        
        #killing
        if adept_to_die != None:
            #print len(hitforrest)
            kill = True
            for pixel in hitforrest:
                if pixel != (0,0,0,0):
                    kill = False
            
            if kill:
                animals[len(hitforrest)].remove(adept_to_die)

        #drawing cursor
        screen.blit(cursor_img, (pygame.mouse.get_pos()[0]-cursor_img.get_size()[0]//2, pygame.mouse.get_pos()[1]-cursor_img.get_size()[1]//2))

        #adding drops
        if counter%5 == 0:
            roll = random.randrange(0,len(drops))
            drop_img_toshow = toshow(drop_img, roll)

            drops[ roll ].append(Drop([-(x//(roll+2))+ random.randrange(drop_img.get_size()[0], screen_x-drop_img.get_size()[0]), -drop_img.get_size()[1]], [random.randrange(-1,2), 0.5*random.randrange(1, 1+len(drops)-roll) ], drop_img_toshow))

        #adding animals
        #if counter%100000 == 1:
        if counter%400 == 0:
            roll = random.randrange(1,len(animals))
            #animal_img_toshow = toshow(pygame.image.load("img/animals/fox.png").convert_alpha(), roll)
            animal_img_toshow = toshow( animals_images[ random.randrange(0, len(animals_images)) ], roll )
            roll2 = random.randrange(0, 2)
            animals[roll].append(Animal( [screen_x//2 - player_img_toshow.get_size()[0]//2-(x//(roll+2)) + (roll2*-2+1)*(animal_img_toshow.get_size()[0]//2+screen_x), screen_y -animal_img_toshow.get_size()[1] -35*(roll-1)], roll2, random.randrange(2,7)/10., animal_img_toshow ))
        
        pygame.display.flip()
        
        mouseclick = False
        
        timer.tick(100)
        if counter%100 == 0:
            #print "fps", int(timer.get_fps())
            if counter > 10000:
                counter = 0

main()