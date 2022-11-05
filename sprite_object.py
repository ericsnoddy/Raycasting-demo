# std lib
from math import cos, atan2, hypot, pi
from collections import deque
from os import listdir
from os.path import isfile, join

# pip install
import pygame as pg

# local
from settings import *

class Sprite:
    def __init__(self, game, path='resources/sprites/static_sprites/candelabra.png', 
                pos=(10.5, 3.5), scale=0.7, shift=0.37):
        self.game = game
        self.player = game.player
        
        self.x, self.y = pos
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift
        self.image = pg.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.IMAGE_WIDTH // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()

        # init to avoid errors
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.sprite_half_width = 0


    def update(self):
        self.get_sprite()


    def get_sprite_projection(self):

        # as in raycasting we calc height of projection...
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
        # ... but we must take initial image aspect ratio into account so we rescale
        proj_w, proj_h = proj * self.IMAGE_RATIO, proj
        image = pg.transform.scale(self.image, (proj_w, proj_h))

        # HALF_WIDTH math because sprite has width dimension but screen_x is its center
        self.sprite_half_width = proj_w // 2

        height_shift = proj_h * self.SPRITE_HEIGHT_SHIFT
        x_offset = self.screen_x - self.sprite_half_width
        y_offset = HALF_HEIGHT - proj_h // 2 + height_shift

        pos = x_offset, y_offset

        # append the variables we calc'd as tuple, which is all we need to render the sprite
        self.game.ray_casting.objects_to_render.append((self.norm_dist, image, pos))


    def get_sprite(self):
        # angle between player and sprite is theta = arctan[(sy - py)/(sx - px))
        # see 'player-sprite-delta_angle.jpg' and 'player-sprite-theta.jpg'
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy
        self.theta = atan2(dy, dx)  # atan2 ensures result is in correct quadrant [-pi, pi] over atan

        delta = self.theta - self.player.angle

        # due to signage in polar trig, if dx > 0 and player angle is > pi -OR- dx, dy both < 0, we have to add 2pi (tau)
        if (dx > 0 and self.player.angle > pi) or (dx < 0 and dy < 0):
            delta += 2 * pi

        # how many rays fit in that delta angle is how many rays from the edge of our FOV
        delta_rays = delta / DELTA_ANGLE

        # add delta_rays to the central ray and multiply by scale to get the x-pos of sprite on screen
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE

        # To calc size of projection for sprite, first calc distance; normalize to remove fish-lens effect
        self.dist = hypot(dx, dy)
        self.norm_dist = self.dist * cos(delta)

        # To maintain performance, we'll do certain things only while sprite is in view and not up close
        if -self.IMAGE_HALF_WIDTH < self.screen_x < (WIDTH + self.IMAGE_HALF_WIDTH) and self.norm_dist > 0.5:
            self.get_sprite_projection()



class AnimatedSprite(Sprite):
    def __init__(self, game, path=('resources/sprites/animated_sprites/green_light/0.png'),
                pos=(11.5, 3.5), scale=0.8, shift=0.27, animation_time=120):
        super().__init__(game, path, pos, scale, shift)
        self.animation_time = animation_time
        self.path = path.rsplit('/', 1)[0]  # isolate the folder-path
        self.images = self.get_images(self.path)
        self.animation_time_prev = pg.time.get_ticks()  # time since last frame
        self.animation_trigger = False


    def update(self):
        super().update()
        self.check_animation_time()
        self.animate(self.images)


    def animate(self, images):
        if self.animation_trigger:
            images.rotate(-1)  # deque list method
            self.image = images[0]  # now 0 is next item in the queue


    def check_animation_time(self):
        self.animation_trigger = False
        now = pg.time.get_ticks()
        if now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = now
            self.animation_trigger = True


    def get_images(self, path):
        # we use deque for convenient rotation method
        images = deque()
        for file_name in listdir(path):
            full_path = join(path, file_name)
            if isfile(full_path):
                img = pg.image.load(full_path).convert_alpha()
                images.append(img)
        return images
