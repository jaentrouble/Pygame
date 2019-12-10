import pygame

pygame.init()
screen = pygame.display.set_mode((100,100))
bacnd = pygame.Surface((100,100))
bacnd.fill((255,255,255))
mainloop = True
bacnd.blit(screen,(0,0))
while mainloop :
    pygame.display.flip()
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            mainloop = False