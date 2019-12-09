import pygame
import random

class main() :
    def __init__(self, width = 1280, height = 720, fps = 60) :
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((255,255,255))
        self.background = self.background.convert()
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.playtime = 0.0
        self.balls = []

    def run(self) :
        mainloop = True
        while mainloop :
            milliseconds = self.clock.tick(self.fps)
            self.playtime += milliseconds/1000.0

            #escape
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    mainloop = False
                elif event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_ESCAPE :
                        mainloop = False 
             ########
                    if event.key == pygame.K_SPACE :
                        self.balls.append(Ball(self.width,self.height))

            self.screen.blit(self.background, (0,0))
            for ball in self.balls :
                ball.blit(self.screen, milliseconds)
            caption = "FPS: {0:.2f}, Playtime: {1:.2f}, Balls: {2}".format(self.clock.get_fps(), self.playtime, len(self.balls))
            pygame.display.set_caption(caption)
            pygame.display.flip()
        print("This game was played for {0:.2f} seconds".format(self.playtime))



class Ball() :
    def __init__ (self, scr_width, scr_height) :
        self.radius = random.randint(0, min(scr_width, scr_height)//2)
        self.xpos = random.randint(0, scr_width - 2*self.radius)
        self.ypos = random.randint(0, scr_height - 2*self.radius)
        self.scr_width = scr_width
        self.scr_height = scr_height
        self.ballsurface = pygame.Surface((2*self.radius, 2*self.radius))
        self.ballsurface.set_colorkey((0,0,0))
        pygame.draw.circle(self.ballsurface,(random.randint(1,255),random.randint(1,255),random.randint(1,255)),(self.radius,self.radius), self.radius)
        self.ballsurface.convert_alpha()
        self.dx = random.uniform(-(scr_width - 2*self.radius)/1000.0, (scr_width - 2*self.radius)/1000.0)
        self.dy = random.uniform(-(scr_height - 2*self.radius)/1000.0, (scr_height - 2*self.radius)/1000.0)

    def blit (self, target, milliseconds) :
        """
        target : Surface to blit on
        milliseconds : tick
        """
        if self.xpos + self.dx*milliseconds > self.scr_width - 2*self.radius :
            self.xpos = 2*self.scr_width - self.xpos - self.dx*milliseconds -4*self.radius
            self.dx *= -1
        elif self.xpos + self.dx*milliseconds < 0 :
            self.xpos = -(self.xpos + self.dx*milliseconds)
            self.dx *= -1
        else :
            self.xpos += self.dx * milliseconds

        if self.ypos + self.dy*milliseconds > self.scr_height - 2*self.radius :
            self.ypos = 2*self.scr_height - self.ypos - self.dy*milliseconds - 4*self.radius
            self.dy *= -1
        elif self.ypos + self.dy*milliseconds < 0 :
            self.ypos = -(self.ypos + self.dy*milliseconds)
            self.dy *= -1
        else :
            self.ypos += self.dy * milliseconds

        target.blit(self.ballsurface, (self.xpos, self.ypos))

if __name__ == '__main__' :
    main(1280,720,60).run()