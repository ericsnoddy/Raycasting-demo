# pip install
import pygame as pg

# local
from settings import *

class Sprite:
    def __init__(self, game, path='resources/sprites/candelabra.png', pos=(10.5, 3.5)):
        self.game = game
        self.player = game.player
        self.x, self.y = pos
        self.image = pg.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.IMAGE_WIDTH // 2

    def get_sprite(self):
        pass
