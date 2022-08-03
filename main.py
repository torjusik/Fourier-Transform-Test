from math import cos, pi, sin
from random import randrange
import numpy
import pygame as pg
from pygame.constants import FULLSCREEN
from vector import Vector
class Game():
    def __init__(self):
        pg.init()
        pg.font.init()
        self.width, self.height = 1920, 1080
        self.resized_screen=pg.display.set_mode((0, 0), FULLSCREEN)
        self.screen = pg.Surface((self.width, self.height))
        pg.display.set_caption("Game!")
        self.fpsClock = pg.time.Clock()
        self.fps = 144
        self.dt = 1/self.fps
        self.pause_toggle = False
        self.slider_variable = 0
        vectorlist = [[100, 0], [50, 0], [25, 0]]
        self.vectorcount = 5
        self.vectorspeedlist = [1, -1, 1]
        self.vector = Vector((50, 50))
        self.base_vector = self.vector
        for i in range(self.vectorcount):
            self.vector = Vector((200 / (i+1), 0), parentVector=self.vector)
        self.rotate_pressed = False
        self.dot_list = []
    
    def quit(self):
        pg.quit()
        exit(0)

    
    def run(self):
        while True:
            self.update()
            if not self.pause_toggle:
                self.draw()
            self.dt = self.fpsClock.tick(self.fps)
    
    def update(self):
        self.keys = pg.key.get_pressed()
        if not self.keys[pg.K_r]:
            self.rotate_pressed = False
        for event in pg.event.get():
            if event.type == pg.quit:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_r and not self.rotate_pressed:
                    self.vector.rotate(pi)
                    self.rotate_pressed = True
                if event.key == pg.K_SPACE:
                    self.pause_toggle = not self.pause_toggle
                    
        if not self.pause_toggle:
            self.base_vector.set_rad(self.slider_variable/100*2*pi)
            curr_vector = self.vector
            i = 0
            while type(curr_vector.parentVector) != numpy.ndarray:
                curr_vector.set_rad(curr_vector.radian + self.dt/1000*2*pi)
                curr_vector.update()
                curr_vector = curr_vector.parentVector
                i += 1

    def draw(self):
        self.screen.fill((10, 10, 10))
        self.slider_variable = self.draw_slider((500, 50), (self.width/1.5, self.height/1.3), self.slider_variable, "Radians: ")
        self.vector.draw(self.screen)
        resized_screen = pg.transform.scale(self.screen, (self.width/1.5, self.height/1.5))
        self.resized_screen.blit(resized_screen, (0, 0))
        pg.display.flip()

    
    def draw_slider(self, size, position, progress, text, pointdiameter=20, colorpoint="blue", colorborder="White", colorprogress="Green", colorbackground="Black", bordersize=4):
        if pg.mouse.get_pressed()[0]:
            x, y = numpy.array(pg.mouse.get_pos())*1.5
            if self.check_point_in_rect((x,y), (position[0], position[1], size[0], size[1])):
                progress = (x - position[0]) / size[0] * 100
                if progress >= 100:
                        progress = 100
                elif progress <= 0:
                    progress = 0
            
        self.blit_text(text, (position[0] + 250, position[1] -30), size[1], self.screen, color=(255,255,255))
        progress_in_pixels = round((size[0] - bordersize*2)/100 * progress) + 0.01
        self.draw_progressbar(size, position, progress, colorborder=colorborder, colorprogress=colorprogress, colorbackground=colorbackground, bordersize=bordersize)
        pg.draw.circle(self.screen, (pg.Color(colorpoint)), (position[0] + progress_in_pixels, position[1] + size[1]/2), pointdiameter)
        return progress
    
    def draw_progressbar(self, size, position, progress, colorborder="White", colorprogress="Green", colorbackground="Black", bordersize=4):
        progress_in_pixels = round((size[0] - bordersize*2)/100 * progress)
        
        #border
        pg.draw.rect(self.screen, pg.Color(colorborder), (position[0], position[1], size[0], size[1]))
        
        #background
        pg.draw.rect(self.screen, pg.Color(colorbackground), (position[0] + progress_in_pixels + bordersize, position[1] + bordersize, size[0] - progress_in_pixels - bordersize*2, size[1] - bordersize*2))
        
        #progress
        pg.draw.rect(self.screen, pg.Color(colorprogress), (position[0] + bordersize, position[1] + bordersize, progress_in_pixels, size[1] - bordersize*2))

        #border corners
        pg.draw.rect(self.screen, pg.Color(colorborder), (position[0], position[1], bordersize*2, bordersize*2))
        pg.draw.rect(self.screen, pg.Color(colorborder), (position[0], position[1] + size[1] - bordersize*2, bordersize*2, bordersize*2))
        pg.draw.rect(self.screen, pg.Color(colorborder), (position[0] + size[0] - bordersize*2, position[1], bordersize*2, bordersize*2))
        pg.draw.rect(self.screen, pg.Color(colorborder), (position[0] + size[0] - bordersize*2, position[1] + size[1] -bordersize*2, bordersize, bordersize))
        return progress_in_pixels

    def check_point_in_rect(self, point, rect):
        if point[0] <= rect[0] + rect[2] and point[0] >= rect[0] and point[1] <= rect[1] + rect[3] and point[1] >= rect[1]:
            return True
        else:
            return False

    def blit_text(self, text, position, size, SurfaceToBlitTo, aa=True, font="comic sans", color=(0,0,0)):
        myFont = pg.font.SysFont(font, size)
        text_font = myFont.render(str(text), aa, (color))
        SurfaceToBlitTo.blit(text_font, text_font.get_rect(center=position))

if __name__ == '__main__':
    game = Game()
    game.run()
    