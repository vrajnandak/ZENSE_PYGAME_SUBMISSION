import pygame
from Settings import *

#A class to make obstacle sprites
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,obstacle_pos,obstacle_img,groups):
        super().__init__(groups)
        self.pos=obstacle_pos
        self.img=obstacle_img
        if(self.img==None):
            self.img=pygame.Surface((BASE_SIZE,BASE_SIZE))
            self.img.fill('black')
        self.rect=self.img.get_rect(topleft=self.pos)
        self.mask=pygame.mask.from_surface(self.img)

    def update(self,display_surf,offset):
        new_offset=self.rect.topleft-offset
        display_surf.blit(self.img,new_offset)