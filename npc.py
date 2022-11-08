# std lib
from random import randint, random
from math import sin    # cos is included with sprite_object import

# local
from sprite_object import *

class NPC(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/npc/soldier/0.png', 
                pos=(10.5, 5.5), scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_images = self.get_images(self.path + '/attack')
        self.death_images = self.get_images(self.path + '/death')
        self.idle_images = self.get_images(self.path + '/idle')
        self.pain_images = self.get_images(self.path + '/pain')
        self.walk_images = self.get_images(self.path + '/walk')
        self.frame_counter = 0

        self.attack_dist = randint(3, 6)
        self.search_dist = randint(6, 9)
        self.speed = 0.03
        self.size = 10
        self.health = 100
        self.attack_damage = (7, 12)      # range, including end
        self.accuracy_percent = (10, 22)  # range, including end
        self.alive = True
        self.pain = False

        # We need to cast a single ray so we have a line of sight (npc logic; impenetrable walls)
        # will be just a general copy/paste of the raycasting method with some changes
        self.LOS = False
        self.npc_search_trigger = False

        
    def update(self):
        self.check_animation_time()
        self.get_sprite()
        self.run_logic()
        # self.debug_draw_ray_cast()

    
    def check_wall(self, x, y):
        # check_wall, check_wall_collision copied from player.py with some changes
        return (x, y) not in self.game.map.world_map


    def check_wall_collision(self, dx, dy):
        # disallow movement (dx, dy) if such movement puts npc in wall (accounting for npc's size)
        # 'size' instead of 'scale=size/delta_time' since npc doesn't depend on delta_time
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy


    def movement(self):
        # get the player's pos - retrieve the next step by call to pathfinder
        next_pos = self.game.pathfinding.get_path(self.map_pos, self.game.player.map_pos)
        next_x, next_y = next_pos

        # debug draw next pathfinding step to color it blue in 2-d topdown mode
        # pg.draw.rect(self.game.screen, 'blue', (TILEPX * next_x, TILEPX * next_y, TILEPX, TILEPX))

        # if next node(tile) in pathfinding path is occupied, do not move; wait for alternate route on next get_path call
        if next_pos not in self.game.object_handler.npc_locations:

            # calculate the angle if NPC looks at center of this tile
            angle = atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)

            # knowing the angle, calc increments for x, y-axis
            dx = cos(angle) * self.speed
            dy = sin(angle) * self.speed
            self.check_wall_collision(dx, dy)


    def attack(self):
        if self.animation_trigger:
            self.game.sound.npc_shot.play()
            # compare npc accuracy to decimal generated between [0, 1)
            if random() < randint(self.accuracy_percent[0], self.accuracy_percent[1]) / 100:
                damage = randint(self.attack_damage[0], self.attack_damage[1])
                self.game.player.get_damage(damage)


    def animate_death(self):
        if not self.alive:
            # increases the frame_counter, changes the frame, for every global timer trigger until anim complete
            if self.game.global_trigger and self.frame_counter < len(self.death_images) - 1:
                self.death_images.rotate(-1)
                self.image = self.death_images[0]
                self.frame_counter += 1


    def animate_pain(self):
        self.animate(self.pain_images)
        # trigger is false when animation completes, pain=False so animation does not restart
        if self.animation_trigger:
            self.pain = False


    def check_target_hit(self):
        if self.LOS and self.game.player.fired:
            # we know the edges of our sprite projection from other calculations
            if HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width:
                self.game.sound.npc_pain.play()
                self.game.player.fired = False
                self.pain = True
                self.health -= self.game.weapon.damage
                self.check_health()


    def check_health(self):
        if self.health < 1:
            self.alive = False
            self.game.sound.npc_death.play()


    def run_logic(self):
        if self.alive:
            self.LOS = self.player_has_LOS()
            self.check_target_hit()

            if self.pain:
                self.animate_pain()

            elif self.LOS:
                self.npc_search_trigger = True

                if self.dist < self.attack_dist:
                    self.animate(self.attack_images)
                    self.attack()
                else:
                    self.animate(self.walk_images)
                    self.movement()
                
            # while trigger is true, npc continues to search even if LOS lost
            elif self.npc_search_trigger and self.dist < self.search_dist:
                self.animate(self.walk_images)
                self.movement()
            else:
                self.animate(self.idle_images)
        else:
            self.animate_death()


    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    
    # this method returns a bool whether or not a ray can be cast between player and enemy (LOS=line of sight)
    # see raycasting.py for trig work commentation
    def player_has_LOS(self):
        # first check if player is in same tile as the npc - automatic LOS
        if self.game.player.map_pos == self.map_pos:
            return True

        # init dist variables
        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0

        px, py = self.game.player.pos
        map_x, map_y = self.game.player.map_pos

        # the ray angle is known to us from the Sprite class update method
        ray_angle = self.theta

        cos_a = cos(ray_angle)
        sin_a = sin(ray_angle)

        #
        # VERTICALS - see 'raycasting-coords-X.jpg'
        #
        x_vert, dx = (map_x + 1, 1) if cos_a > 0 else (map_x - 1e-6, -1)

        depth_vert = (x_vert - px) / cos_a
        y_vert = (depth_vert * sin_a) + py

        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)

            # if the tile is a wall or npc we record the instance
            if tile_vert == self.map_pos:    # npc
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.map.world_map:  # wall
                wall_dist_v = depth_vert
                break

            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        #
        # HORIZONTALS
        #
        y_hor, dy = (map_y + 1, 1) if sin_a > 0 else (map_y - 1e-6, -1)

        depth_hor = (y_hor - py) / sin_a
        x_hor = (depth_hor * cos_a) + px

        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)

            if tile_hor == self.map_pos:
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:  
                wall_dist_h = depth_hor
                break

            # extend ray to next horizontal intersection
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        # determine if there is a direct LOS based on max of these values
        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)

        # we have LOS if the following is true
        if 0 < player_dist < wall_dist or not wall_dist:
            return True

        # else we do not have LOS
        return False

    # debug draw for our LOS
    def debug_draw_ray_cast(self):
        # draw the npc
        pg.draw.circle(self.game.screen, 'red', (TILEPX * self.x, TILEPX * self.y), 15)

        # draw a line representing our LOS ray, if one exists
        if self.player_has_LOS():
            pg.draw.line(self.game.screen, 'orange', (TILEPX * self.game.player.x, TILEPX * self.game.player.y),
                        (TILEPX * self.x, TILEPX * self.y), 2)

#
# ENEMY CLASSES
#
class SoldierNPC(NPC):
    def __init__(self, game, path='resources/sprites/npc/soldier/0.png', pos=(10.5, 5.5),
                 scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)


class CacoDemonNPC(NPC):
    def __init__(self, game, path='resources/sprites/npc/caco_demon/0.png', pos=(10.5, 6.5),
                 scale=0.7, shift=0.27, animation_time=250):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_dist = 2
        self.search_dist = 10
        self.health = 150
        self.attack_damage = (18, 24)
        self.speed = 0.075
        self.accuracy_percent = (40, 60)


class CyberDemonNPC(NPC):
    def __init__(self, game, path='resources/sprites/npc/cyber_demon/0.png', pos=(11.5, 6.0),
                 scale=1.0, shift=0.04, animation_time=210):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_dist = 6
        self.search_dist = 8
        self.health = 350
        self.attack_damage = (15, 20)
        self.speed = 0.055
        self.accuracy_percent = (20, 30)
