# pip installl
import pygame as pg

# local
from settings import *

class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures_dict = self.load_wall_textures()

    def draw(self):
        self.render_game_objects()

    def render_game_objects(self):
        # list by (depth, wall_slice, wall_pos) of each texture subsurface
        list_objects = self.game.ray_casting.objects_to_render
        for _, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        # scale and return the image
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        # return a Dict in which the texture no. is key and texture itself is value
        return {
            1: self.get_texture('resources/textures/1.png'),
            2: self.get_texture('resources/textures/2.png'),
            3: self.get_texture('resources/textures/3.png'),
            4: self.get_texture('resources/textures/4.png'),
            5: self.get_texture('resources/textures/5.png'),
        }

