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
        self.blood_screen = self.get_texture('resources/textures/blood_screen.png', RES)
        self.digit_images = [self.get_texture(f'resources/textures/digits/{i}.png', DIGIT_RES) for i in range(11)]
        self.game_over_image = self.get_texture('resources/textures/game_over.png', RES)
        self.victory_image = self.get_texture('resources/textures/win.png', RES)

        # map generates an iterator after performing the given function on each item in an iterable
            # in this case, map turns each int in range(11) into a string and yields as in iterator
        # zip yields a list of tuples until input exhausted
            # in this case (str(int) for each value in self.digit_images)
        # dict converts the list of tuples into a dict of key:value pairs
        self.digits = dict(zip(map(str, range(11)), self.digit_images))


    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()


    def victory(self):
        self.screen.blit(self.victory_image, (0, 0))


    def game_over(self):
        self.screen.blit(self.game_over_image, (0,0))
        

    def draw_player_health(self):
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * DIGIT_RES[0], 0))
        self.screen.blit(self.digits['10'], ((i + 1) * DIGIT_RES[0], 0))   # '%' symbol


    def player_damage(self):
        self.screen.blit(self.blood_screen, (0,0))


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

