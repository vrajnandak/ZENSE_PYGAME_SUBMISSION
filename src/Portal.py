import pygame
from Settings import *


class Portal(pygame.sprite.Sprite):
    def __init__(self,pos,groups,graphics_path):
        super().__init__(groups)
        self.pos=pos

        self.graphics_path=graphics_path
        self.graphics=[]                    #There is only one straightforward animation(to iterate over the list of images), so we can just use a list.
        self.load_portal_graphics()

        self.frame_index=0
        self.frames=len(self.graphics)
        self.frame_inc=0.4
        self.img=self.graphics[int(self.frame_index)]
        self.rect=self.img.get_rect(topleft=self.pos)

    def load_portal_graphics(self):
        image_files=os.listdir(self.graphics_path)
        for file_name in image_files:
            img=pygame.image.load(os.path.join(self.graphics_path,file_name))
            self.graphics.append(img)           #Since the files are numbered based on their indices, they would get appended in ascending order only.
        pass

    def update_img(self):
        self.frame_index=self.frame_index+self.frame_inc
        if(self.frame_index>=self.frames):
            self.frame_index=0
        self.img=self.graphics[int(self.frame_index)]
        pass

    def update(self,display_surf,offset):
        self.update_img()
        newpos=self.rect.topleft-offset
        display_surf.blit(self.img,newpos)
        pass