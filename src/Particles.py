from Settings import *


def GET_ALL_IMAGES_IN_FOLDER(folder):
    images=[]
    image_files=os.listdir(folder)
    for image_file_name in image_files:
        img=pygame.image.load(os.path.join(folder,image_file_name))
        images.append(img)
    return images
    pass

class Animations:
    def __init__(self):
        self.graphics={
            #Magic spells.
            'flame':GET_ALL_IMAGES_IN_FOLDER(os.path.join(GRAPHICS_DIR_PATH,"PLAYER_MAGIC","flame")),
            'heal':GET_ALL_IMAGES_IN_FOLDER(os.path.join(GRAPHICS_DIR_PATH,"PLAYER_MAGIC","heal")),

            #Attack types.
            'claw':GET_ALL_IMAGES_IN_FOLDER(os.path.join(GRAPHICS_DIR_PATH,"ENEMY_ATTACKS","claw")),
            'slash':GET_ALL_IMAGES_IN_FOLDER(os.path.join(GRAPHICS_DIR_PATH,"ENEMY_ATTACKS","slash")),
            'sparkle':GET_ALL_IMAGES_IN_FOLDER(os.path.join(GRAPHICS_DIR_PATH,"ENEMY_ATTACKS","sparkle")),
            'thunder':GET_ALL_IMAGES_IN_FOLDER(os.path.join(GRAPHICS_DIR_PATH,"ENEMY_ATTACKS","thunder")),
        }

    def create_particles(self,animation_type,pos,groups):
        animation_frames=self.graphics[animation_type]
        ParticleEffect(pos,animation_frames,groups,)
        pass


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self,pos,animation_frames,groups):
        super().__init__(groups)
        self.pos=pos
        self.frame_index=0.1
        self.animation_speed=0.6
        self.frames=animation_frames
        self.image=self.frames[int(self.frame_index)]
        self.rect=self.image.get_rect(center=pos)

    def animate(self):
        self.frame_index+=self.animation_speed
        if(self.frame_index>len(self.frames)):
            self.kill()
        else:
            self.image=self.frames[int(self.frame_index)]

    def draw(self,display_surf,offset):
        newpos=self.rect.topleft-offset
        display_surf.blit(self.image,newpos)

    def update(self,display_surf,offset):
        self.animate()
        self.draw(display_surf,offset)