import pygame

class Step3 :
    def __init__ (self, width = 1280, height = 720, FPS = 30, radius = 25) :
        pygame.init()
        self.width = width
        self.height = height
        self.radius = radius
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((255,255,255))
        self.background = self.background.convert()
        self.FPS = FPS
        self.clock = pygame.time.Clock()
        self.playtime = 0.0
        self.ball = Ball(self.radius)
        self.xpos = 0
        self.ypos = 0
        self.xlen = 0
        self.ylen = 0

    def run(self) :
        mainloop = True
        
        while mainloop :
            milliseconds = self.clock.tick(self.FPS)
            self.playtime += milliseconds / 1000.0

            #escape
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    mainloop = False
                elif event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_ESCAPE :
                        mainloop = False 
            #####
            text = "FPS: {0:.2f} Playtime: {1:.2f} xpos: {2} ypos: {3} xlen: {4} ylen: {5}".format(self.clock.get_fps(), self.playtime, self.xpos, self.ypos, self.xlen, self.ylen)
            self.pastebackground()
            self.pasteball()
            pygame.display.set_caption(text)
            pygame.display.flip()

        print("This game was played for {0:.2f} seconds".format(self.playtime))


    def pastebackground(self) :
        self.screen.blit(self.background, (0,0))

    def pasteball(self) :
        seconds = int(10*self.playtime)
        xpos = self.radius
        ypos = self.radius
        xlen = int((self.width - 2*self.radius) // (2*self.radius))
        ylen = int((self.height - 2*self.radius) // (2*self.radius))
        if (seconds // xlen) % 2 == 0 :
            xpos = self.radius*(1 + 2*(seconds % xlen))
        else :
            xpos = self.radius*(2*(xlen - (seconds % xlen))-1)
        
        if ((seconds // xlen) // ylen) % 2 == 0 :
            ypos = self.radius*(1 + 2*((seconds //xlen) % ylen))
        else :
            ypos = self.radius*(2*(ylen - ((seconds // xlen) % ylen))-1)
        self.xpos = xpos
        self.ypos = ypos
        self.xlen = xlen
        self.ylen = ylen
        self.ball.blit(self.screen, (xpos,ypos))

class Ball():

    def __init__(self, radius : int) :
        self.radius = radius
        self.ballsurface = pygame.Surface((2*self.radius, 2*self.radius))
        pygame.draw.circle(self.ballsurface, (255,255,0), (self.radius,self.radius), self.radius)
        self.ballsurface = self.ballsurface.convert()

    def blit(self, target, pos) :
        """
        target : Surface
        pos : (xpos,ypos)
        
        """
        target.blit(self.ballsurface, pos)

if __name__ == '__main__' :
    Step3(1280, 720, 30, 40).run()