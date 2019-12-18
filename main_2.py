import pygame
import os
import random
import math
import cells_2 as cell
import functions_2 as tool
import particles_2 as particle
import eukaryote_2 as eukaryote
import virus_2 as virus
import grampos_2 as gramp
import time
import sys


class Main() :
    def __init__ (self, width = 1600, height = 900, fps = 60, render = False, rendertime = 0) :
        pygame.init()
        self.render_mode = render
        self.render_frame = rendertime * 60 * fps
        self.width = width
        self.height = height
        self.fps = fps
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        self.background.fill((255,255,255))
        self.background = self.background.convert()
        self.clock = pygame.time.Clock()
        self.playtime = 0.0
        self.rect = self.screen.get_rect()
        self.allgroup = pygame.sprite.LayeredDirty()
        self.ingroup = pygame.sprite.Group()
        self.boundaries = {}
        self.boundaries[tool.Boundary(self.rect)] = self.allgroup
        self.frame = 0 #frame counter 0~fps-1
        self.glucose_spawn = 90
        self.glucose_max = 600
        self.skin_layer = 5
        self.skin_start = 50
        self.screenshot_count = 0
        tool.totalgrid.initialize(self.width,self.height)
        self.groupsetter()   

    def groupsetter(self) :
        cell.Cell.groups = self.allgroup
        eukaryote.HumanCell.groups = self.allgroup, self.ingroup
        particle.Particle.groups = self.allgroup
        particle.ApoptoticBody.groups = self.allgroup, self.ingroup
        particle.NecroticBody.groups = self.allgroup, self.ingroup
        particle.Cytokine.groups = self.allgroup, self.ingroup

    def run(self) :
        mainloop = True
        self.screen.blit(self.background, (0,0))     
        self.set_skin()
        #self.one = eukaryote.Macrophage(tool.rand_point(self.vessel),tool.rand_2D())
        tool.filler(eukaryote.Epithelium,[(0,0)],0,self.skin_area, [self.ingroup])
        if self.render_mode :
            self.saver = tool.Saver('1.json')
            self.saver.clear_savefile()
        while mainloop :
            milliseconds = self.clock.tick(self.fps)
            self.playtime += milliseconds / 1000.0
            self.frame += 1
            if self.frame >= self.fps :
                self.frame = 0

            ##escape
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    mainloop = False
                elif event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_ESCAPE :
                            mainloop = False 
                            break
            ####################################################
                    x, y = pygame.mouse.get_pos()
                    #if event.key == pygame.K_r :
                    #    self.one.replicate_now = True
                    if event.key == pygame.K_t :
                        eukaryote.CD8Tcell((x,y), tool.rand_2D(1))
                    elif event.key == pygame.K_m :
                        eukaryote.Macrophage((x,y), tool.rand_2D(1))
                    elif event.key == pygame.K_b :
                        gramp.Aureus((x,y), tool.rand_2D(1))
                    elif event.key == pygame.K_e :
                        eukaryote.Epithelium((x,y), (1,1))
                    elif event.key == pygame.K_v :
                        virus.Epi_virus((x,y), (1,1))
                    elif event.key == pygame.K_s :
                        self.take_screenshot()
                    elif event.key == pygame.K_q :
                        if self.render_mode :
                            self.saver.saverapid()
                        mainloop = False

                elif event.type == pygame.MOUSEBUTTONDOWN :
                    x, y = pygame.mouse.get_pos()
                    #virus.HIV((x,y),tool.rand_2D(1))
                    #particle.Chemokine((x,y), tool.rand_2D(), random.randint(1,3))
                    #particle.NecroticBody((x,y),tool.rand_2D(0.1))
                    for cll in eukaryote.Epithelium.epithelium_list :
                        if cll.rect.collidepoint(x,y) :
                            cll.necrosis()

            if len(particle.Glucose.glucose_list) < self.glucose_max :
                self.glucose_creator(self.glucose_spawn,self.vessel)
            self.update()
            if self.render_mode :
                self.saver.append(self.allgroup)
                self.screenshot_count += 1
                if sys.getsizeof(self.saver.sequel) > 70000 :
                    self.saver.saverapid()
                if self.screenshot_count > self.render_frame :
                    self.saver.saverapid()
                    mainloop = False

            
    def glucose_creator (self, num : int, rect : pygame.Rect) :
        """
        num of glucose per second(frame-based), random place in the rect
        glucose will not move
        """
        if num < 0 :
            raise UserWarning('negative number passed to glucose_creator')
        if num == 0 :
            return
        elif self.fps < num :
            inte = int(num%self.fps)
            left = num - self.fps * inte
            for _ in range(inte) :
                x = random.randint(int(rect.left + particle.Glucose.rect.width/2), int(rect.right - particle.Glucose.rect.width/2))
                y = random.randint(int(rect.top + particle.Glucose.rect.height/2), int(rect.bottom - particle.Glucose.rect.height/2))
                particle.Glucose((x,y),tool.rand_2D(1,1)).add(self.ingroup)
            if left != 0 and self.frame % (self.fps / left) < 1:
                x = random.randint(int(rect.left + particle.Glucose.rect.width/2), int(rect.right - particle.Glucose.rect.width/2))
                y = random.randint(int(rect.top + particle.Glucose.rect.height/2), int(rect.bottom - particle.Glucose.rect.height/2))
                particle.Glucose((x,y),tool.rand_2D(1,1)).add(self.ingroup)

        elif self.frame % (self.fps / num) < 1:
            x = random.randint(int(rect.left + particle.Glucose.rect.width/2), int(rect.right - particle.Glucose.rect.width/2))
            y = random.randint(int(rect.top + particle.Glucose.rect.height/2), int(rect.bottom - particle.Glucose.rect.height/2))
            particle.Glucose((x,y),tool.rand_2D(1,1)).add(self.ingroup)

    def set_skin(self) :
        self.skin_thick = eukaryote.Epithelium.rect.height * self.skin_layer
        self.skin_area = pygame.Rect(0,self.skin_start,self.rect.width,self.skin_thick)
        self.inside = pygame.Rect(0,self.skin_start, self.rect.width, self.rect.height - self.skin_start)
        self.boundaries[tool.Boundary(self.inside)] = self.ingroup
        self.vessel = pygame.Rect(0,self.skin_area.bottom,self.rect.width, self.inside.height - self.skin_thick)

    def take_screenshot (self) :
        pygame.image.save(self.screen, 'screenshot\{0}.jpeg'.format(self.screenshot_count))
        self.screenshot_count +=1

    def update (self) :
        """
        update - clear - draw steps
        """
        t = time.time()
        for bndry, grp in self.boundaries.items() :
            bndry.bounce(grp)
        self.allgroup.update()
        uptime = time.time()-t
        self.allgroup.clear(self.screen, self.background)
        self.allgroup.draw(self.screen)
        drwtime = time.time()-t-uptime
        #pygame.display.set_caption('[FPS] : {0:.1f}, atp:{1}, glucose:{2}, nadh:{3}, pyruvate:{4}\
        #m.atp:{5}, m.pyru:{6}, m.nadh:{7}, m.intramem:{8}'.format(self.clock.get_fps(), self.one.atp, self.one.glucose, self.one.nadh, self.one.pyruvate\
        #    ,self.one.mitochondria.atp, self.one.mitochondria.pyruvate, self.one.mitochondria.nadh,self.one.mitochondria.intramem_h))
        if not self.render_mode :
            cap = '[FPS] : {0:.1f}, Total sprites: {1}, update : {2}, draw: {3}'.format(self.clock.get_fps(), len(self.allgroup), uptime, drwtime)
        else :
            cap = '[FPS] : {0:.1f}, Total sprites: {1}, update : {2}, draw: {3}, frame : {4}/{5}, save size : {6}'.format(self.clock.get_fps(), len(self.allgroup), uptime, drwtime, self.screenshot_count, self.render_frame, sys.getsizeof(self.saver.sequel),)
        pygame.display.set_caption(cap)
        tool.CRASHTIME=0.0
        pygame.display.flip()


if __name__ == '__main__' :
    Main(1000, 300, 60, True, 1).run()