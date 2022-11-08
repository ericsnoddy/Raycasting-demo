# local
from sprite_object import *
from npc import *


class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_locations = {}
        self.npc_path = 'resources/sprites/npc/'
        self.static_path = 'resources/sprites/static_sprites/'
        self.animated_path = 'resources/sprites/animated_sprites/'
        
        # sprite map
        add_sprite = self.add_sprite   # brevity shortcuts - functions don't need ()
        add_npc = self.add_npc
        red_light = self.animated_path + 'red_light/0.png'

        add_sprite(Sprite(game))
        add_sprite(AnimatedSprite(game))
        add_sprite(AnimatedSprite(game, pos=(1.5, 1.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 7.5)))
        add_sprite(AnimatedSprite(game, pos=(5.5, 3.25)))
        add_sprite(AnimatedSprite(game, pos=(5.5, 4.75)))
        add_sprite(AnimatedSprite(game, pos=(7.5, 2.5)))
        add_sprite(AnimatedSprite(game, pos=(7.5, 5.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 1.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 4.5)))
        add_sprite(AnimatedSprite(game, path=red_light, pos=(14.5, 5.5)))
        add_sprite(AnimatedSprite(game, path=red_light, pos=(14.5, 7.5)))
        add_sprite(AnimatedSprite(game, path=red_light, pos=(12.5, 7.5)))
        add_sprite(AnimatedSprite(game, path=red_light, pos=(9.5, 7.5)))
        add_sprite(AnimatedSprite(game, path=red_light, pos=(14.5, 12.5)))
        add_sprite(AnimatedSprite(game, path=red_light, pos=(9.5, 20.5)))
        add_sprite(AnimatedSprite(game, path=red_light, pos=(10.5, 20.5)))
        add_sprite(AnimatedSprite(game, path=red_light, pos=(3.5, 14.5)))
        add_sprite(AnimatedSprite(game, path=red_light, pos=(3.5, 18.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 24.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 30.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 30.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 24.5)))

        # npc map
        add_npc(SoldierNPC(game, pos=(11.0, 19.0)))
        add_npc(SoldierNPC(game, pos=(11.5, 4.5)))
        add_npc(SoldierNPC(game, pos=(13.5, 6.5)))
        add_npc(SoldierNPC(game, pos=(2.0, 20.0)))
        add_npc(SoldierNPC(game, pos=(4.0, 29.0)))
        add_npc(CacoDemonNPC(game, pos=(5.5, 14.5)))
        add_npc(CacoDemonNPC(game, pos=(5.5, 16.5)))
        add_npc(CyberDemonNPC(game, pos=(14.5, 25.5)))


    def update(self):
        # build a dict of current positions so we ensure npcs do not marge/overlap one another while pathfinding.
        self.npc_locations = {npc.map_pos for npc in self.npc_list if npc.alive}

        # call the update method for all objects in our lists
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]


    def check_win(self):
        if not len(self.npc_positions):
            self.game.object_renderer.victory()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()


    def add_npc(self, npc):
        self.npc_list.append(npc)


    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)