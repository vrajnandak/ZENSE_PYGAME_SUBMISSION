import pygame
from Settings import *
from pathfinding.core.grid import Grid

class Enemy(pygame.sprite.Sprite):
    def __init__(self,pos,zombieType,groups):
        super().__init__(groups)
        self.pos=pos

        self.graphics_path=os.path.join(GRAPHICS_DIR_PATH,"Enemy",zombieType)
        self.load_graphics()

        #Animation variables.
        self.status='idle'
        self.frame_index=0.1
        self.animation_speed=0.5
        self.img=self.graphics[self.status][int(self.frame_index)]
        self.mask=pygame.mask.from_surface(self.img)        #This will be used by the player for collision detection.
        self.rect=self.img.get_rect(topleft=self.pos)

        #Enemy Dimensions - Used for updating the tiles
        self.width_tiles=int(self.rect.width//BASE_SIZE)
        self.height_tiles=int(self.rect.height//BASE_SIZE)

        #Movement Variables.
        self.direction=pygame.math.Vector2()

        self.zombieType=zombieType

        #Getting the index of the zombie type from the dictionary in the Settings.py file.
        self.attack_radius=BASE_SIZE*(ZOMBIE_ENEMIES_INFO[zombieType]['attack_radius'])
        self.notice_radius=BASE_SIZE*(ZOMBIE_ENEMIES_INFO[zombieType]['notice_radius'])
        self.attack_type=ZOMBIE_ENEMIES_INFO[zombieType]['attack_type']
        self.exp_gained_on_killing=ZOMBIE_ENEMIES_INFO[zombieType]['exp']

        #The max size of the submatrix, centered around self( i.e., enemy sprite).
        self.SUBMATRIX_SIZE=12
        self.SUBMATRIX_HALF_SIZE=int(self.SUBMATRIX_SIZE//2)

        #Enemy UI.
        self.max_health=ZOMBIE_ENEMIES_INFO[zombieType]['health']
        self.health=ZOMBIE_ENEMIES_INFO[zombieType]['health']
        self.attack_power=ZOMBIE_ENEMIES_INFO[zombieType]['damage']
        self.resistance=ZOMBIE_ENEMIES_INFO[zombieType]['resistance']
        self.speed=ZOMBIE_ENEMIES_INFO[zombieType]['speed']

        #Player interaction
        self.attack_cooldown=200
        self.can_attack=True
        self.attack_time=None

        #Timer variables for enemy getting hit only once when player is in attack mode.
        self.hit_time=None
        self.can_get_hit=True
        self.cant_get_hit_duration=700          #Putting this to be more than that of player.attack_cooldown so that the enemy gets hit only once everytime the player attacks.

    def load_graphics(self):
        self.graphics={
            'idle':[],
            'move':[],
            'attack':[]
        }

        animation_names=os.listdir(self.graphics_path)
        for animation_name in animation_names:
            animation_path=os.path.join(self.graphics_path,animation_name)
            image_file_names=os.listdir(animation_path)
            imgs=[]
            for image_file_name in image_file_names:
                img=pygame.image.load(os.path.join(animation_path,image_file_name))
                imgs.append(img)
            self.graphics[animation_name]=imgs

    def update_direction(self,player,level):
        #The default direction of the enemy.
        self.direction.x=player.rect.centerx-self.rect.centerx
        self.direction.y=player.rect.centery-self.rect.centery
        
        #Making the grid(A small submatrix of the level's matrix), centered about the enemy sprite. There is no need to do a grid.cleanup() as we create a new grid each time.
        small_submatrix=[]
        start_row=max(0,int((self.rect.y//BASE_SIZE)-self.SUBMATRIX_HALF_SIZE))
        end_row=min(len(level.detection_tiles),start_row+self.SUBMATRIX_SIZE)
        start_col=max(0,int((self.rect.x//BASE_SIZE)-self.SUBMATRIX_HALF_SIZE))
        end_col=min(len(level.detection_tiles[0]), start_col+self.SUBMATRIX_SIZE)
        for i in range(start_row,end_row,1):
            submatrix_row=level.detection_tiles[i][start_col:end_col]
            small_submatrix.append(submatrix_row)
        grid=Grid(matrix=small_submatrix)

        #Finding the start and end cells.
        start_x=int(self.rect.x//BASE_SIZE)-start_col
        start_y=int(self.rect.y//BASE_SIZE)-start_row
        
        end_x=min(max(int(player.rect.x//BASE_SIZE)-start_col, 0),end_col-start_col-1)
        end_y=min(max(int(player.rect.y//BASE_SIZE)-start_row, 0),end_row-start_row-1)
        start_cell=grid.node(start_x,start_y)
        end_cell=grid.node(end_x,end_y)
        
        #Finding the path to the player and updating the direction of the enemy sprite.
        path,runs=level.finder.find_path(start_cell,end_cell,grid)
        if(len(path)>2):
            next_cell=path[1]       #This cell contains the indices in the submatrix, so we find the actual position in map. BASE_SIZE//2 is added to give a bit of diagonal movement.
            next_cell_col=(start_col+next_cell.x)*BASE_SIZE + BASE_SIZE//2
            next_cell_row=(start_row+next_cell.y)*BASE_SIZE + BASE_SIZE//2
            
            self.direction.x=next_cell_col-self.rect.x
            self.direction.y=next_cell_row-self.rect.y
    
    #A method to handle the collisions of the enemy(self) with other obstacles.
    def handle_collisions(self,direction,level):
        ret_val1=level.collision_detector.handle_spritegroup_collision(self,self.speed,direction,level.transport_sprites,1,collision_type="rect_collision")
        ret_val2=level.collision_detector.handle_spritegroup_collision(self,self.speed,direction,level.obstacle_sprites,0,collision_type="rect_collision")
        ret_val3=level.collision_detector.handle_spritegroup_collision(self,self.speed,direction,level.enemy_sprites,0,collision_type="rect_collision")
        ret_val4=level.collision_detector.handle_spritegroup_collision(self,self.speed,direction,[level.player],0,collision_type="rect_collision")
        if(ret_val3==1):
            return 1
        elif(ret_val1==2 or ret_val2==2 or ret_val3==2 or ret_val4==2):
            return 2
        else:
            return 0

    def reduce_health(self,player,is_weapon):
        if(self.can_get_hit):
            self.can_get_hit=False
            self.hit_time=pygame.time.get_ticks()
            if(is_weapon):
                self.health-=player.get_full_weapon_damage()
            else:
                self.health-=player.get_full_magic_damage()
                pass
            if(self.chk_death()==1):
                player.exp+=self.exp_gained_on_killing
                return 1
            
        return 0
        pass
    def chk_death(self):
        if self.health<=0:
            self.kill()
            return 1
        return 0

    #A method to apply the cooldowns on the enemy
    def apply_cooldowns(self):
        curr_time=pygame.time.get_ticks()
        #If it has been a while since the last animation has been played, then the enemy can attack.
        if not self.can_attack:
            if curr_time-self.attack_time >=self.attack_cooldown:
                self.can_attack=True

        #If it has been a while since the last time the enemy got hit, then we can update the attribute to be able to get hit.
        if not self.can_get_hit:
            if curr_time-self.hit_time >=self.cant_get_hit_duration:
                self.can_get_hit=True

    #A method to animate the enemy sprite.
    def animate(self):
        #Updating the animation.
        self.frame_index+=self.animation_speed
        if(self.frame_index>=len(self.graphics[self.status])):
            if self.status=='attack':           #We want to complete the animation of attack. So we wait until the last frame has been played for the attack.
                self.can_attack=False
            self.frame_index=0
        self.img=self.graphics[self.status][int(self.frame_index)]
        self.rect=self.img.get_rect(center=self.rect.center)

        if not self.can_get_hit:
            #Flicker animation for the enemy sprite.
            alpha=wave_value()
            self.img.set_alpha(alpha)
            pass
        else:
            self.img.set_alpha(255)

    def update(self,display_surf,offset,level):
        self.speed=level.GameSettings.ENEMY_SPEED

        #Moving the enemy sprite if player within notice range.
        player_enemy_distance=pygame.math.Vector2(level.player.rect.left-self.rect.left, level.player.rect.top-self.rect.top).magnitude()
        if(player_enemy_distance<=self.notice_radius):
            self.update_direction(level.player,level)
            self.status='move'

            if not self.can_get_hit:
                self.can_apply_resistance=False
                self.resistance_applied_time=pygame.time.get_ticks()
                self.direction*=-self.resistance


            if(self.direction.magnitude()!=0):
                self.direction=self.direction.normalize()
            self.rect.x+=self.direction.x*self.speed
            self.handle_collisions("Horizontal",level)
            self.rect.y+=self.direction.y*self.speed
            self.handle_collisions("Vertical",level)
            
        else:
            self.direction.x=0
            self.direction.y=0
        if(player_enemy_distance<=self.attack_radius and self.can_attack):
            self.frame_index=0
            self.status='attack'
            
            self.attack_time=pygame.time.get_ticks()
            level.damage_the_player(self.attack_power,self.attack_type)
        if(self.direction.x==0 and self.direction.y==0):
            self.status='idle'
        
        self.animate()
        self.apply_cooldowns()

        self.draw(display_surf,offset)
        pass

    def draw_health_bar(self,display_surf,offset):
        newpos=self.rect.topleft-offset - pygame.math.Vector2(0,20)
        if(self.rect.width!=BASE_SIZE):
            newpos.x+=(self.rect.width//4)                  #This is to center the health bar position on top of the enemy sprite. As 'zombie1' has dimensions 64x64, we use this else it is not needed and can be commented.
        health_rect=pygame.rect.Rect(newpos[0],newpos[1],BASE_SIZE,10)
        pygame.draw.rect(display_surf,HEALTH_BAR_BGCOLOR,health_rect,0,border_radius=2)
        pygame.draw.rect(display_surf,HEALTH_BAR_BORDER_COLOR, health_rect,1,border_radius=2)

        curr_width=int((self.health*BASE_SIZE)//self.max_health)
        present_health_rect=pygame.rect.Rect(newpos[0],newpos[1],curr_width,10)
        pygame.draw.rect(display_surf,'red', present_health_rect,0,border_radius=2)

    def draw(self,display_surf,offset):
        newpos=self.rect.topleft-offset
        display_surf.blit(self.img,newpos)
        self.draw_health_bar(display_surf,offset)

    #A method to load the enemy using the saved data.
    def useSavedData(self, enemyData):
        self.status=enemyData['status']
        self.frame_index=enemyData['frame_index']
        self.rect=pygame.rect.Rect(enemyData['rect']['x'],enemyData['rect']['y'],enemyData['rect']['width'],enemyData['rect']['height'])
        self.direction=pygame.math.Vector2(enemyData['direction']['x'],enemyData['direction']['y'])
        self.health=enemyData['health']
        pass