import pygame
from Settings import *
from Level import Level
from Player import Player
from LEVEL_THINGS import game_info
from LEVEL_THINGS import game_lore
import json

class Game:
    def __init__(self,clock, shd_display_game_lore=1):
        self.clock=clock
        self.GameSettings=Settings()

        #A Surface to be drawn on the screen when transitioning between different maps.
        self.shade_screen_surf=pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.transition_maps_speed=0.5
        self.opacity_val=0.1

        #Some basic variables.
        self.font=pygame.font.Font(None,32)
        display_surf=pygame.display.get_surface()
        bg_image=pygame.image.load(os.path.join(GRAPHICS_DIR_PATH,"GameStartingScreen.png"))
        
        #Displaying the game lore.
        if(shd_display_game_lore==1):
            DISPLAY_DIALOGS(game_lore,60,40,SCREEN_WIDTH-100,int(SCREEN_HEIGHT_HALF//2),bg_image)
        display_surf.blit(bg_image,(0,0))
        
        #Getting the credentaials
        if(shd_display_game_lore==1):
            information=getRequiredInfo(["Name","Age"],self.font,start_pos_y=SCREEN_HEIGHT_HALF,bg_image=bg_image,display_this_msg_and_pos=["Hover the mouse over the textbox and type the appropriate credential. Press 'Enter' or the submit button to submit the credentials.",[60,40,SCREEN_WIDTH-100,int(SCREEN_HEIGHT_HALF//2)]])
            self.GameSettings.my_Name=information[0]
            self.GameSettings.my_age=information[1]
        display_surf.blit(bg_image,(0,0))
        
        #Displaying the game info.
        if(shd_display_game_lore==1):
            DISPLAY_DIALOGS(game_info,60,40,SCREEN_WIDTH-100,int(SCREEN_HEIGHT_HALF//2),bg_image)
        display_surf.blit(bg_image,(0,0))

        #The player for the Game.
        self.player=Player(GAME_START_PLAYER_POS,self.GameSettings)

        #All the levels unlocked till now
        self.levels=[]
        self.curr_level=Level(STARTING_LEVEL_ID,self.player,self.GameSettings)
        self.levels.append(self.curr_level)

        #A timer for pause screen.
        self.esc_time_duration=100
        self.previous_esc_keydown=pygame.time.get_ticks()

        #A timer for using the portals.
        self.can_teleport=True
        self.teleport_cooldown=1000
        self.previous_teleported_time=None

    #A method to add a black shade color to the game surface, which gradually increases or decreases in opacity based on the kind of transitions.
    def transition_maps(self,transition_type,level_id=None,already_exists=None):
        SaveGameScreen()
        bg_image=LoadCurrScreen()

        display_surf=pygame.display.get_surface()
        bg_screen_pos=(0,0)

        if transition_type=="OUT OF":                                                                       #Darken the screen while on the current map.
            while self.opacity_val<=255:
                #Drawing the background image and then the shaded screen with a opacity value.
                self.shade_screen_surf.set_alpha(int(self.opacity_val))
                display_surf.blit(bg_image,bg_screen_pos)
                display_surf.blit(self.shade_screen_surf,bg_screen_pos)
                
                #Increasing the opacity value to darken the shaded screen.
                self.opacity_val+=self.transition_maps_speed
                pygame.display.flip()

        elif transition_type=="IN TO":                                                                      #Lighten the screen after changing to the next map's background image.
            #Getting the appropriate background image based on if the level has been created earlier.
            if(already_exists==1):
                bg_image=pygame.image.load(os.path.join(GRAPHICS_DIR_PATH,"TRANSITIONED_OUT_OF",f'Ruin{level_id}.png'))
            else:
                bg_image=pygame.image.load(os.path.join(GRAPHICS_DIR_PATH,"STARTSCREEN_IMAGES",f'Ruin{level_id}.png'))

            while self.opacity_val>=0:
                #Drawing the background image and then the shaded screen with a opacity value.
                self.shade_screen_surf.set_alpha(int(self.opacity_val))
                display_surf.blit(bg_image,bg_screen_pos)
                display_surf.blit(self.shade_screen_surf,bg_screen_pos)

                #Decreasing the opacity value to lighten the shaded screen.
                self.opacity_val-=self.transition_maps_speed
                pygame.display.flip()
    
    #A method to get the next level's ID to move to.
    def get_next_level_id(self):
        new_level=self.curr_level.level_id

        #The additional conditions to the inner if, elif statements are only for the purpose of readibility and could be removed(except for the first condition of 'self.player.has_entered_correct_code'). These conditional checks are already performed by the event handler method in the LEVEL_THINGS.py file.
        if self.curr_level.level_id==0:                                                         #Handling the transportation portals of Ruin0.
            if self.player.rect.colliderect(Ruin0_rect_enterCode) and self.player.has_entered_correct_code==True:
                new_level=1
            elif self.player.rect.colliderect(Ruin0_rect_Ruin2) and self.player.has_cleared_maps[1]==True:
                new_level=2
            elif self.player.rect.colliderect(Ruin0_rect_Ruin3) and self.player.has_cleared_maps[2]==True:
                new_level=3

        elif self.curr_level.level_id==1:                                                       #Handling the transportation portals of Ruin1.
            if self.player.rect.colliderect(Ruin1_rect_Ruin0) and self.player.has_cleared_maps[1]==True:
                new_level=0
            elif self.player.rect.colliderect(Ruin1_rect_Ruin1_Dummy):
                pass
            elif self.player.rect.colliderect(Ruin1_rect_Ruin1_hidden):
                pass
            
        elif self.curr_level.level_id==2:                                                       #Handling the transportation portals of Ruin2.
            if self.player.rect.colliderect(Ruin2_rect_Ruin0) and self.player.has_cleared_maps[2]==True:
                new_level=0
                pass
            elif self.player.rect.colliderect(Ruin2_rect_Ruin2_Dummy):
                pass
            elif self.player.rect.colliderect(Ruin2_rect_Ruin2_hidden):
                pass
            
        elif self.curr_level.level_id==3:                                                       #Handling the transportation portals of Ruin3.
            if self.player.rect.colliderect(Ruin3_rect_Ruin0) and self.player.has_cleared_maps[3]==True:
                new_level=0
            elif self.player.rect.colliderect(Ruin3_rect_Ruin3_hidden):
                pass

        return new_level

    #A method to change to the next map.
    def changeMap(self):
        new_level_id=self.get_next_level_id()
        if(new_level_id==self.curr_level.level_id):
            return
        
        self.transition_maps("OUT OF")

        #Storing the previously selected magic, weapon so that they can be the actively selected weapon, magic in the next level.
        curr_level_selected_weapon=self.curr_level.curr_selected_weapon
        curr_level_selected_magic=self.curr_level.curr_selected_magic

        #Checking if the next level has previously been created or not.
        for level in self.levels:
            if level.level_id == new_level_id:
                self.curr_level=level
                self.player.rect.topleft=self.curr_level.player_pos
                self.curr_level.curr_selected_weapon=curr_level_selected_weapon
                self.curr_level.curr_selected_magic=curr_level_selected_magic

                #Passing the player, the create and destroy functions for attack,magic which are specific to the level. Without these, the attacks would work on only the recently created level.
                self.player.getAttackFunctions(self.curr_level.create_attack,self.curr_level.destroy_attack)
                self.player.getMagicFunctions(self.curr_level.create_magic)

                self.transition_maps("IN TO",self.curr_level.level_id,already_exists=1)
                return
        
        #Creating a new level as the level has not been created yet.
        self.curr_level=Level(new_level_id,self.player,self.GameSettings)
            #Using the previously selected weapon and magic as the default ones to be displayed.
        self.curr_level.curr_selected_weapon=curr_level_selected_weapon
        self.curr_level.curr_selected_magic=curr_level_selected_magic
            #Adding the newly created levels to the list of levels in the curr game.
        self.levels.append(self.curr_level)

        #Transitioning into the new map and then displaying it's start message.
        self.transition_maps("IN TO",self.curr_level.level_id)
        self.curr_level.DisplayLevelStartMessages()

    #A method to apply cooldown for all the timers(currently only for teleportation) used by the game.
    def apply_cooldown(self):
        curr_time=pygame.time.get_ticks()
        if self.can_teleport==False:
            if curr_time-self.previous_teleported_time>=self.teleport_cooldown:
                self.can_teleport=True

    #Game logic.
    def run(self,previous_esc_time):
        running=True
        while running:
            #The basic event loop to run the game.
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    running=False
                    pygame.quit()
                    sys.exit()

                if event.type==pygame.KEYDOWN:

                    if event.key==pygame.K_g:                                                   #Display the Dialog logs if 'g' is pressed on the keyboard.
                        #Saving the current gamescreen to be used as the background image.
                        SaveGameScreen()
                        bg_image=LoadCurrScreen()
                        dialog_num=DisplayDialogHistory(bg_image)

                        #Displaying the chosen dialog.
                        if(dialog_num==None):
                            pass
                        elif (dialog_num=="QUIT"):
                            pygame.quit()
                            sys.exit()
                        else:
                            DISPLAY_DIALOGS(DIALOG_LOGS[dialog_num],60,40,SCREEN_WIDTH-100,SCREEN_HEIGHT-100,bg_image=bg_image,shd_log_dialogs=False)
                        break

                    if self.player.curr_selected_inventory_item_index!=None:                    #Updating the selected item in inventory box.
                        #Changing the index of selected item.
                        has_changed_selection=False
                        if event.key==pygame.K_t:
                            self.player.curr_selected_inventory_item_index-=1
                            has_changed_selection=True
                        if event.key==pygame.K_y:
                            self.player.curr_selected_inventory_item_index+=1
                            has_changed_selection=True
                        
                        #Capping the selected index to within the number of item boxes in inventory boxes.
                        if self.player.curr_selected_inventory_item_index<0:
                            self.player.curr_selected_inventory_item_index=self.player.inventory_boxes_num
                        elif self.player.curr_selected_inventory_item_index>self.player.inventory_boxes_num:
                            self.player.curr_selected_inventory_item_index=0

                        #Changing the selection values of items in the inventory if the selected item has been changed.
                        if(has_changed_selection):
                            for index,key in enumerate(list(self.player.inventory_items.keys())):
                                if index==self.player.curr_selected_inventory_item_index:
                                    self.player.curr_selected_inventory_item[key]=True
                                else:
                                    self.player.curr_selected_inventory_item[key]=False
                                
                    if event.key==pygame.K_v:                                                   #Selecting, De-selecting the inventory box.
                        self.player.curr_selected_inventory_item_index=0 if self.player.curr_selected_inventory_item_index==None else None
                        if self.player.curr_selected_inventory_item_index==None:
                            for index, key in enumerate(list(self.player.inventory_items.keys())):
                                self.player.curr_selected_inventory_item[key]=False
                        else:
                            self.player.curr_selected_inventory_item["HEALTH_POTION"]=True                      #This item(the first item) is selected by default.

                    if event.key==pygame.K_e:                                                   #Consuming the potions available to the player.
                        #If the selected index is the index of one of the potions(in range[0,2]), then the player can consume the potion.
                        if self.player.curr_selected_inventory_item_index!=None and self.player.curr_selected_inventory_item_index>=0 and self.player.curr_selected_inventory_item_index<=2:
                            self.player.consume_potion(self.player.curr_selected_inventory_item_index)

            if(running==False):
                break
            
            #Getting the mouse Keys
            keys=pygame.key.get_pressed()
            if(keys[pygame.K_ESCAPE] and pygame.time.get_ticks()-previous_esc_time>=500):          #Pause screen has to be visible if the user hits 'esc'
                SaveGameScreen()
                return "Pause"
            
            #Running the Level logic.
            if(self.curr_level.has_displayed_level_start_msg==False):
                self.curr_level.DisplayLevelStartMessages()
            ret_val=self.curr_level.run(keys)

            #Updating the screen.
            pygame.display.flip()
            self.apply_cooldown()

            if(ret_val==1):     #Changing the map.
                if self.can_teleport:
                    self.previous_teleported_time=pygame.time.get_ticks()
                    self.can_teleport=False
                    self.changeMap()
                    
            elif(ret_val==10):
                return "Lose"
            
            elif(ret_val==11):
                return "Victory"
            
            self.clock.tick(self.GameSettings.GAME_FPS)

    def saveLevels(self):
        saveLevels=[]
        for level in self.levels:
            saveLevels.append(level.saveLevel())
        return saveLevels

    #Method to save the Game.
    def saveGame(self):
        gameData=self.__dict__.copy()

        #Making the non-serializable attributes to be None.
        gameData['clock']=None
        gameData['GameSettings']=self.GameSettings.saveSettings()
        gameData['shade_screen_surf']=None
        gameData['font']=font_to_dict(self.font)
        gameData['player']=self.player.savePlayer()
        gameData['levels']=self.saveLevels()
        gameData['curr_level']=self.curr_level.level_id
        return gameData
    