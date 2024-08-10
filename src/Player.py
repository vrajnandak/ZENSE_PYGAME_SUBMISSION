import pygame
from Settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,settings):
        pygame.sprite.Sprite.__init__(self)          #Calling the constructor of the sprite class so that we can add the player to the visible_sprites spriteGroup.
        self.pos=pos

        #Different unlocking event's variables.
        self.has_entered_correct_code=False
        self.has_cleared_maps=[False,False,False,False]

        #Inventory Items
        self.inventory_items={}
        self.loadInventoryItems()
        self.curr_selected_inventory_item_index=None
        self.inventory_boxes_num=len(self.inventory_items)-1          #0-Indexing.
        self.curr_selected_inventory_item={
            "HEALTH_POTION":False,
            "ENERGY_POTION":False,
            "EXP_POTION":False,
            "SECRET_KEY":False,
            "INVENTORY_NUM5":False
        }

        #List of all the potions collected by the player.
        self.health_potions_vals=[]
        self.exp_potions_vals=[]
        self.energy_potions_vals=[]

        #Getting the game's settings.
        self.GameSettings=settings

        #Loading player graphics.
        self.player_graphics_path=PLAYER_DIRECTORY_PATH
        self.load_my_graphics()

        #Default image.
        self.img=self.graphics['right_idle'][0]
        self.rect=self.img.get_rect(topleft=self.pos)
        self.mask=pygame.mask.from_surface(self.img)
        self.status='down'          #Used for controlling the images to be loaded of the player.
        self.frame_index=0.1        #To loop over the list of images for a certain animation state.
        self.animation_speed=0.4    #The speed at which the frame index increases.

        #Player Dimensions - Used for updating the tiles.
        self.width_tiles=int(self.rect.width//BASE_SIZE)
        self.height_tiles=int(self.rect.height//BASE_SIZE)

        #Player movement
        self.direction=pygame.math.Vector2()        #A vector to only get the directions of the player.
        self.offset=pygame.math.Vector2()   #A vector to hold the position at which the player has to be blit at. The value is set in the get_offset() in Level.

        #Attack variables
        self.attack_cooldown=400
        self.attacking=False
        self.attack_time=None
        self.createAttack=None
        self.destroyAttack=None

        #Magic variables
        self.magic_cooldown=500
        self.magicing=False
        self.magic_time=None
        self.createMagic=None       #Magic is automatically destroyed.

        #Weapon variables
        self.weapon_index=0
        self.weapon_name=list(self.GameSettings.WEAPON_INFO.keys())[self.weapon_index]
        self.weapon_switch_cooldown=200
        self.can_switch_weapon=True
        self.weapon_switch_time=None

        #Magic dynamic variables.
        self.magic_index=0
        self.magic_name=list(self.GameSettings.MAGIC_INFO.keys())[self.magic_index]
        self.magic_switch_cooldown=200
        self.can_switch_magic=True
        self.magic_switch_time=None

        #Player stats.
        self.stats={'health':1000,'energy':100,'attack':50,'magic':4,'speed':self.GameSettings.PLAYER_SPEED}        #These are the default or caps on player stats.
        self.health=self.stats['health']
        self.energy=self.stats['energy']
        self.exp=1
        self.exp_cap=100                        #This will be updated to a new cap whenever the self.exp >= self.exp_cap.
        self.speed=self.stats['speed']
        self.player_level=0

        #Player level up timers.
        self.player_level_up_time=None
        self.player_level_up_msg_duration=4000
        self.player_level_up=False

        #Player UI
        self.loadUI()
        

        #Enemy interactions.
        self.can_get_hit=True
        self.hit_time=None
        self.cant_get_hit_duration=300      #This is a bit more than enemy's attack cooldown.

        #Initializing the pygame images for pointing the direction to the enemy in the level.
        self.direction2_enemy_images=[]
        self.direction2_enemy_frame=0.1
        self.direction2_enemy_animation_speed=0.5
        self.LoadDirection2EnemyImages()
        self.direction2_enemy_frames=len(self.direction2_enemy_images)

    #A method to load player UI variables
    def loadUI(self):
        self.health_bar_rect=pygame.rect.Rect(10,10,HEALTH_BAR_WIDTH,BAR_HEIGHT)
        self.health_text_surf=UI_TEXT_FONT.render("HP",True,'black')
        self.health_text_surf_pos=(self.health_bar_rect.centerx-self.health_text_surf.get_width()//2,self.health_bar_rect.centery-self.health_text_surf.get_height()//2)
        self.energy_bar_rect=pygame.rect.Rect(10,40,ENERGY_BAR_WIDTH,BAR_HEIGHT)
        self.energy_text_surf=UI_TEXT_FONT.render("MP",True,'black')
        self.energy_text_surf_pos=(self.energy_bar_rect.centerx-self.energy_text_surf.get_width()//2,self.energy_bar_rect.centery-self.energy_text_surf.get_height()//2)
        self.exp_bar_rect=pygame.rect.Rect(10,70,EXP_BAR_WIDTH,BAR_HEIGHT)
        self.exp_text_surf=UI_TEXT_FONT.render("EXP",True,'black')
        self.exp_text_surf_pos=(self.exp_bar_rect.centerx-self.exp_text_surf.get_width()//2,self.exp_bar_rect.centery-self.exp_text_surf.get_height()//2)
        self.player_level_text_surf_pos=(10,110)

    #A method to load inventory Items
    def loadInventoryItems(self):
        self.inventory_items={
            'HEALTH_POTION':[0,pygame.transform.scale_by(pygame.image.load(os.path.join(GRAPHICS_DIR_PATH,"RANDOM_LOOT","Health_Potion.png")),factor=1.5)],
            'ENERGY_POTION':[0,pygame.transform.scale_by(pygame.image.load(os.path.join(GRAPHICS_DIR_PATH,"RANDOM_LOOT","Energy_Potion.png")),factor=1.5)],
            'EXP_POTION':[0,pygame.transform.scale_by(pygame.image.load(os.path.join(GRAPHICS_DIR_PATH,"RANDOM_LOOT","Exp_Potion.png")),factor=1.5)],
            'SECRET_KEY':[0,pygame.transform.scale_by(pygame.image.load(os.path.join(GRAPHICS_DIR_PATH,"secret_key.png")),factor=2.5)],
            'INVENTORY_NUM5':[0,None]
        }
        
    #A method to load the graphics for the arrow to point to the closest enemy.
    def LoadDirection2EnemyImages(self):
        direction2_enemy_graphics_path=os.path.join(GRAPHICS_DIR_PATH,"DIRECTION2_ENEMY")
        image_file_names=os.listdir(direction2_enemy_graphics_path)
        for image_file in image_file_names:
            img_path=os.path.join(direction2_enemy_graphics_path,image_file)
            img=pygame.image.load(img_path)
            self.direction2_enemy_images.append(img)

    #A method to return the correct frame of the arrow's animations.
    def animate_arrow_and_return(self):
        self.direction2_enemy_frame+=self.direction2_enemy_animation_speed
        if(self.direction2_enemy_frame>self.direction2_enemy_frames):
            self.direction2_enemy_frame=0.1

        return self.direction2_enemy_images[int(self.direction2_enemy_frame)]

    #A method to initialize the function to create the weapon and destroy the weapon.
    def getAttackFunctions(self,createAttack,destroyAttack):
        self.createAttack=createAttack
        self.destroyAttack=destroyAttack

    #A method to initialize the function to create the magic and destroy it.
    def getMagicFunctions(self,createMagic):
        self.createMagic=createMagic
        pass

    #A method to return the total attack by combining the base attack of player(basically fist power) and the weapon power.
    def get_full_weapon_damage(self):
        base_damage=self.stats['attack']
        weapon_damage=self.GameSettings.WEAPON_INFO[self.weapon_name]['damage']
        return base_damage+weapon_damage
    
    #A method to return the total attack by magic.
    def get_full_magic_damage(self):
        base_damage=self.stats['magic']
        magic_damage=self.GameSettings.MAGIC_INFO[self.magic_name]['strength']
        return base_damage+magic_damage

    #A method to load the graphics of the players.
    def load_my_graphics(self):
        self.graphics={
            'right':[],
            'left':[],
            'up':[],
            'down':[],

            'right_idle':[],
            'left_idle':[],
            'up_idle':[],
            'down_idle':[],

            'right_attack':[],
            'left_attack':[],
            'up_attack':[],
            'down_attack':[],

            'right_magic':[],
            'left_magic':[],
            'up_magic':[],
            'down_magic':[]
        }

        for animation in self.graphics.keys():
            full_path=os.path.join(self.player_graphics_path,animation)
            files=os.listdir(full_path)
            imgs=[]
            for image_file in files:
                img=pygame.image.load(os.path.join(full_path,image_file))
                imgs.append(img)
            self.graphics[animation]=imgs

    #A helper method to simply change the status of the player as required.
    def set_status_helper(self,replace_words,replace_words_with):
        if replace_words_with in self.status:
            return
        
        for word in replace_words:
            if word in self.status:
                self.status=self.status.replace(word,replace_words_with)
                return

        self.status=self.status + '_' + replace_words_with

    #A method to set the status of the player.
    def set_status(self):
        #Idle status
        if self.direction.x==0 and self.direction.y==0:
            self.set_status_helper(['attack','magic'],'idle')

        #Attack status
        if self.attacking:
            self.set_status_helper(['idle','magic'],'attack')

        #Magic status
        if self.magicing:
            self.set_status_helper(['idle','attack'],'magic')

    #A method to set the direction of player, attack mode, magic mode etc.
    def use_controls(self,keys,level):
        #Using the normal movement controls.
        self.direction.x=0
        self.direction.y=0
        if(keys[pygame.K_w] or keys[pygame.K_UP]):
            self.direction.y=-1
            self.status='up'
        if(keys[pygame.K_s] or keys[pygame.K_DOWN]):
            self.direction.y=1
            self.status='down'
        if(keys[pygame.K_a] or keys[pygame.K_LEFT]):
            self.direction.x=-1
            self.status='left'
        if(keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            self.direction.x=1
            self.status='right'

        #Using the Attack Moves
        if(keys[pygame.K_SPACE] and not(self.attacking)):
            self.attacking=True
            self.attack_time=pygame.time.get_ticks()
            self.createAttack()
            pass

        #Switching the weapons.
        if self.can_switch_weapon:
            inc=1 if keys[pygame.K_n] else 0
            dec=-1 if keys[pygame.K_p] else 0
            if(inc==1 or dec==-1):
                self.can_switch_weapon=False
                self.weapon_switch_time=pygame.time.get_ticks()

                #Changing the weapon index to be within the range.
                self.weapon_index+=(inc+dec)
                self.weapon_index=self.weapon_index if self.weapon_index>=0 else len(self.GameSettings.WEAPON_INFO)-1
                self.weapon_index=self.weapon_index if self.weapon_index<len(self.GameSettings.WEAPON_INFO) else 0

                self.weapon_name=list(self.GameSettings.WEAPON_INFO.keys())[self.weapon_index]
                level.curr_selected_weapon=pygame.image.load(os.path.join(PLAYER_WEAPONS_DIRECTORY_PATH,f'{self.weapon_name}','full.png'))

        #Using the Magic Moves
        if(keys[pygame.K_LCTRL] and not(self.attacking) and not(self.magicing)):
            self.magicing=True
            self.magic_time=pygame.time.get_ticks()
            style=self.magic_name
            strength=self.GameSettings.MAGIC_INFO[style]['strength'] + self.stats['magic']
            cost=self.GameSettings.MAGIC_INFO[style]['cost']
            self.createMagic(style,strength,cost)

        #Switching the Magic
        if self.can_switch_magic:
            inc=1 if keys[pygame.K_m] else 0
            dec=-1 if keys[pygame.K_o] else 0
            if(inc==1 or dec==-1):
                self.can_switch_magic=False
                self.magic_switch_time=pygame.time.get_ticks()

                #Changing the weapon index to be within the range.
                self.magic_index+=(inc+dec)
                self.magic_index=self.magic_index if self.magic_index>=0 else len(self.GameSettings.MAGIC_INFO)-1
                self.magic_index=self.magic_index if self.magic_index<len(self.GameSettings.MAGIC_INFO) else 0

                self.magic_name=list(self.GameSettings.MAGIC_INFO.keys())[self.magic_index]
                level.curr_selected_magic=pygame.image.load(os.path.join(PLAYER_MAGIC_DIRECTORY_PATH,f'{self.magic_name}.png'))
        pass

    #A method to apply cooldowns on the timers used by player.
    def apply_cooldown(self):
        current_time=pygame.time.get_ticks()

        #Applying cooldown for attack
        if self.attacking:
            if current_time-self.attack_time >=self.attack_cooldown + self.GameSettings.WEAPON_INFO[self.weapon_name]['cooldown']:
                self.attacking=False
                self.destroyAttack()

        #Applying cooldown for switching weapons.
        if not self.can_switch_weapon:
            if current_time-self.weapon_switch_time >=self.weapon_switch_cooldown:
                self.can_switch_weapon=True

        #Applying cooldown for Magic
        if self.magicing:
            if current_time-self.magic_time >=self.magic_cooldown:
                self.magicing=False

        #Applying cooldown for switching magic.
        if not self.can_switch_magic:
            if current_time-self.magic_switch_time>=self.magic_switch_cooldown + self.GameSettings.MAGIC_INFO[self.magic_name]['cooldown']:
                self.can_switch_magic=True

        #Applying cooldown for the player being able to get hit.
        if not self.can_get_hit:
            if current_time-self.hit_time >=self.cant_get_hit_duration:
                self.can_get_hit=True
    
        #Apply cooldown for the player level up message being shown.
        if self.player_level_up:
            if current_time-self.player_level_up_time >=self.player_level_up_msg_duration:
                self.player_level_up=False

    #A method to check collision with loot drops.
    def chk_collision_with_randomLoot(self,loot_sprites):
        for loot in loot_sprites:
            if self.rect.colliderect(loot.rect):
                if loot.name=="Health_Potion":
                    self.inventory_items['HEALTH_POTION'][0]+=1
                    self.health_potions_vals.append(HEALTH_POTION_VAL[loot.val])
                    
                elif loot.name=="Exp_Potion":
                    self.inventory_items['EXP_POTION'][0]+=1
                    self.exp_potions_vals.append(EXP_POTION_VAL[loot.val])
                    
                elif loot.name=="Energy_Potion":
                    self.inventory_items['ENERGY_POTION'][0]+=1
                    self.energy_potions_vals.append(ENERGY_POTION_VAL[loot.val])
                    
                loot.kill()

    #A method for the player to consume potions.
    def consume_potion(self,potion_num):
        if potion_num==0 and self.inventory_items["HEALTH_POTION"][0]>0:
            self.health+=self.health_potions_vals[0]
            self.health_potions_vals.pop(0)
            self.chk_health()
            self.inventory_items["HEALTH_POTION"][0]-=1

        elif potion_num==1 and self.inventory_items["ENERGY_POTION"][0]>0:
            self.energy+=self.energy_potions_vals[0]
            self.energy_potions_vals.pop(0)
            self.chk_energy()
            self.inventory_items["ENERGY_POTION"][0]-=1

        elif potion_num==2 and self.inventory_items["EXP_POTION"][0]>0:
            self.exp+=self.exp_potions_vals[0]
            self.exp_potions_vals.pop(0)
            self.chk_exp()
            self.inventory_items["EXP_POTION"][0]-=1

    #A method to check collisions with the different sprite groups.
    def handle_collisions(self,direction, level):
        level.collision_detector.handle_spritegroup_collision(self,self.speed,direction,level.enemy_sprites,0)
        level.collision_detector.handle_spritegroup_collision(self,self.speed,direction,level.obstacle_sprites,0)
        ret_val=level.collision_detector.handle_spritegroup_collision(self,self.speed,direction,level.transport_sprites,1)
        self.chk_collision_with_randomLoot(level.loot_drops)
        if(ret_val==1):
            return ret_val
        return 0
    
    #A method to animate the player.
    def animate(self):
        animation=self.graphics[self.status]

        #Updating the frame and the image.
        if(len(animation)>0):
            self.frame_index+=self.animation_speed
            if(int(self.frame_index)>=len(animation)):
                self.frame_index=0
                
            self.img=animation[int(self.frame_index)]
            self.rect=self.img.get_rect(center=self.rect.center)

        #Flicker the player if player has been hit by decreasing/increasing alpha value of player image.
        if not self.can_get_hit:
            alpha=wave_value()
            self.img.set_alpha(alpha)
        else:
            self.img.set_alpha(255)     #This else statement is important because if the previously executed 'if' statement sets the alpha to '0', then we still have to change it to 255, else it would be transparent.

    #A method to recover some of the energy.
    def recover_energy(self):
        self.energy=self.stats['energy'] if (self.energy>=self.stats['energy']) else (self.energy+0.1*self.stats['magic'])

    #Method to move the player, animate, 
    def move(self,keys,level):
        #Gettings the controls
        self.use_controls(keys,level)

        #Settings player status.
        self.set_status()

        #Applying the cooldown
        self.apply_cooldown()

        #Moving the player
        if(self.direction.magnitude()!=0):
            self.direction=self.direction.normalize()

            #Move player horizontally and then check collisions. If player has to transport, then return '1'
            self.rect.x=self.rect.x+self.speed*self.direction.x
            shd_transport=self.handle_collisions("Horizontal",level)
            if(shd_transport==1):
                self.rect.x=self.rect.x-self.speed*self.direction.x           #Undoing movement as we have to transport. Next time we load back into this map, no collision happens.
                return shd_transport
            
            #Move player Vertically and then check collisions. If player has to transport, then return '1'.
            self.rect.y=self.rect.y+self.speed*self.direction.y
            shd_transport=self.handle_collisions("Vertical",level)
            if(shd_transport==1):
                self.rect.y=self.rect.y-self.speed*self.direction.y
                return shd_transport
            
        self.recover_energy()

        self.animate()
        pass

    #A method to draw the player(Name should have been 'draw').
    def draw(self,display_surf,offset=None):
        newpos=self.rect.topleft-self.offset
        display_surf.blit(self.img,newpos)

    #A method to display only the Bar name on the bar.
    def draw_box_bars(self,text_surf,text_surf_pos,display_surf,BOX_BG_COLOR,BAR_COLOR,BORDER_COLOR,box_rect,curr_val,max_val,BAR_WIDTH,):
        #Displaying the bar.
        pygame.draw.rect(display_surf,BOX_BG_COLOR,box_rect,0,border_radius=2)
        box_width=int((curr_val*BAR_WIDTH)//max_val)
        curr_rect=box_rect.copy()
        curr_rect.width=box_width

        #Displaying the current value.
        pygame.draw.rect(display_surf,BAR_COLOR,curr_rect,0,border_radius=2)

        #Displaying the border around the bar.
        pygame.draw.rect(display_surf,BORDER_COLOR,box_rect,2,border_radius=2)

        #Displaying the text on the bar.
        display_surf.blit(text_surf,text_surf_pos)
    
    #A method to update the exp cap as the player has hit the threshold exp.
    def update_exp_cap(self):
        self.exp_cap=int(self.exp_cap*INC_EXP_CAP)
        pass

    #A method to update the player's level if the player exp has reached the current exp threshold
    def chk_exp(self):
        if(self.exp>=self.exp_cap):
            self.player_level+=1
            self.player_level_up_time=pygame.time.get_ticks()
            self.player_level_up=True
            self.update_exp_cap()

    #A method to cap the player's health.
    def chk_health(self):
        if(self.health>self.stats['health']):
            self.health=self.stats['health']

    #A method to cap the player's energy.
    def chk_energy(self):
        if(self.energy>self.stats['energy']):
            self.energy=self.stats['energy']

    #A method to display the HP,MP,EXP.
    def display_ui(self,display_surf):
        self.chk_exp()
        self.chk_energy()
        self.chk_health()

        #Displaying the health bar.
        self.draw_box_bars(self.health_text_surf,self.health_text_surf_pos,display_surf,HEALTH_BAR_BGCOLOR,HEALTH_BAR_COLOR,HEALTH_BAR_BORDER_COLOR,self.health_bar_rect,self.health,self.stats['health'],HEALTH_BAR_WIDTH)

        #Displaying the energy bar.
        self.draw_box_bars(self.energy_text_surf,self.energy_text_surf_pos,display_surf,ENERGY_BAR_BGCOLOR,ENERGY_BAR_COLOR,ENERGY_BAR_BORDER_COLOR,self.energy_bar_rect,self.energy,self.stats['energy'],ENERGY_BAR_WIDTH)

        #Displaying the exp bar.
        self.draw_box_bars(self.exp_text_surf,self.exp_text_surf_pos,display_surf,EXP_BAR_BGCOLOR,EXP_BAR_COLOR,EXP_BAR_BORDER_COLOR,self.exp_bar_rect,self.exp,self.exp_cap,EXP_BAR_WIDTH)

        #Displaying the player level.
        text_surf=UI_TEXT_FONT.render(f'Player Level: {self.player_level}',True,'black')
        display_surf.blit(text_surf,(self.player_level_text_surf_pos))

    def saveInventoryItems(self):
        return {
            'type':'Function',
            'function_name':'loadInventoryItems'
        }
    
    def saveGraphics(self):
        return {
            'type':'Function',
            'function_name':'load_my_graphics'
        }

    #A method to make a copy of the serializable data of the player.
    def savePlayer(self):
        playerData=self.__dict__.copy()
        playerData['_Sprite__g']=None
        playerData['inventory_items']=[value[0] for value in self.inventory_items.values()]
        playerData['GameSettings']=None      #Is going to be created after reading from file and only then player should be created by passing this to the player.
        playerData['graphics']=None
        playerData['img']=None
        playerData['rect']=rect_to_dict(self.rect)
        playerData['mask']=None
        playerData['direction']=vect2_to_dict(self.direction)
        playerData['offset']=vect2_to_dict(self.offset)

        #The below 3 methods will be created in level, else you will have to handle them separately.
        playerData['createAttack']=None
        playerData['destroyAttack']=None
        playerData['createMagic']=None

        playerData['health_bar_rect']=None
        playerData['health_text_surf']=None
        playerData['energy_bar_rect']=None
        playerData['energy_text_surf']=None
        playerData['exp_bar_rect']=None
        playerData['exp_text_surf']=None

        playerData['direction2_enemy_images']=None

        return playerData

    #A method to load the player using the saved data.    
    def useSavedData(self,playerData):
        self.rect=pygame.rect.Rect(playerData['rect']['x'], playerData['rect']['y'], playerData['rect']['width'], playerData['rect']['height'])
        self.direction=pygame.math.Vector2(playerData['direction']['x'],playerData['direction']['y'])
        self.offset=pygame.math.Vector2(playerData['offset']['x'],playerData['offset']['y'])
        self.curr_selected_inventory_item_index=playerData['curr_selected_inventory_item_index']

        self.has_entered_correct_code=playerData['has_entered_correct_code']
        self.has_cleared_maps=playerData['has_cleared_maps']
        self.curr_selected_inventory_item=playerData['curr_selected_inventory_item']

        #Updating the inventory of the player.
        inventoryData=playerData['inventory_items']
        for index, value in enumerate(inventoryData):
            self.inventory_items[list(self.inventory_items.keys())[index]][0]=value

        self.health_potions_vals=playerData['health_potions_vals']
        self.exp_potions_vals=playerData['exp_potions_vals']
        self.energy_potions_vals=playerData['energy_potions_vals']

        self.status=playerData['status']

        self.weapon_index=playerData['weapon_index']
        self.weapon_name=playerData['weapon_name']

        self.magic_index=playerData['magic_index']
        self.magic_name=playerData['magic_name']

        self.health=playerData['health']
        self.energy=playerData['energy']
        self.exp=playerData['exp']
        self.exp_cap=playerData['exp_cap']

        self.speed=playerData['speed']
        self.player_level=playerData['player_level']
        
        pass