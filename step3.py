import pygame
pygame.init()

screen = pygame.display.set_mode((1280,720))
background = pygame.Surface(screen.get_size())
background.fill((255,255,255))
background = background.convert()
ballsurface = pygame.Surface((50,50))
pygame.draw.circle(ballsurface, (255,0,0), (25,25), 20)
ballsurface = ballsurface.convert()

mainloop = True
FPS = 30.0
playtime = 0.0
clock = pygame.time.Clock()
radius = 20


while mainloop :
    milliseconds = clock.tick(FPS)
    playtime += milliseconds / 1000.0

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            mainloop = False
        elif event.type == pygame.KEYDOWN :
            if event.key == pygame.K_ESCAPE :
                mainloop = False

    screen.blit(background, (0,0))
    screen.blit(ballsurface, (radius*(1+2*(playtime%20)), 25))

    text = "FPS: {0:.2f} Playtime: {1:.2f}".format(clock.get_fps(), playtime)
    pygame.display.set_caption(text)
    pygame.display.flip()

print("This game was played for {0:.2f} seconds".format(playtime))