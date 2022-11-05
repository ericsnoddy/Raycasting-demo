# std lib
from random import randint, random, choice

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

        self.attack_dist = randint(3, 6)
        self.speed = 0.03
        self.size = 10
        self.health = 100
        self.attack_damage = 10
        self.accuracy = 0.15
        self.alive = True
        self.pain = False


    def update(self):
        self.check_animation_time()
        self.get_sprite()
        self.run_logic()


    def animate_pain(self):
        self.animate(self.pain_images)
        # trigger is false when animation completes, pain=False so animation does not restart
        if self.animation_trigger:
            self.pain = False


    def check_target_hit(self):
        if self.game.player.fired:
            # we know the edges of our sprite projection from other calculations
            if HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width:
                self.game.sound.npc_pain.play()
                self.game.player.fired = False
                self.pain = True


    def run_logic(self):
        if self.alive:
            self.check_target_hit()
            if self.pain:
                self.animate_pain()
            else:
                self.animate(self.idle_images)