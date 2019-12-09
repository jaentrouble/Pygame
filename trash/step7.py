import pygame
import os
import random

pygame.init()
folder = "image"

try :
    prettybackground = pygame.image.load(os.path.join(folder,"pretty.jpg"))
    uglybackground = pygame.image.load(os.path.join(folder,"ugly.jpg"))
    man = pygame.image.load(os.path.join(folder,"man.png"))
except :
    raise(UserWarning, "loading image failed")

screen = pygame.display.set_mode((1280,720))
screenrect = screen.get_rect()
prettybackground = prettybackground.convert()
uglybackground = uglybackground.convert()
background = uglybackground.copy()
man = man.convert_alpha()
manrect = man.get_rect()

x = 1
y = 1
dx, dy = 40, 40

screen.blit(uglybackground, (0,0))
screen.blit(man, (x, y))
clock = pygame.time.Clock()
mainloop = True
fps = 60
playtime = 0.0
painting = False
dirty = False

while mainloop :
    milliseconds = clock.tick(fps)
    seconds = milliseconds / 1000.0
    playtime += seconds

    #escape
    for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    mainloop = False
                elif event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_ESCAPE :
                        mainloop = False 
    ###############
                    elif event.key == pygame.K_r :
                        background = uglybackground.copy()
                        screen.blit(uglybackground, (0,0))
                    elif event.key == pygame.K_p :
                        painting = not painting
                    elif event.key == pygame.K_d :
                        dirty = not dirty

    caption = "FPS: {0:.2f}, Playtime: {1:.2f} ".format(clock.get_fps(), playtime)
    pygame.display.set_caption(caption)

    if not dirty :
        dirtyrect = background.subsurface((x, y, manrect.width, manrect.height))
        screen.blit(dirtyrect, (x,y))

    x += dx * seconds
    y += dy * seconds
    
    if x<0 :
        x = 0
        dx *= -1
        dx += random.randint(-15,15)
    elif x + manrect.width >= screenrect.width :
        x = screenrect.width - manrect.width
        dx *= -1
        dx += random.randint(-15,15)

    if y<0 :
        y = 0
        dy *= -1
        dy += random.randint(-15,15)
    elif y + manrect.height >= screenrect.height :
        y = screenrect.height - manrect.height
        dy *= -1
        dy += random.randint(-15,15)

    screen.blit(man, (x, y))

    tvscreen = prettybackground.subsurface((x, y, manrect.width, manrect.height))
    screen.blit(tvscreen, (0,0))

    if painting :
        background.blit(tvscreen, (x,y))

    pygame.display.flip()
