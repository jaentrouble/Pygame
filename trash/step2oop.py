import pygame

class PygView :
    def __init__(self, width=640, height=400, fps=30) :
        pygame.init()
        pygame.display.set_caption("Press Esc to quit")
        self.width = width
        self.height = height
        self.fps = fps
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((255,255,0))
        self.background = self.background.convert()
        self.clock = pygame.time.Clock()
        self.playtime = 0.0
        self.font = pygame.font.SysFont('Bradley Hand ITC', 20, bold=True)

    def run(self) :
        running = True

        while running :
            milliseconds = self.clock.tick(self.fps)
            self.playtime += milliseconds / 1000.0

            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    running = False
                elif event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_ESCAPE :
                        running = False

            text = "FPS: {0:.2f} Playtime: {1:.2f}".format(self.clock.get_fps(), self.playtime)

            pygame.display.set_caption(text)
            self.screen.blit(self.background, (0,0))
            self.draw_text(text)
            pygame.display.flip()
            
        pygame.quit()
        print("This game was played for {0:.2f} seconds".format(self.playtime))

    def draw_text(self, text) :
        fw, fh = self.font.size(text)
        surface = self.font.render(text, False, (0,255,0))
        self.screen.blit(surface, ((self.width - fw) // 2, (self.height - fh) // 2))

if __name__ == "__main__":
        PygView(640,480).run()