import pygame

class RandomLoot(pygame.sprite.Sprite):
    def __init__(self,pos,groups,img,name,val):
        super().__init__(groups)
        self.pos=pos
        self.img=img
        self.rect=self.img.get_rect(topleft=self.pos)
        self.name=name
        self.val=val

        self.created_time=pygame.time.get_ticks()
        self.despawn_timer=15000

    def update(self,display_surf,offset):
        newpos=self.rect.topleft-offset
        display_surf.blit(self.img,newpos)

        if pygame.time.get_ticks()-self.created_time>=self.despawn_timer:
            self.kill()