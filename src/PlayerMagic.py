import pygame
from Settings import *
from random import randint

class MagicPlayer:
    def __init__(self,animation_player):
        self.animation_player=animation_player
        pass

    def heal(self,player,strength,cost,groups):
        if player.energy>=cost:
            player.energy-=cost
            player.health+=strength
            if(player.health>=player.stats['health']):
                player.health=player.stats['health']

            self.animation_player.create_particles('heal',player.rect.center,groups)

    def flame(self,player,cost,groups):
        if player.energy >= cost:
            player.energy-=cost

            direction_vector=pygame.math.Vector2()
            direction=player.status.split('_')[0]
            if direction=='right':
                direction_vector.x=1
            elif direction=='left':
                direction_vector.x=-1
            elif direction=='up':
                direction_vector.y=-1
            elif direction=='down':
                direction_vector.y=1 

            for i in range(1,6):
                if direction_vector.x:
                    offset_x=(direction_vector.x*i)*BASE_SIZE
                    x=player.rect.centerx+offset_x
                    y=player.rect.centery
                    self.animation_player.create_particles('flame',(x,y),groups)
                else:
                    offset_y=(direction_vector.y*i)*BASE_SIZE
                    x=player.rect.centerx
                    y=player.rect.centery+offset_y
                    self.animation_player.create_particles('flame',(x,y),groups)