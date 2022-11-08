# std lib
import sys

# 3rd party
import pygame as pg

# local
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *

class Game:
    def __init__(self):
        # toggle 2-D topdown mode with command line arg -2d or by setting self.topdown = True
        self.topdown = False
        self.topdown = True if '-2d' in sys.argv else self.topdown

        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1 # track the time between frames for consistency adjustment

        # repeating global trigger for timing events; when triggered it adds the custom flag to the event queue
        self.global_trigger = False
        self.global_event = pg.USEREVENT+0  # see check_events() for event handling
        pg.time.set_timer(self.global_event, TIMER_MS)

        self.new_game()


    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        # call renderer before raycaster so raycaster has access to loaded textures
        self.object_renderer = ObjectRenderer(self)
        self.ray_casting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)


    def update(self):

        # update game objects
        self.player.update()
        self.ray_casting.update()
        self.object_handler.update()
        self.weapon.update()

        # update regions of the display which have changed since last call
        pg.display.flip()

        # returns the time since last frame + ticks frames consistent with 60 FPS (or less)
        self.delta_time = self.clock.tick(FPS)

        # display the framerate as the window caption
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')


    def draw(self):
        if self.topdown:
            self.screen.fill('black')
            self.map.draw()
            self.player.draw()
        else:
            self.object_renderer.draw()
            self.weapon.draw()


    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            
            # flags True every TIMER_MS ms
            elif event.type == self.global_event:
                self.global_trigger = True

            # trace fire events
            self.player.single_fire_event(event)


    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()