# std lib
from math import sin, cos

# pip install
import pygame as pg

# local
from settings import *

class RayCasting:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.world_map = game.map.world_map

        self.ray_casting_results = []
        self.objects_to_render = []
        self.textures_dict = game.object_renderer.wall_textures_dict

    # Call this method from the update() method
    def get_objects_to_render(self):
        self.objects_to_render = []

        # generate a ray number 0+ and extract raycasting values to associate with the ray
        for ray, values in enumerate(self.ray_casting_results):
            depth, proj_height, texture_num, offset = values

            # x-pos and width do not need rescaling 
            # offset will be 0, 1, or decimal in (0,1) - see 'render-slice.jpg'
            x, w = offset * (TEXTURE_SIZE - SCALE), SCALE

            # As the depth of the ray approaches 0 (texture up close) the proj_height gets very large
            # this kills performance so we correct this by limiting the proj_height to the size of the display screen
            if proj_height < HEIGHT:
                
                # no height rescaling
                y, h = 0, TEXTURE_SIZE
                wall_slice = self.textures_dict[texture_num].subsurface(x, y, w, h)

                # scale to the width (SCALE) and projection height of the ray-rectangle
                wall_slice = pg.transform.scale(wall_slice, (SCALE, proj_height))

                # calc pos from ray number (x) and center texture on y-axis (ie, player POV stays on the same centered horizontal plane)
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)

            else:
                # height rescaling using screen-projection ratio - see 'render-proj_height.jpg'
                h = TEXTURE_SIZE * HEIGHT / proj_height
                y = HALF_TEXTURE_SIZE - h // 2
                wall_slice = self.textures_dict[texture_num].subsurface(x, y, w, h)

                # now the projected height will not exceed the screen height
                wall_slice = pg.transform.scale(wall_slice, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            # now we have an object with attributes to render: add it to the list
            self.objects_to_render.append((depth, wall_slice, wall_pos))


    def ray_cast(self):

        # clear the ray casting results list before doing anything
        self.ray_casting_results = []

        # see '_tutorial/raycasting-overview.jpg'
        px, py = self.game.player.pos   # player.x + dx, player.y + dy e.g. (3.33, 0.22)
        map_x, map_y = self.game.player.map_pos     # int(player.x), int(player.y) e.g. (3, 0)

        # init/reset variables to avoid error
        texture_num_vert, texture_num_hor = 1, 1

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
                    # get texture number from world_map grid, later used to retrieve texture from Dict
                    texture_num_vert = self.world_map[tile_vert]
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
                    # get texture number from world_map grid, later used to retrieve texture from Dict
                    texture_num_hor = self.world_map[tile_hor]
                    break   # reached an obstacle

                # extend ray to next horizontal intersection
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            #
            # DEPTH and TEXTURE OFFSET
            #
            # we want to use the closer intersection - see 'raycasting-depths-vert-hor.jpg'
            # Since we're (usually) projecting into the middle of a texture we need offset to find texture vertices (grid pts)
            # for offsets see handwritten notes + four 'render-approach-X.jpg' imgs
            if depth_vert < depth_hor:
                depth, texture_num = depth_vert, texture_num_vert
                # x % 1 returns x if x in (0,1) else returns 0 (x <= 0 or x >= 1)
                # This clever function for offset equates to 0 when we're on one of the endpoints
                # but equates to (1 - the coord) when it's between endpts, so we know how much to add to the rectangle's origin (0,0)
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth, texture_num = depth_hor, texture_num_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            # That step will leave us with a fish-eye lens effect due to combining polar and Cartesian coords
            # Especially noticeable up close, we have to scale the depth to correct for distance between the
            # arc of the projection and tangent of the arc (flat plane of the screen)
            # That is, we project an arc onto a line by scaling the hypotenuse (depth) at even intervals.
            # Comment out the following line of code to test the undesired effect:
            depth *= cos(self.game.player.angle - ray_angle)
            '''
            More complete but harder to grasp explanation from YT user 'Arnon Marcus':
            "...the choise of using angle deltas to compute ray directions: In a rectilinear projection as the one used here, 
            that choice makes the rays hitting the projection plane distributed along it non-uniformly, where they get more 
            spread-out around the center and more clumped together closer to the right and left edges of the screen (where 
            this second fish-eye lense effect becomes noticeable). The full fix for that is to instead step along the 
            projection plane itself (in this case, a projection-line, as it's 2D ray-casting), at a constant step 
            corresponding to a fixed width of the columns. Then, the ray direction are the vectors from the player's 
            position to those points on the projection-line - but normalized. This ensures the distribution of the rays is 
            uniform across the screen, removing that fish-eye lens effect.
            '''

            #
            # PROJECTION
            #
            # see 'raycasting-projection-sideview.jpg' and 'raycasting-projection-topdown.jpg'
            proj_height = SCREEN_DIST / (depth + 0.0001)  # avoid div by zero


####################################
            # DRAW WALLS  -  see 'raycasting-delta-rect.jpg'
            # we use SCALE factor (settings.py) so we dont consider rays beyond screen RES (performance)
            # This amounts to distributing rays and hence the rectangles at 2px widths across the screen
            # this is all we need to convert our 2D raycast plane into 3 dimensions (turn off map.draw() and player.draw())
            # Also, a REALLY COOL FUNCTION for changing color based on a power of the depth variable, great illusion

            # No longer necessary once we apply textures, but can be re-implemented if rendering is removed
            # Saving it here for future coding use:

            # color = [255 / (1 + depth ** 5 * 0.00002)] * 3
            # pg.draw.rect(self.screen, color, (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))

            # DEBUG DRAW
            # This is for a topdown view of all rays being cast, must un-comment code to draw map and player, turn off renderer:

            # start_xy = (TILEPX * px, TILEPX * py)
            # end_x = TILEPX * px + TILEPX * depth * cos_a
            # end_y = TILEPX * py + TILEPX * depth * sin_a
            # pg.draw.line(self.screen, 'yellow', start_xy, (end_x, end_y), 2)

####################################

            #
            # RAY CASTING RESULTS
            #
            self.ray_casting_results.append((depth, proj_height, texture_num, offset))

            # FINALLY, adding DELTA_ANGLE gives us the angle for the next ray, ready for next loop iter
            ray_angle += DELTA_ANGLE


    def update(self):
        self.ray_cast()
        self.get_objects_to_render()