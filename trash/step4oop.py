import pygame
import os

class main() :
    def __init__(self, width = 1280, height = 720, fps = 30):
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
        self.man = man(self.width, self.height)

    def run(self) :
        mainloop = True
        self.screen.blit(self.background, (0,0))
        self.man.blit(self.screen, pygame.key.get_pressed())

        while mainloop : 
            
            milliseconds = self.clock.tick(self.fps)
            self.playtime += milliseconds / 1000.0

            #escape
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    mainloop = False
                elif event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_ESCAPE :
                        mainloop = False 
             ########
            self.screen.blit(self.background, (0,0))
            self.man.blit(self.screen, pygame.key.get_pressed())

            caption = "FPS: {0:.2f}, Playtime: {1:.2f}".format(self.clock.get_fps(), self.playtime)
            
            pygame.display.set_caption(caption)
            pygame.display.flip()
        print("This game was played for {0:.2f} seconds".format(self.playtime))

class man() :
    def __init__(self, scr_width, scr_height) :
        """
        scr_width : screen width
        scr_height : screen height (in pixels)
        """
        self.img = pygame.image.load(os.path.join("image","man.png")).convert_alpha()
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.scr_width = scr_width
        self.scr_height = scr_height
        self.xpos = self.scr_width // 2 - self.width // 2
        self.ypos = self.scr_height // 2 - self.height // 2
        
    def blit(self, target, pressed_key) :
        """
        target : Surface
        pressed : pygame.key.get_pressed()
        """
        
        if pressed_key[pygame.K_UP] :
            self.ypos -= 10 if self.ypos > 10 else self.ypos
        if pressed_key[pygame.K_DOWN] :
            self.ypos += 10 if self.ypos + self.height + 10 < self.scr_height else (self.scr_height - self.ypos - self.height)
        if pressed_key[pygame.K_LEFT] :
            self.xpos -= 10 if self.xpos > 10 else self.xpos
        if pressed_key[pygame.K_RIGHT] :
            self.xpos += 10 if self.xpos + self.width +10 < self.scr_width else (self.scr_width - self.xpos - self.width)

        target.blit(self.img,(self.xpos, self.ypos))

if __name__ == '__main__' :
    main(1280,720,60).run()