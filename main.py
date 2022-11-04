# std lib
import sys

# 3rd party
import pygame as pg

# local
from settings import *
from map import *
from player import *


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1 # track the time between frames for consistency adjustment
        self.new_game()


    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)

    def update(self):

        # update game objects
        self.player.update()

        # update regions of the display which have changed since last call
        pg.display.flip()

        # returns the time since last frame, ticks the frame consistent with 60 FPS
        self.delta_time = self.clock.tick(FPS)

        # display the framerate as the window caption
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.screen.fill('black')
        self.map.draw()
        self.player.draw()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()