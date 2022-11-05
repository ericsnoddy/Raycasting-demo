# local
from sprite_object import *

class Weapon(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/weapon/shotgun/0.png', scale=0.4, animation_time=90, damage=50):
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale)) 
                for img in self.images])
        # center the weapon on screen
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.reloading = False
        self.num_frames = len(self.images)
        self.frame_counter = 0
        self.damage = damage


    def animate_shot(self):
        if self.reloading:
            self.game.player.fired = False
            if self.animation_trigger:
                # rotate the frames list but keep track of how many frames so we can stop appropriately
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_frames:
                    self.reloading = False
                    self.frame_counter = 0


    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)

    
    def update(self):
        # we need to call first method to get our animation trigger flag updated
        self.check_animation_time()
        self.animate_shot()