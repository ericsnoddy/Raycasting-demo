# pip installl
import pygame as pg

# local
from settings import *

class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures_dict = self.load_wall_textures()
        self.sky_image = self.get_texture('resources/textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0

    def draw(self):
        self.draw_background()
        self.render_game_objects()

    def draw_background(self):
        # sky
        # this is just a clever function for determining pos of sky based on rel mouse movement
        # it provides an illusion of background depth relative to the foreground
        # ...don't ask me. You can kind of see what's happening by commenting out individal blits
        self.sky_offset = (self.sky_offset + 4.0 * self.game.player.rel_x) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))

        # floor - just fill bottom half of screen with solid color
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        # list by (depth, wall_slice, wall_pos) of each texture subsurface
        # objs must be sorted by dist so closer walls are drawn after further entities, else see-thru walls
        # distance is the first value in the tuple
        list_objects = sorted(self.game.ray_casting.objects_to_render, key=lambda dist: dist[0], reverse=True)
        for _dist, image, pos in list_objects:
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

