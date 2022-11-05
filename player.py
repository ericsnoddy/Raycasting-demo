# std lib
import math

# 3rd party
import pygame as pg
from pygame.locals import *

# local
from settings import *


class Player:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.fired = False

    
    def single_fire_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1 and not self.fired and not self.game.weapon.reloading:
                self.game.sound.shotgun.play()
                self.fired = True
                self.game.weapon.reloading = True


    def movement(self):
        # see '_tutorial/player-movement.jpg' and 'direction_vector_math.jpg'
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0   # initialize

        # we want player movement speed independent of frame rate, so we introduce delta_time
        # this is the time between frames which we'll use to error-correct inconsistent framerates.
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()

        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin

        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin

        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos

        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos

        # apply the speed differentials only if wall does not block player movement
        self.check_wall_collision(dx, dy)

        # if keys[pg.K_LEFT]:
        #     self.angle -= PLAYER_ROT_SPEED * self.game.delta_time

        # if keys[pg.K_RIGHT]:
        #     self.angle += PLAYER_ROT_SPEED * self.game.delta_time

        self.angle %= math.tau  # keeps the angle within 2pi (tau = 2 * pi)


    def check_wall(self, x, y):
        # on the world_map, obstacles return True and open space returns False, as designed
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):

        # dx, dy depend on delta_time; player size should not so we divide it out
        # scaling dx, dy provides illusion of player size
        scale = PLAYER_SIZE_SCALE / self.game.delta_time

        # disallow movement (dx, dy) if such movement puts player in wall
        # scaling dx, dy is how we keep player from getting too close too walls which stretches the texture into pixels 
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy
        

    def draw(self):
        # pg.draw.line(self.screen, 'yellow', (self.x * TILEPX, self.y * TILEPX),
        #                 (self.x * TILEPX + WIDTH * math.cos(self.angle),
        #                     self.y * TILEPX + WIDTH * math.sin(self.angle)), 2)
        pg.draw.circle(self.screen, 'green', (self.x * TILEPX, self.y * TILEPX), 15)
    
    def mouse_control(self):
        mx, my = pg.mouse.get_pos()

        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        # get relative x-coord mouse movement since previous frame
        self.rel_x = pg.mouse.get_rel()[0]
        # clamp this value between -MOUSE_MAX_REL and MOUSE_MAX_REL
        self.rel_x = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel_x))
        # adjust player angle taking into account mouse sensitivity and delta time.
        # multiplying by delta_time is the reason for the small numbers in mouse settings
        self.angle += self.rel_x * MOUSE_SENSITIVITY * self.game.delta_time

        
    def update(self):
        self.movement()
        self.mouse_control()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    