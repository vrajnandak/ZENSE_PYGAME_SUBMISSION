import pygame
from Settings import *
from Obstacle import *
from Player import *
from Enemy import *
from Button import *
from Portal import *
from CollisionHelper import CollisionHelper
from Weapon import Weapon
from Particles import Animations
from PlayerMagic import *
from RandomLoot import RandomLoot
from LEVEL_THINGS import *
import math
from math import inf

class Level:
    def __init__(self,level_id,player,settings):
        self.level_id=level_id
        self.GameSettings=settings

        #Getting the level information.
        self.level_information=LEVEL_INFO(self.level_id)
        self.has_displayed_level_start_msg=False
        self.timer=[5,0]            #Minutes and then seconds. Reduces every second.
        self.last_checked_time=0

        #Sprite groups of the level.
        self.enemy_sprites=pygame.sprite.Group()
        self.enemy_counter=0
        self.visible_sprites=pygame.sprite.Group()
        self.obstacle_sprites=pygame.sprite.Group()
        self.transport_sprites=pygame.sprite.Group()
        self.attack_sprites=pygame.sprite.Group()
        self.loot_drops=pygame.sprite.Group()
        self.unlockable_gate_sprites=pygame.sprite.Group()
        self.level_scientist=None

        self.curr_attack=None                               #The current weapon being used by player to attack.
        self.curr_selected_weapon=pygame.image.load(os.path.join(PLAYER_WEAPONS_DIRECTORY_PATH,list(self.GameSettings.WEAPON_INFO.keys())[0],'full.png'))
        self.curr_selected_magic=pygame.image.load(os.path.join(PLAYER_MAGIC_DIRECTORY_PATH,f'{list(self.GameSettings.MAGIC_INFO.keys())[0]}.png'))

        # #Some Event handlers to ensure that speaking events, other events happen only once or a limited number of times.
        self.game_finished=False
        self.has_triggered_event0=False
        self.has_triggered_event1=False
        self.has_triggered_event2=False
        self.has_triggered_event3=False
        self.has_triggered_event4=False

        self.secret_key=None            #Set up in the CreateMap() method.
        self.secret_key_img=pygame.image.load(os.path.join(GRAPHICS_DIR_PATH,"secret_key.png"))

        #Player of the level.
        self.player=player
        self.player.getAttackFunctions(self.create_attack,self.destroy_attack)
        self.player.getMagicFunctions(self.create_magic)
        self.player_pos=None
        self.directing_player_to_closest_enemy=False

        #Graphics of the level.
        self.graphics_path=os.path.join(MAPS_DIRECTORY_PATH,f'Ruin{self.level_id}')
        self.graphics={}            #Has 'elem_id' as key, and value is a list '[pygame_img,(imgwidth,imgheight)]
        self.loadGraphics()
        self.animation_player=Animations()
        self.magic_player=MagicPlayer(self.animation_player)

        #Collision Detecting class (Has all the functions needed for detecting collisions)
        self.collision_detector=CollisionHelper(self)
        self.detection_tiles=[]             #Will be filled with in createMap() itself. Used for pathfinding.
        self.createDetectionTiles()
        self.finder=AStarFinder()           #We don't mention diagonal movement as the sprites may not necessarily be able to move diagonally due to obstacles.

        self.random_loot_graphics={}
        self.getRandomLootGraphics()
        self.random_loot_graphics_names=list(self.random_loot_graphics.keys())

        #Creating the map.
        self.createMap()

        #Sizes for the Level. I am doing this in the hope that there will be less computations as these values are stored after __init__() is called.
        self.LEVEL_HEIGHT=self.baseFloorRect.bottom
        self.LEVEL_WIDTH=self.baseFloorRect.right

        #OFFSET
        self.offset=pygame.math.Vector2()           #This is the offset used for blitting sprites. This offset ranges from [0,self.RIGHT_OFFSET_VAL] for offset in x-axis and [0,self.BOTTOM_OFFSET_VAL] for offset in y-axis.
        self.LOWER_XOFFSET_LIM=0
        self.LOWER_YOFFSET_LIM=0
        self.UPPER_XOFFSET_LIM=self.LEVEL_WIDTH-SCREEN_WIDTH
        self.UPPER_YOFFSET_LIM=self.LEVEL_HEIGHT-SCREEN_HEIGHT
            #The below variables are used for calculating offsets for a good experience of camera movement. This is mainly with respect to player's position.
        self.RIGHT_OFFSET_BORDER=self.LEVEL_WIDTH-SCREEN_WIDTH_HALF
        self.LEFT_OFFSET_BORDER=SCREEN_WIDTH_HALF
        self.TOP_OFFSET_BORDER=SCREEN_HEIGHT_HALF
        self.BOTTOM_OFFSET_BORDER=self.LEVEL_HEIGHT-SCREEN_HEIGHT_HALF
        self.RIGHT_OFFSET_VAL=self.UPPER_XOFFSET_LIM
        self.BOTTOM_OFFSET_VAL=self.UPPER_YOFFSET_LIM
            #The below variables are used for calculating the offsets based on player movement, box position to show a box-camera movement.
        self.box_camera={'left':60,'right':60,'top':60,'bottom':60}
        default_left=self.player.rect.left
        default_top=self.player.rect.top
        box_width=SCREEN_WIDTH-(self.box_camera['left']+self.box_camera['right'])
        box_height=SCREEN_HEIGHT-(self.box_camera['top']+self.box_camera['bottom'])
        self.box_rect=pygame.Rect(default_left,default_top,box_width,box_height)
            #The below variables are used for calculating the offsets based on keyboard camera controls.
        self.keyboard_offset_counter=pygame.math.Vector2()      #'.x' is used for x-axis controlling, '.y' is used for y-axis controlling.
            #The below variables are used for calculating the offsets based on mouse positions.
        self.mouse_offset_counter=pygame.math.Vector2()         #'.x' is used for x-axis controlling, '.y' is used for y-axis controlling.
        self.MOUSE_RIGHT_LIMIT=SCREEN_WIDTH-30
        self.MOUSE_LEFT_LIMIT=30
        self.MOUSE_TOP_LIMIT=30
        self.MOUSE_BOTTOM_LIMIT=SCREEN_HEIGHT-30

    #A method to display the start messages of the level when loaded.
    def DisplayLevelStartMessages(self):
        bg_image=pygame.image.load(os.path.join(GRAPHICS_DIR_PATH,"STARTSCREEN_IMAGES",f'Ruin{self.level_id}.png'))
        display_surf=pygame.display.get_surface()
        DISPLAY_DIALOGS(self.level_information.start_msg,60,40,SCREEN_WIDTH-100,int(SCREEN_HEIGHT_HALF//2),bg_image)
        display_surf.blit(bg_image,(0,0))
        self.has_displayed_level_start_msg=True

    #A method to get the graphics of the random loot potions.
    def getRandomLootGraphics(self):
        graphics_path=os.path.join(GRAPHICS_DIR_PATH,"RANDOM_LOOT")
        files=os.listdir(graphics_path)
        for image_name in files:
            img=pygame.image.load(os.path.join(graphics_path,image_name))
            self.random_loot_graphics[image_name.split('.png')[0]]=img
        pass

    #A method to simply store the unique graphics for this level.
    def loadGraphics(self):
        #Load the different graphics in this folder. Since all the images have their id's, we can just parse the names of the files and then set the graphics.
        all_files_in_ruin=os.listdir(self.graphics_path)
        for file in all_files_in_ruin:
            if '.png' in file and BASEMAP_NAME not in file and ('not_obstacle' not in file):
                use_file_name=file[:-4]                     #Getting rid of the '.png' from the file name
                ind_strings=use_file_name.split('_',4)      #The ind_strings will be <name_of_obstacle>
                ind_strings[1:]=[int(num) if num.isdigit() else num for num in ind_strings[1:]]
                self.graphics[ind_strings[1]]=[pygame.image.load(os.path.join(self.graphics_path,file)),(ind_strings[2],ind_strings[3])]
            pass
        pass

    #A method to create the level's detection Tiles. Called only during creation of the level.
    def createDetectionTiles(self):
        self.baseFloorImg=pygame.image.load(os.path.join(self.graphics_path,BASEMAP_NAME))
        self.baseFloorRect=self.baseFloorImg.get_rect(topleft=(0,0))
        width_tiles=self.baseFloorRect.width//BASE_SIZE
        height_tiles=self.baseFloorRect.height//BASE_SIZE
        self.detection_tiles=[[1 for _ in range(width_tiles)] for _ in range(height_tiles)]
        pass

    #A method to create the map.
    def createMap(self):
        #Set up the key if not already
        if self.level_id==2:
            self.secret_key=pygame.rect.Rect(0,2000,2*BASE_SIZE,BASE_SIZE)
            pass

        #Figure out the Base Map.
        self.baseFloorImg=pygame.image.load(os.path.join(self.graphics_path,BASEMAP_NAME))
        self.baseFloorRect=self.baseFloorImg.get_rect(topleft=(0,0))

        #Figure out the layout using csv. User 'self.graphics' to create the objects
        FloorinfoPath=os.path.join(self.graphics_path,FLOORINFO_DIR_NAME)
        floorinfo_files=os.listdir(FloorinfoPath)

        #You now have the .csv files. Iterate through all of them and then create the objects. Use the comments in the settings to figure out where to place enemies, player, invisible_blocks based on id's.
        for file in floorinfo_files:
            with open(os.path.join(FloorinfoPath,file)) as map:
                layout=reader(map,delimiter=',')
                for row_index,row in enumerate(layout):
                    for col_index,val in enumerate(row):

                        x=col_index*BASE_SIZE
                        y=row_index*BASE_SIZE
                        if(val!='-1'):
                            val=int(val)
                            img_pos=(x,y)

                            if(val<100):                #The obstacle sprites.
                                img=self.graphics[int(val)]
                                img=img[0]
                                Obstacle(img_pos,img,[self.visible_sprites,self.obstacle_sprites])      #The instance of this class created is added to the given spriteGroups.
                                img_width=int(img.get_rect().width//BASE_SIZE)
                                img_height=int(img.get_rect().height//BASE_SIZE)
                                detection_tiles_row=len(self.detection_tiles)
                                detection_tiles_cols=len(self.detection_tiles[0])
                                for i in range(img_width+2):
                                    for j in range(img_height+2):
                                        new_row_index=row_index-1+j
                                        new_col_index=col_index-1+i
                                        if((new_row_index>=0 and new_row_index<detection_tiles_row) and (new_col_index>=0 and new_col_index<detection_tiles_cols)):
                                            self.detection_tiles[new_row_index][new_col_index]=0

                            if(val==100):
                                Enemy(img_pos,'zombie1',[self.enemy_sprites])
                                self.enemy_counter+=1
                            elif(val==101):
                                Enemy(img_pos,'zombie2',[self.enemy_sprites])
                                self.enemy_counter+=1
                            elif(val==102):
                                Enemy(img_pos,'zombie3',[self.enemy_sprites])
                                self.enemy_counter+=1
                            elif(val==103):
                                Enemy(img_pos,'zombie4',[self.enemy_sprites])
                                self.enemy_counter+=1
                            elif(val==104):
                                if self.level_id==3:
                                    Enemy(img_pos,'zombieBoss',[self.enemy_sprites])
                                    self.enemy_counter+=1
                            
                            elif(val==300):     #Scientist1
                                self.level_scientist=Scientist((x,y),[self.visible_sprites],1)
                                SCIENTIST_DIALOG_COLLIDE_RECTS['1']=pygame.rect.Rect(x-10*BASE_SIZE,y-10*BASE_SIZE,24*BASE_SIZE,24*BASE_SIZE)
                                pass
                            elif(val==301):     #Scientist2
                                self.level_scientist=Scientist((x,y),[self.visible_sprites],2)
                                SCIENTIST_DIALOG_COLLIDE_RECTS['2']=pygame.rect.Rect(x-10*BASE_SIZE,y-10*BASE_SIZE,24*BASE_SIZE,24*BASE_SIZE)
                                pass
                            elif(val==302):     #Scientist3
                                self.level_scientist=Scientist((x,y),[self.visible_sprites],3)
                                SCIENTIST_DIALOG_COLLIDE_RECTS['3']=pygame.rect.Rect(x-10*BASE_SIZE,y-10*BASE_SIZE,24*BASE_SIZE,24*BASE_SIZE)
                                pass

                            elif(val==500):             #The unlockable gate sprite.
                                img=pygame.image.load(os.path.join(self.graphics_path,"not_obstacle_unlockable_gate.png"))
                                Obstacle(img_pos,img,[self.unlockable_gate_sprites,self.obstacle_sprites,self.visible_sprites])
                                pass

                            elif(val==1000):
                                Obstacle(img_pos,None,[self.obstacle_sprites])
                                self.detection_tiles[row_index][col_index]=0
                                pass

                            elif(val==1001):
                                #This is to update the detection tiles properly so that the player's tiles are marked as '0'.
                                self.player.rect.left=x
                                self.player.rect.top=y

                            elif(val==1003):
                                Portal(img_pos,[self.visible_sprites,self.transport_sprites], os.path.join(self.graphics_path,"Portals"))

                            elif(val==1004):
                                pass

    #A method to get the offset for all the visible objects to be blit at, with the player being at the center of the screen except for when the player is at the corners of the screen.
    def get_player_based_offset(self):
        player_pos=self.player.rect.topleft     #Since the visible sprites are being blit() using pos(which is initialized to topleft position in createMap()), we use topleft only.

        #Getting the x-offset.
        if(player_pos[0]<self.LEFT_OFFSET_BORDER):
            self.offset.x=0
        elif(player_pos[0]>self.RIGHT_OFFSET_BORDER):
            self.offset.x=self.RIGHT_OFFSET_VAL
        else:
            self.offset.x=player_pos[0]-SCREEN_WIDTH_HALF

        #Gettings the y-offset.
        if(player_pos[1]<self.TOP_OFFSET_BORDER):
            self.offset.y=0
        elif(player_pos[1]>self.BOTTOM_OFFSET_BORDER):
            self.offset.y=self.BOTTOM_OFFSET_VAL
        else:
            self.offset.y=player_pos[1]-SCREEN_HEIGHT_HALF
    
    #A method to get the offset for the box-camera using the box_rect and the player position.
    def get_box_based_offset(self):
        if(self.player.rect.left < self.box_rect.left):
            self.box_rect.left=self.player.rect.left
        if(self.player.rect.right > self.box_rect.right):
            self.box_rect.right=self.player.rect.right
        if(self.player.rect.top < self.box_rect.top):
            self.box_rect.top=self.player.rect.top
        if(self.player.rect.bottom > self.box_rect.bottom):
            self.box_rect.bottom=self.player.rect.bottom

        self.offset.x=self.box_rect.left-self.box_camera['left']
        self.offset.y=self.box_rect.top-self.box_camera['top']
        self.player.offset=self.offset

    #A method to add the offset accumulated by keyboard keys to the final offset used for blitting sprites.
    def get_keyboard_based_offset(self,keys):
        if(keys[pygame.K_i] and ((self.offset.y + (self.keyboard_offset_counter.y-1)*self.GameSettings.KEYBOARD_CAMERA_SPEED)>0)):
            self.keyboard_offset_counter.y-=1
        if(keys[pygame.K_j] and ((self.offset.x + (self.keyboard_offset_counter.x-1)*self.GameSettings.KEYBOARD_CAMERA_SPEED)>0)):
            self.keyboard_offset_counter.x-=1
        if(keys[pygame.K_k] and ((self.offset.y + (self.keyboard_offset_counter.y+1)*self.GameSettings.KEYBOARD_CAMERA_SPEED) < self.UPPER_YOFFSET_LIM)):
            self.keyboard_offset_counter.y+=1
        if(keys[pygame.K_l] and ((self.offset.x + (self.keyboard_offset_counter.x+1)*self.GameSettings.KEYBOARD_CAMERA_SPEED) < self.UPPER_XOFFSET_LIM)):
            self.keyboard_offset_counter.x+=1
        
        self.offset=self.offset+self.keyboard_offset_counter*self.GameSettings.KEYBOARD_CAMERA_SPEED

    #A method to add the offset accumulated by mouse position to the final offset used for blitting sprites.
    def get_mouse_based_offset(self):
        mouse_pos=pygame.math.Vector2(pygame.mouse.get_pos())
        if(mouse_pos.x<=self.MOUSE_LEFT_LIMIT and (self.offset.x+(self.mouse_offset_counter.x-1)*self.GameSettings.MOUSE_CAMERA_SPEED)>0):
            self.mouse_offset_counter.x-=1
        elif(mouse_pos.x>=self.MOUSE_RIGHT_LIMIT and (self.offset.x+(self.mouse_offset_counter.x-1)*self.GameSettings.MOUSE_CAMERA_SPEED)<self.UPPER_XOFFSET_LIM):
            self.mouse_offset_counter.x+=1
        if(mouse_pos.y<=self.MOUSE_TOP_LIMIT and (self.offset.y+(self.mouse_offset_counter.y-1)*self.GameSettings.MOUSE_CAMERA_SPEED)>0):
            self.mouse_offset_counter.y-=1
        elif(mouse_pos.y>=self.MOUSE_BOTTOM_LIMIT and (self.offset.y+(self.mouse_offset_counter.y+1)*self.GameSettings.MOUSE_CAMERA_SPEED)<self.UPPER_YOFFSET_LIM):
            self.mouse_offset_counter.y+=1

        self.offset=self.offset+self.mouse_offset_counter*self.GameSettings.MOUSE_CAMERA_SPEED
    
    def apply_offset_limits(self):
        self.offset.x=min(max(self.LOWER_XOFFSET_LIM,self.offset.x),self.UPPER_XOFFSET_LIM)
        self.offset.y=min(max(self.LOWER_YOFFSET_LIM,self.offset.y),self.UPPER_YOFFSET_LIM)
        pass
    
    #Getting the offset accounting the different cameras.
    def get_offset(self,keys):
        #There are 3 types of offset. player_based_offset, (keyboard_keys_based_offset, mouse_based_offset). And pressing 'u' resets the offset to player_based_offset.
        if(keys[pygame.K_u]):                               #Ressetting the camera to the player.
            self.keyboard_offset_counter=pygame.math.Vector2()
            self.mouse_offset_counter=pygame.math.Vector2()
            pygame.mouse.set_pos((SCREEN_WIDTH_HALF,SCREEN_HEIGHT_HALF))

        elif(keys[pygame.K_b]):                             #Using box camera.
            self.get_box_based_offset()
            pass

        else:                                               #Using the default player-centered camera.
            self.get_player_based_offset()
            #Handling keyboard based camera movement.
            self.get_keyboard_based_offset(keys)
            self.get_mouse_based_offset()
            self.box_rect.center=self.player.rect.topleft               #So that there is no log when releasing or on clicking 'b'.
            
        self.apply_offset_limits()
        self.player.offset=self.offset

        pass

    #A method to create a weapon. It is better to handle the weapon as a separate entity from the player in order to not have to write extra code to deal with collisions.
    def create_attack(self):
        self.curr_attack=Weapon(self.player,[self.visible_sprites])
        pass

    #A method to destroy the created weapon.
    def destroy_attack(self):
        if self.curr_attack:
            self.curr_attack.kill()
            self.curr_attack=None

    #A method to create the magic.
    def create_magic(self,style,strength,cost):
        if(style=='heal'):
            self.magic_player.heal(self.player,strength,cost,[self.visible_sprites])
        if(style=='flame'):
            self.magic_player.flame(self.player,cost,[self.attack_sprites,self.visible_sprites])

    #A method to display the weapon selections.
    def display_selection(self,display_surf,left,top,has_switched,img=None,shd_display_count=None):
        #Draw the box.
        bg_rect=pygame.rect.Rect(left,top,ITEM_BOX_SIZE,ITEM_BOX_SIZE)
        pygame.draw.rect(display_surf,ITEM_BOX_BG_COLOR,bg_rect,0,border_radius=2)

        #Draw the borders.
        if has_switched==True:
            pygame.draw.rect(display_surf,ITEM_BOX_BORDER_COLOR_ACTIVE,bg_rect,2,border_radius=2)
        elif has_switched==False:
            pygame.draw.rect(display_surf,ITEM_BOX_BORDER_COLOR,bg_rect,2,border_radius=2)

        #Draw the image in the box.
        if(img!=None):
            image_pos=[bg_rect.centerx-img.get_width()//2,bg_rect.centery-img.get_height()//2]
            display_surf.blit(img,(image_pos[0],image_pos[1]))
            if shd_display_count!=None:
                count_surf=pygame.font.Font(None,20).render(f'x{shd_display_count}',False,'white')
                display_surf.blit(count_surf,(image_pos[0]+10+count_surf.get_width()//2,image_pos[1]+45))

    #A method to randomly drop a loot drop whenever an enemy sprite dies.
    def random_loot_drop(self,pos,zombieType):
        n=randint(0,2*len(self.random_loot_graphics_names))
        if(n<len(self.random_loot_graphics_names)):
            loot_name=self.random_loot_graphics_names[n]
            #Making the drop have stats based on the zombie Type killed.
            if(zombieType[-1].isdigit()):
                val=int(zombieType[-1])-1
            else:
                val=4
            RandomLoot(pos,[self.visible_sprites,self.loot_drops],self.random_loot_graphics[loot_name],loot_name,val)
        pass

    #A method to check if the player has attacked any sprite by checking the weapon sprite collision with the sprite groups.
    def player_attack(self):
        attacking_sprites=[self.attack_sprites,[self.curr_attack]]
        for index,sprite_group in enumerate(attacking_sprites):
            if sprite_group:                                                        #If spriteGroup exists.

                for sprite in sprite_group:
                    if sprite:                                                      #If the sprite exists.

                        collision_sprites=pygame.sprite.spritecollide(sprite,self.enemy_sprites,False)
                        if collision_sprites:                                       #If there are enemy sprites colliding with either 'weapon' or 'magic' sprites of player.

                            for target_sprite in collision_sprites:
                                target_sprite_pos=target_sprite.rect.topleft
                                ret_val=target_sprite.reduce_health(self.player,index)                          #Deal damage to the enemy.
                                if(ret_val==1):
                                    self.enemy_counter-=1
                                    self.random_loot_drop(target_sprite_pos,target_sprite.zombieType)           #Drop a random loot based on the stats of the enemy killed.

                                    if(self.enemy_counter==0):                                                  #Increase player stats if all enemies are cleared. Handle some scientist specific events.
                                        if self.level_id==1:
                                            self.player.has_cleared_maps[1]=True
                                        elif self.level_id==2:
                                            self.level_information.handle_event(EVENT_CODES[1],self)
                                            self.has_triggered_event1=True

                                        if self.level_scientist!=None and self.level_id!=2:
                                            self.level_information.handle_event(EVENT_CODES[1],self)
                                            self.has_triggered_event1=True
                                            self.level_scientist.shd_escape_from_ruin=True
                                            self.level_scientist.initialize_escape_path(self)
                                        
                                        if not self.game_finished:
                                            SaveGameScreen()
                                            bg_image=pygame.image.load(os.path.join(GRAPHICS_DIR_PATH,"Curr_Screen.png"))
                                            DISPLAY_DIALOGS([f'Reward for Destroying all Enemies in Ruin{self.level_id}:\nPlayer Attack Inc by 10\nPlayer Magic Inc by 10\nPlayer speed Inc by 2.'],60,40,SCREEN_WIDTH-100,int(SCREEN_HEIGHT_HALF//2),bg_image)
                                            self.GameSettings.PLAYER_SPEED=self.GameSettings.PLAYER_SPEED+2
                                            self.player.stats['attack']+=10
                                            self.player.stats['magic']+=10
    
    #A method to damage the player whenever an enemy sprite attacks the player.
    def damage_the_player(self,amount,attack_type):
        if self.player.can_get_hit:
            self.player.health-=amount
            self.player.can_get_hit=False
            self.player.hit_time=pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type,self.player.rect.center,[self.visible_sprites])
        pass
    
    #A method to display the starting dialog of the scientist.
    def display_dialog_box_by_scientist(self):
        scientist_collide_rect=SCIENTIST_DIALOG_COLLIDE_RECTS[f'{self.level_id}']
        if scientist_collide_rect!=None:
            if self.player.rect.colliderect(scientist_collide_rect) and not self.has_triggered_event0:
                SaveGameScreen()
                bg_image=pygame.image.load(os.path.join(GRAPHICS_DIR_PATH,"Curr_Screen.png"))
                DISPLAY_DIALOGS(self.level_scientist.dialogs[EVENT_CODES[0]],60,40,SCREEN_WIDTH-100,int(SCREEN_HEIGHT_HALF//2),bg_image)
                self.has_triggered_event0=True

    #Method to draw the arrow, directed to the closest enemy, at a distance from the player.
    def draw_arrow_to_enemy(self,vector_2_enemy):
        #Getting the angle of enemy-player vector.
        angle=math.degrees(math.atan2(vector_2_enemy.y, vector_2_enemy.x))-90

        #Rotating the image.
        img=self.player.animate_arrow_and_return()
        img=pygame.transform.rotate(img,-angle)

        #Getting the topleft position of the rotated image to be drawn at.
        radius=pygame.math.Vector2(0,DIRECTION2_ENEMY_RADIUS).rotate(angle)
        center_point=(self.player.rect.left-self.offset.x,self.player.rect.top-self.offset.y)
        pt_x,pt_y=center_point[0]-radius.x,center_point[1]-radius.y

        #Drawing the arrow.
        display_surf=pygame.display.get_surface()
        display_surf.blit(img,(pt_x,pt_y))

    #A method to get the vector to the closest enemy.
    def direct_player_to_closest_enemy(self):
        closest_distance=inf
        closest_distance_vector=None
        for sprite in self.enemy_sprites:
            curr_player_enemy_vector=pygame.math.Vector2(self.player.rect.centerx-sprite.rect.centerx, self.player.rect.centery-sprite.rect.centery)        #We're making the vector point towards the player because of the way the image of the arrow is in the graphics(pointing to the top)
            curr_player_enemy_distance=curr_player_enemy_vector.magnitude()
            if closest_distance>curr_player_enemy_distance:
                closest_distance=curr_player_enemy_distance
                closest_distance_vector=curr_player_enemy_vector

        #Draw the arrow if there is no enemy within the 'DRAW_TO_ENEMY' radius of the player.
        if self.enemy_counter>0 and closest_distance_vector!=None and closest_distance>DRAW_TO_ENEMY:
            self.draw_arrow_to_enemy(closest_distance_vector)

    #A method to update the timer of the Ruin3.
    def update_timer(self):
        curr_time=pygame.time.get_ticks()
        if curr_time-self.last_checked_time>=1000:
            self.last_checked_time=curr_time
            if self.timer[1]==0:
                if self.timer[0]==0:
                    SaveGameScreen()
                    bg_image=LoadCurrScreen()
                    DISPLAY_DIALOGS(["YOU RAN OUT OF TIME"],60,40,SCREEN_WIDTH-100,int(SCREEN_HEIGHT_HALF//2),bg_image=bg_image)
                    return 10           #Indicating you've lost.
                else:
                    self.timer[0]-=1
                    self.timer[1]=59
            else:
                self.timer[1]-=1

    #The level logic.
    def run(self,keys):
        shd_transport=self.player.move(keys,self)

        #Storing the key in the player's inventory if obtained.
        if self.secret_key!=None and (not self.player.has_cleared_maps[2]) and self.secret_key.colliderect(self.player.rect) and pygame.key.get_pressed()[pygame.K_e]:
            SaveGameScreen()
            bg_image=LoadCurrScreen()
            DISPLAY_DIALOGS(self.level_scientist.dialogs[EVENT_CODES[3]],60,40,SCREEN_WIDTH-100,int(SCREEN_HEIGHT_HALF//2),bg_image)
            self.player.has_cleared_maps[2]=True
            for sprite in self.unlockable_gate_sprites:
                sprite.kill()
            self.level_scientist.shd_escape_from_ruin=True
            self.level_scientist.initialize_escape_path(self)
            self.secret_key=None
            self.player.inventory_items['SECRET_KEY'][0]=True


        if(shd_transport==1):
            SaveGameScreen(filename=os.path.join("TRANSITIONED_OUT_OF",f'Ruin{self.level_id}.png'))
            shd_use_portal_and_change_map=self.level_information.handle_event(EVENT_CODES[2],self)
            if(shd_use_portal_and_change_map):
                self.player_pos=self.player.rect.topleft        #Saving the player's position so that the next time player comes back to this level, he starts from here.
                return shd_transport
        
        #Checking player collision with scientist's dialog box.
        self.display_dialog_box_by_scientist()
        
        #Get the Offset
        self.get_offset(keys)

        #Draw the BaseMap Image after considering offset
        display_surf=pygame.display.get_surface()
        baseFloor_offset=self.baseFloorRect.topleft-self.offset
        display_surf.blit(self.baseFloorImg,baseFloor_offset)

        #Draw the visible sprites after considering offset
        self.enemy_sprites.update(display_surf,self.offset,self)
        self.visible_sprites.update(display_surf,self.offset)
        if self.secret_key!=None:
            display_surf.blit(self.secret_key_img,(self.secret_key.left-self.offset.x,self.secret_key.top-self.offset.y))
        self.player.draw(display_surf,self.offset)
        
        self.player_attack()
        if(self.player.health<=0):
            SaveGameScreen()
            return 10
        if self.game_finished==True:
            return 11
        
        self.player.display_ui(display_surf)

        self.direct_player_to_closest_enemy()

        #Displaying the weapon selection.
        self.display_selection(display_surf,10,SCREEN_HEIGHT-ITEM_BOX_SIZE,not self.player.can_switch_weapon,self.curr_selected_weapon)

        #Displaying the magic selection.
        self.display_selection(display_surf,10,SCREEN_HEIGHT-2*ITEM_BOX_SIZE - 20, not self.player.can_switch_magic, self.curr_selected_magic)

        #Displaying the Dialog Log Box to access previous dialogs.
        self.display_selection(display_surf,SCREEN_WIDTH-ITEM_BOX_SIZE-20,SCREEN_HEIGHT-3*ITEM_BOX_SIZE-40,False,img=DisplayDialogIMG)

        #Displaying the player's inventory.
        for index,key in enumerate(list(self.player.curr_selected_inventory_item.keys())):
            self.display_selection(display_surf,int(SCREEN_WIDTH//4)+110+index*(ITEM_BOX_SIZE), SCREEN_HEIGHT-ITEM_BOX_SIZE-20, self.player.curr_selected_inventory_item[key],self.player.inventory_items[key][1] if self.player.inventory_items[key][0]>0 else None,shd_display_count=(self.player.inventory_items[key][0] if (self.player.inventory_items[key][0]>0 and key!="SECRET_KEY" )else None))

        #Performing necessary timer related updates.
        if self.level_id==3:
            ret_val=self.update_timer()
            if ret_val==10:
                return ret_val
            if self.timer[1]<10:
                debug_print(f'{self.timer[0]} : 0{self.timer[1]}',(SCREEN_WIDTH_HALF,200))
            else:
                debug_print(f'{self.timer[0]} : {self.timer[1]}',(SCREEN_WIDTH_HALF,200))
        return 0
    
    #A method to draw the detection tiles(a matrix consisting of tiles, one per BASE_SIZExBASE_SIZE area, over the entire level), used for path-finding for enemies.
    def draw_map_detection_tiles(self,display_surf):
        for row_index,row in enumerate(self.detection_tiles):
            for col_index,val in enumerate(row):
                pos=(col_index*BASE_SIZE,row_index*BASE_SIZE)
                newpos=pos-self.offset
                debug_print(val,newpos,display_surf)

    def saveLevel(self):
        levelData=self.__dict__.copy()
        levelData['GameSettings']=None
        levelData['level_information']=None
        levelData['enemy_sprites']=enemySprites_to_dict(self.enemy_sprites)
        levelData['visible_sprites']=None
        levelData['obstacle_sprites']=None
        levelData['transport_sprites']=None
        levelData['attack_sprites']=None
        levelData['loot_drops']=lootSprites_to_dict(self.loot_drops)        # 'img' attribute will be created using the 'name' attribute.
        levelData['unlockable_gate_sprites']=len(self.unlockable_gate_sprites)       #1 indicates that the sprites are present, 0 indicates that the sprites have been killed.
        levelData['level_scientist']=scientist_to_dict(self.level_scientist)

        #The last 2 in the below 3 will be automatically loaded.
        levelData['curr_attack']=None
        levelData['curr_selected_weapon']=None
        levelData['curr_selected_magic']=None

        levelData['secret_key']=rect_to_dict(self.secret_key)
        levelData['secret_key_img']=None

        levelData['player']=None
        levelData['baseFloorImg']=None
        levelData['baseFloorRect']=rect_to_dict(self.baseFloorRect)
        levelData['graphics']=None
        levelData['animation_player']=None
        levelData['magic_player']=None
        levelData['collision_detector']=None
        levelData['detection_tiles']=None
        levelData['finder']=None
        levelData['random_loot_graphics']=None
        levelData['random_loot_graphics_names']=None

        levelData['offset']=vect2_to_dict(self.offset)

        levelData['box_rect']=rect_to_dict(levelData['box_rect'])
        levelData['keyboard_offset_counter']=vect2_to_dict(levelData['keyboard_offset_counter'])
        levelData['mouse_offset_counter']=vect2_to_dict(levelData['mouse_offset_counter'])

        return levelData
    
    #A method to load the Level with the saved data.
    def useSavedData(self, levelData):
        #Loading enemy sprites
        self.enemy_counter=levelData['enemy_counter']
        enemySpritesData=levelData['enemy_sprites']
        self.enemy_sprites=pygame.sprite.Group()
        for enemyData in enemySpritesData:
            #Create the enemy using Enemy data.
            img_pos=(enemyData['rect']['x'], enemyData['rect']['y'])
            enemy_created=Enemy(img_pos,enemyData['zombieType'],[self.enemy_sprites])
            enemy_created.useSavedData(enemyData)
            pass

        #Loading loot sprites
        self.loot_drops=pygame.sprite.Group()
        loot_drops_data=levelData['loot_drops']
        for loot_drop in loot_drops_data:
            pos=(loot_drop['rect']['x'],loot_drop['rect']['y'])
            RandomLoot(pos,[self.visible_sprites,self.loot_drops],self.random_loot_graphics[loot_drop['name']],loot_drop['name'],loot_drop['val'])
            pass

        #Loading unlockable gate sprites based on whether the value is '1' or '0'.
        if(levelData['unlockable_gate_sprites']!=0):
            for sprite in self.unlockable_gate_sprites:
                sprite.kill()

        #Loading the level scientist if any.
        if(levelData['level_scientist']!=None):
            scientist_data=levelData['level_scientist']
            self.level_scientist.rect=pygame.rect.Rect(scientist_data['rect']['x'], scientist_data['rect']['y'],scientist_data['rect']['width'],scientist_data['rect']['height'])
            self.level_scientist.direction=pygame.math.Vector2(scientist_data['direction']['x'], scientist_data['direction']['y'])
            self.level_scientist.shd_escape_from_ruin=scientist_data['shd_escape_from_ruin']
            self.level_scientist.end_rect_topleft=scientist_data['end_rect_topleft']

        #Loading the secret key based on whether or not the rect exists or not, because if player has already collected key, then the rect would be none itself.
        self.secret_key=None if levelData['secret_key']==None else self.secret_key
        
        #Loading baseFloorRect.
        self.baseFloorRect=pygame.rect.Rect(levelData['baseFloorRect']['x'],levelData['baseFloorRect']['y'],levelData['baseFloorRect']['width'],levelData['baseFloorRect']['height'])

        #Loading offset
        self.offset=pygame.math.Vector2(levelData['offset']['x'],levelData['offset']['y'])
        #Loading box_rect
        self.box_rect=pygame.rect.Rect(levelData['box_rect']['x'],levelData['box_rect']['y'],levelData['box_rect']['width'],levelData['box_rect']['height'])

        #Loading keyboard_offset_counter
        self.keyboard_offset_counter=pygame.math.Vector2(levelData['keyboard_offset_counter']['x'],levelData['keyboard_offset_counter']['y'])
        #Loading mouse_offset_counter
        self.mouse_offset_counter=pygame.math.Vector2(levelData['mouse_offset_counter']['x'],levelData['mouse_offset_counter']['y'])

        self.has_displayed_level_start_msg=levelData['has_displayed_level_start_msg']
        self.timer=levelData['timer']
        # self.last_checked_time=levelData['last_checked_time']
        self.enemy_counter=levelData['enemy_counter']
        self.game_finished=levelData['game_finished']
        self.has_triggered_event0=levelData['has_triggered_event0']
        self.has_triggered_event1=levelData['has_triggered_event1']
        self.has_triggered_event2=levelData['has_triggered_event2']
        self.has_triggered_event3=levelData['has_triggered_event3']
        self.has_triggered_event4=levelData['has_triggered_event4']

        self.secret_key=levelData['secret_key']
        self.directing_player_to_closest_enemy=levelData['directing_player_to_closest_enemy']
        self.player_pos=levelData['player_pos']
        pass