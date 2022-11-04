# std lib
from math import sin, cos

# pip install
import pygame as pg

# local
from settings import *

class RayCasting:
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen
        self.world_map = self.game.map.world_map

    def ray_cast(self):
        # see '_tutorial/raycasting-overview.jpg'
        px, py = self.game.player.pos   # player.x + dx, player.y + dy e.g. (3.33, 0.22)
        map_x, map_y = self.game.player.map_pos     # int(player.x), int(player.y) e.g. (3, 0)

        # see 'raycasting-angle.jpg'
        ray_angle = self.game.player.angle - HALF_FOV + 0.0001  # avoid div by zero

        for ray in range(NUM_RAYS):
            cos_a = cos(ray_angle)
            sin_a = sin(ray_angle)

            #
            # VERTICALS - see 'raycasting-coords-X.jpg'
            #
            # see 'raycasting-coords-E.jpg' and 'raycasting-coords-W.jpg'
            x_vert, dx = (map_x + 1, 1) if cos_a > 0 else (map_x - 1e-6, -1)

            # see 'raycasting-vertical.jpg and 'raycasting-depth-vert.jpg'
            # we know x_vert so we can calc depth_vert and solve for y_vert
            depth_vert = (x_vert - px) / cos_a
            y_vert = (depth_vert * sin_a) + py

            # see 'raycasting-depth-delta-dy.jpg'
            # we know dx and cos(a) so we can calc delta_depth and solve for dy
            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            # now we have everything we need to cast a ray and find intersections with verticals
            for i in range(MAX_DEPTH):
                # now we can check if the tile of the vertical intersection is a wall:
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.world_map:
                    break  # we've reached an obstacle

                # if not we cast the ray to the next intersection
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            #
            # HORIZONTALS - repeat; see 'raycasting-horizontal.jpg'
            #
            y_hor, dy = (map_y + 1, 1) if sin_a > 0 else (map_y - 1e-6, -1)

            # see 'raycasting-depth-horiz.jpg' and comments for VERTICALS
            depth_hor = (y_hor - py) / sin_a
            x_hor = (depth_hor * cos_a) + px

            # see 'raycasting-depth-delta-dx.jpg'
            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for i in range(MAX_DEPTH):
                # check if the tile of the horizontal interesction is a wall
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.world_map:
                    break   # reached an obstacles

                # extend ray to next horizontal intersection
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            #
            # DEPTH 
            #
            # we want to use the closer intersection - see 'raycasting-depths-vert-hor.jpg'
            depth = min(depth_vert, depth_hor)

            # debug draw
            start_xy = (TILEPX * px, TILEPX * py)
            end_x = TILEPX * px + TILEPX * depth * cos_a
            end_y = TILEPX * py + TILEPX * depth * sin_a
            pg.draw.line(self.screen, 'yellow', start_xy, (end_x, end_y), 2)

            # FINALLY, adding DELTA_ANGLE gives us the angle for the next ray, ready for next loop iter
            ray_angle += DELTA_ANGLE



    def update(self):
        self.ray_cast()