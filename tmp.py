# import pygame
# import os

# pygame.init()
# WORKING_DIRECTORY_PATH=os.getcwd()
# GRAPHICS_DIR_PATH=os.path.join(WORKING_DIRECTORY_PATH,"graphics")
# def getSpriteFromSpriteSheet(spritesheet_path,sprite_width,sprite_height,sprite_location_left,sprite_location_top,colorKey=None):
#     spritesheet=pygame.image.load(spritesheet_path)
#     sprite=pygame.Surface((sprite_width,sprite_height)).convert_alpha()
#     sprite.blit(spritesheet,(0,0),(sprite_location_left,sprite_location_top,sprite_width,sprite_height))
#     if(colorKey==None):
#         sprite.set_colorkey(colorKey)
#     return sprite

# Window=pygame.display.set_mode((550,550),pygame.RESIZABLE)
# img=getSpriteFromSpriteSheet(os.path.join(GRAPHICS_DIR_PATH,"Blocks.png"),32,32,32,0,'Black')
# while True:
#     for event in pygame.event.get():
#         if event.type==pygame.QUIT:
#             pygame.quit()
#     Window.fill('white')
#     surf=pygame.image.load('EXAMPLE_IMAGES_FOR_SPRITES/Archaeologist_sprites.png')    #The player sprite to be used is the 'Archaeologist_sprites.png'
#     surf=pygame.transform.scale(surf,(1024,448))

#     Window.blit(surf,(0,0))
#     Window.blit(img,(1100,0))
#     pygame.display.flip()

# class Player:
#     def __init__(self, name):
#         self.name = name
#         self.level = 1  # Example attribute
#         self.helper = Player.PlayerHelperMethods(self)  # Pass a reference to self

#     def play(self):
#         print(f"{self.name} is playing at level {self.level}.")
#         self.helper.do_something()

#     def pause(self):
#         print(f"{self.name} paused.")

#     class PlayerHelperMethods:
#         def __init__(self, player_instance):
#             self.player = player_instance
        
#         def do_something(self):
#             # Accessing attributes from the outer class and potentially modifying them
#             print(f"Helper method doing something for {self.player.name} at level {self.player.level}.")
#             # Modifying the outer class attribute]
#             self.player.level+=3

# # Example usage:
# player = Player("Alice")
# player.play()
# player.pause()
# player.play()
# player.pause()


# import pygame
# import os
# # from TMPPortal import Portal
# pygame.init()
# pygame.font.init()

# current_Dir=os.getcwd()
# current_Dir=os.path.join(current_Dir,"graphics")
# current_Dir=os.path.join(current_Dir,"Ruins")
# current_Dir=os.path.join(current_Dir,"Ruin0")
# current_Dir=os.path.join(current_Dir,"Portals")
# # current_Dir=os.path.join(current_Dir,"1.png")
# screen=pygame.display.set_mode((500,500))
# # img=pygame.image.load(current_Dir)
# # img_rect=img.get_rect(topleft=(0,0))
# print('curren',current_Dir)
# # print('img size: ',img_rect.width,img_rect.height)
# # portal=Portal((100,100),current_Dir)
# while True:
#     for event in pygame.event.get():
#         if event.type==pygame.QUIT:
#             pygame.quit()
#             break
#     # screen.fill('white')
#     # portal.update(screen,pygame.math.Vector2(0,0))
#     # screen.blit(img,(0,0))
#     pygame.display.flip()

# import time
# my_timer_start=time.time()
# from pathfinding.core.grid import Grid
# from pathfinding.finder.a_star import AStarFinder

# my_matrix=[
#     [1,1,1,0,1,1],
#     [1,0,1,1,1,1],
#     [1,0,0,1,1,1]
# ]
# my_grid=Grid(matrix=my_matrix)
# start_x=0       #Starting cell col number
# start_y=0       #Starting cell row number
# start_cell=my_grid.node(start_x,start_y)
# end_x=5
# end_y=2
# end_cell=my_grid.node(end_x,end_y)

# #Create a finder with a movement style.
# finder=AStarFinder()

# #path is as implied, runs is the number of cells you have to go through
# path,runs=finder.find_path(start_cell,end_cell,my_grid)
# my_timer_end=time.time()
# print(path,runs)
# print('cell: ', path[1])
# print(type(path[0]))
# print('node.x: ', path[1].x)        #Gets the col number of that node.
# print(my_grid)
# print(len(path))
# print("Total time: ", my_timer_end-my_timer_start)

# import pygame
# pygame.init()
# clock=pygame.time.Clock()
# screen=pygame.display.set_mode((500,500))
# while True:
#     for event in pygame.event.get():
#         if event.type==pygame.QUIT:
#             pygame.quit()
#     screen.fill('black')
#     keys=pygame.key.get_pressed()
#     a=(keys[pygame.K_UP]+keys[pygame.K_w])-(keys[pygame.K_DOWN]+keys[pygame.K_s])
#     print(a)
#     clock.tick(30)


# for i in range(5,3,-1):
#     print(i)

# matrix=[
#     [1,1,1,1,1],
#     [1,1,1,1,1],
#     [1,1,1],
#     [0,0,0,]
# ]
# print(len(matrix))

# my_dictionary={
#     'attr_name':['hi','bye'],
#     'attr_name2':['hi2','bye2']
# }

# for index,name in enumerate(my_dictionary.keys()):
#     print(name,index)

# import pygame
# pygame.init()
# # print(pygame.K_0)
# # print(pygame.K_9)
# SCREEN_WIDTH=1240
# SCREEN_HEIGHT=800
# SCREEN_WIDTH_HALF=SCREEN_WIDTH//2
# SCREEN_HEIGHT_HALF=SCREEN_HEIGHT//2
# screen=pygame.display.set_mode((500,500))
# base_inventory_surf=pygame.Surface((SCREEN_WIDTH_HALF,50))
# base_inventory_surf.fill('#A8A9Ad')
# # self.inventory_item_border=pygame.Surface(40,50)
# # self.inventory_item_border.fill('#A8A9Ad')
# inventory_item_rect=pygame.rect.Rect(0+5,5,40,40)
# for i in range(5):
#     pygame.draw.rect(base_inventory_surf,'black',inventory_item_rect,0)
#     inventory_item_rect.x+=40+5
#     pass
# while True:
#     for event in pygame.event.get():
#         if event.type==pygame.QUIT:
#             pygame.quit()
#             # sys.exit()
#         # if event.type==pygame.KEYDOWN:
#             # print('event key: ', event.key)
#         if event.type == pygame.MOUSEWHEEL:
#             print(event.x, event.y)
#             #event.y is 1 for scrolling up.
#             #event.y is -1 for scrolling down.

#     screen.fill('blue')
#     screen.blit(base_inventory_surf,(0,0))
#     pygame.display.flip()

# extra_attr_names=['(Cooldown)','(Damage)']*3 + ['(Cooldown)','(Strength)','(Cost)']*2
# print(extra_attr_names)

# extra_attr_names=['(Cooldown)','(Damage)']*3 + ['(Cooldown)','(Strength)','(Cost)']*2
# SCREEN_WIDTH=1240
# SCREEN_HEIGHT=800
# val_changer_height=int((3*SCREEN_HEIGHT)//9)
# val_changer_width=int(SCREEN_WIDTH//6)
# width_gap=35
# height_gap=60
# base_height=200
# attribute_names=[         #The list contains in order [min_val,max_val,cost_of_exp_for_increasing_by_one_unit]
#             "GAME_FPS",
#             "PLAYER_SPEED",
#             "ENEMY_SPEED",
#             "KEYBOARD_CAMERA_SPEED",
#             "MOUSE_CAMERA_SPEED",
#             "Weapon1 Cooldown",              
#             "Weapon1 Damage",
#             "Weapon2 Cooldown",              
#             "Weapon2 Damage",
#             "Weapon3 Cooldown",              
#             "Weapon3 Damage",
#             # "Weapon4 Cooldown",              
#             # "Wepon4 Damage",
#             # "Weapon5 Cooldown",              
#             # "Wepon5 Damage",
#             "Magic1 Cooldown",
#             "Magic1 Strength",
#             "Magic1 Cost",
#             "Magic2 Cooldown",
#             "Magic2 Strength",
#             "Magic2 Cost",
#         ]
# for index,item_name in enumerate(attribute_names):
#     left=width_gap+(index%5)*val_changer_width+width_gap*(index%5)
#     top=base_height+int(index//5)*(val_changer_height + height_gap)
#     print(left,top)


# my_dict={
#     '1':"HIKLJD",
#     '2':"KDJFLJLSDJFLSD"
# }
# print(my_dict[f'{1}'])



# from math import inf
# print(inf<=1111110)
# print(inf>inf)

# import pygame
# rect=pygame.rect.Rect(10,20,30,40)
# print('rect.topleft', rect.topleft)

# my_dict={'oqiwue':'1','sdkjf':'2'}
# for index,keys in enumerate(list(my_dict.keys())):
#     print(index)

# import pygame
# import json
# pygame.init()
# tmpfont=pygame.font.Font(None,30)
# print(tmpfont.get_linesize())
# rect=pygame.Rect(276,200,206,266)
# vector=pygame.math.Vector2(2,3)
# with open('data.json', 'w') as f:
#     json.dump(vector,f)



import pygame
# import pygame.camera
# from pygame.locals import *
pygame.init()
# pygame.camera.init()
# print(pygame.camera.list_cameras())
# cam=pygame.camera.Camera("/tmp/pygameZense/Video",(640,480,"RGB"))
# cam.start()
# image=cam.get_image()
tmp_group=pygame.sprite.Group()

if(tmp_group):
    print('gorup aint empty')
else:
    print('group is really empty')



class Obstacle(pygame.sprite.Sprite):
    def __init__(self,obstacle_pos,obstacle_img,groups):
        super().__init__(groups)
        self.pos=obstacle_pos
        self.img=obstacle_img
        if(self.img==None):
            self.img=pygame.Surface((32,32))
            self.img.fill('black')
        self.rect=self.img.get_rect(topleft=self.pos)
        self.mask=pygame.mask.from_surface(self.img)

    def update(self,display_surf,offset):
        new_offset=self.rect.topleft-offset
        display_surf.blit(self.img,new_offset)

print('the number of sprites: ', len(tmp_group))
Obstacle((32,32),pygame.Surface((32,32)),[tmp_group])
print('the number of sprites: ', len(tmp_group))