import sys
from Settings import *
from Game import *
from Button import Button
from LoadDataManager import *


class MyGame:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        #Checking if there is a game screen that exists already. Delete it if it already exists.
        self.path_to_start_screen=os.path.join(GRAPHICS_DIR_PATH,"GameStartingScreen.png")
        self.start_screen_img=pygame.image.load(self.path_to_start_screen)
        self.path_to_curr_screen=os.path.join(GRAPHICS_DIR_PATH,"Curr_Screen.png")
        self.path_to_screen_img=self.path_to_start_screen
        self.using_saved_game=0

        #Game's clock,settings,font
        self.clock=pygame.time.Clock()
        self.gui_font=pygame.font.Font(None, 30)

        #Game screen.
        self.screen=pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(GAME_TITLE)

        #Buttons. Every screen has different buttons due to having different positions in the screen(we could also manually change the positions of the buttons and their animation phases, since it leads to complexity I decided to just create new Buttons). We could've otherwise re-used the same buttons.
            #Start Screen - "New Game","Saved Games", "Quit", "Settings"
        self.startNewGame=Button((200,100),200,60,"New Game",self.gui_font,-200)
        self.startSavedGames=Button((400,200),200,60,"Saved Games", self.gui_font,-300)
        self.startQuit=Button((600,300),200,60,"Quit",self.gui_font,-400)
        self.startSettings=Button((800,400),200,60,"Settings",self.gui_font,-500)
        self.StartButtons=[self.startNewGame,self.startSavedGames,self.startQuit,self.startSettings]
            #Pause Screen - "Resume", "Save", "Quit", "Settings", "Back To Home", "Restart"
        self.pauseResume=Button((200,100),200,60,"Resume",self.gui_font,-100)
        self.pauseSave=Button((200,250),200,60,"Save", self.gui_font,-200)
        self.pauseQuit=Button((200,400),200,60,"Quit",self.gui_font,-300)
        self.pauseSettings=Button((800,100),200,60,"Settings",self.gui_font,-100)
        self.pauseBackToHome=Button((800,250),200,60,"Back To Home",self.gui_font,-200)
        self.pauseRestart=Button((800,400),200,60,"Restart", self.gui_font,-300)
        self.PauseButtons=[self.pauseResume,self.pauseSave,self.pauseQuit,self.pauseSettings,self.pauseBackToHome,self.pauseRestart]
            #Settings Screen - "Resume","Back to home", "Reset Settings", "Apply Changes"
        self.settingsResume=Button((80,100),200,60,"Resume",self.gui_font,-100)
        self.settingsBackToHome=Button((300,100),200,60,"Back To Home",self.gui_font,-200)
        self.settingsResetSettings=Button((520,100),200,60,"Reset Settings", self.gui_font,-300)
        self.settingsApplyChanges=Button((740,100),200,60,"Apply Changes",self.gui_font,-400)
        self.SettingsButtons=[self.settingsResume,self.settingsBackToHome,self.settingsResetSettings,self.settingsApplyChanges]
        self.scroll_settings_screen=0
        self.accumulated_scroll=0
        self.SETTINGS_SCREEN_TOP=0
        self.SETTINGS_SCREEN_BOTTOM=-SCREEN_HEIGHT+120
            #Victory Or Loss Screen Buttons - "Play Again", "Quit"
        text_font=pygame.font.FontType(None,60)
        self.victory_text_surf=text_font.render("You Have WON!!!", True, 60)
        self.lose_text_surf=text_font.render("You Have LOST!!",True,60)
        self.victory_or_lose_pos=(SCREEN_WIDTH_HALF-self.victory_text_surf.get_width()//2,100)
        self.score_pos=(SCREEN_WIDTH_HALF-80,250)
        self.victory_or_loss_PlayAgain=Button((SCREEN_WIDTH_HALF-120,SCREEN_HEIGHT_HALF-100),200,60,"Play Again",self.gui_font,-100)
        self.victory_or_loss_Quit=Button((SCREEN_WIDTH_HALF-120,((3*SCREEN_HEIGHT)//4)-100),200,60,"Quit",self.gui_font,-100)
        self.victory_or_lose="Lose"
        self.Victory_or_lossButtons=[self.victory_or_loss_PlayAgain,self.victory_or_loss_Quit]
            #Are you sure you want to Quit Screen - "Yes", "No"
        self.AreYouSureYouWantToQuit_text=text_font.render("Are you sure you want to Quit?", True,60)
        self.AreYouSureYouWantToQuit_pos=(SCREEN_WIDTH_HALF-self.AreYouSureYouWantToQuit_text.get_width()//2, int(SCREEN_HEIGHT_HALF//2)-self.AreYouSureYouWantToQuit_text.get_height())
        self.AreYouSureYouWantToQuitYes=Button((400,SCREEN_HEIGHT_HALF),200,60,"Yes",self.gui_font,-200)
        self.AreYouSureYouWantToQuitNo=Button((700,SCREEN_HEIGHT_HALF),200,60,"No",self.gui_font,-200)
        self.AreYouSureYouWantToQuitButtons=[self.AreYouSureYouWantToQuitYes,self.AreYouSureYouWantToQuitNo]

        #The Games available.
        self.curr_Game=None
        self.savedGames=[]
        self.gameDataManager=LoadDataManager()

        #Starting the Code.
        self.display_text_also=""
        self.curr_screen="Start"         #Can be ["Start","Pause","Settings","Victory","Loss","AreYouSureYouWantToQuit"]
        self.curr_buttons=self.StartButtons
        self.screen_shade_color=SCREEN_BG_SHAD_POS
        self.action=None                 #Can be ["New Game", "Saved Games","Quit","Settings","Resume","Save","Back To Home","Restart", "Yes","No"]
        self.previous_esc_applied=pygame.time.get_ticks()
        self.startGame()

    #Method to choose which buttons to be displayed based on curr screen.
    def chooseWhichButtons(self):
        self.victory_or_lose=""
        if(self.curr_screen=="Start"):
            self.curr_buttons=self.StartButtons
            self.screen_shade_color=SCREEN_BG_DARK_COLOR
        elif(self.curr_screen=="Pause"):
            self.path_to_screen_img=self.path_to_curr_screen
            self.curr_buttons=self.PauseButtons
            self.screen_shade_color=SCREEN_BG_SHADE_COLOR
        elif(self.curr_screen=="Settings"):
            self.curr_buttons=self.SettingsButtons
            self.screen_shade_color=SCREEN_BG_DARK_COLOR
        elif(self.curr_screen=="Victory"):
            self.path_to_screen_img=self.path_to_curr_screen
            self.curr_buttons=self.Victory_or_lossButtons
            self.victory_or_lose="Victory"
            self.screen_shade_color=SCREEN_BG_SHADE_COLOR
        elif(self.curr_screen=="Lose"):
            self.path_to_screen_img=self.path_to_curr_screen
            self.curr_buttons=self.Victory_or_lossButtons
            self.victory_or_lose="Lose"
            self.screen_shade_color=SCREEN_BG_SHADE_COLOR
        elif(self.curr_screen=="AreYouSureYouWantToQuit"):
            self.curr_buttons=self.AreYouSureYouWantToQuitButtons
            self.screen_shade_color=SCREEN_BG_SHADE_COLOR

    #A method to reset the animation states of the buttons.
    def Reset_button_animations(self,buttons):
        for button in buttons:
            button.animation_phase=1
            button.curr_left=button.start_left_pos

    #A method to clamp the scroll settings variable so that the page doesn't scroll out of bounds
    def configure_scroll_settings_screen(self):
        if self.accumulated_scroll>self.SETTINGS_SCREEN_TOP:
            self.accumulated_scroll-=self.scroll_settings_screen
            self.scroll_settings_screen=0
        elif self.accumulated_scroll<self.SETTINGS_SCREEN_BOTTOM:
            self.accumulated_scroll-=self.scroll_settings_screen
            self.scroll_settings_screen=0

    #A method to display the given screen. Returns the text of the button on which the mouse is released on.
    def displayScreen(self,screen_bg_shade,buttons):
        #Getting the game screen
        gameScreen=self.start_screen_img
        if(self.path_to_screen_img!=self.path_to_start_screen and os.path.isfile(self.path_to_screen_img)):
            gameScreen=pygame.image.load(self.path_to_screen_img)
        if(self.using_saved_game):
            self.using_saved_game=0
            # gameScreen=LoadCurrScreen()
            gameScreen=pygame.image.load(os.path.join(GRAPHICS_DIR_PATH,"STARTSCREEN_IMAGES",f'Ruin{self.curr_Game.curr_level.level_id}.png'))
            pass

        running=True
        while running:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEWHEEL:                                                     #Scrolling the settings screen.
                    if (self.curr_screen=="Settings"):
                        self.scroll_settings_screen=event.y*SCROLL_SETTINGS_SPEED
                        self.accumulated_scroll+=self.scroll_settings_screen

                if(event.type==pygame.KEYDOWN):                                                         #Pausing the game by pressing 'esc'
                    if event.key==pygame.K_ESCAPE and self.curr_screen=="Pause":
                        self.previous_esc_applied=pygame.time.get_ticks()
                        self.Reset_button_animations(buttons)
                        return "Resume"

                if event.type==pygame.MOUSEBUTTONUP and event.button==1:                                #To indicate a left button release on mouse. The selected button's text is returned accordingly.
                    mouse_pos=pygame.mouse.get_pos()
                    for button in buttons:
                        if(button.bottom_rect.collidepoint(mouse_pos)):
                            self.Reset_button_animations(buttons)

                            if self.curr_Game==None:
                                if button.text=="Resume" or button.text=="Settings" or button.text=="Apply Changes":    #Not possible to resume, view settings, apply changes when you've not loaded into a game.
                                    return "NOT POSSIBLE"
                                else:
                                    return button.text
                            else:
                                if button.text=="Apply Changes":                                                        #Applying changes(selected in the settings page) to the game.
                                    self.curr_Game.GameSettings.apply_changes(self.curr_Game)
                                else:                                                                                   #Returning the button selected.
                                    return button.text
            
            self.configure_scroll_settings_screen()
            self.screen.blit(gameScreen,(0,0))
                
            #Displaying the text(if any with the curr screen).
            if self.victory_or_lose=="Lose":
                self.screen.blit(self.lose_text_surf,self.victory_or_lose_pos)
            elif self.victory_or_lose=="Victory":
                self.screen.blit(self.victory_text_surf,self.victory_or_lose_pos)
                self.screen.blit(self.gui_font.render(f'Your Score: {self.curr_Game.curr_level.timer[0]+100+self.curr_Game.curr_level.timer[1]*12}',False,'black'), self.score_pos)
            elif self.curr_screen=="AreYouSureYouWantToQuit":
                self.screen.blit(self.AreYouSureYouWantToQuit_text,self.AreYouSureYouWantToQuit_pos)

            #Displaying the buttons.
            for button in buttons:
                button.update(self.screen,self.scroll_settings_screen)

            #Displaying the settings buttons if the curr screen is settings.
            if(self.curr_screen=="Settings"):
                if(self.curr_Game!=None):
                    self.curr_Game.GameSettings.display_settings(self.screen,self.curr_Game,can_change_values=1,scroll_settings_screen=self.scroll_settings_screen)
                else:
                    return "NOT POSSIBLE"
            
            #Reset scroll.
            self.scroll_settings_screen=0

            pygame.display.flip()

        if(self.curr_buttons!=None):
            self.Reset_button_animations(self.curr_buttons)
        return "NOT POSSIBLE"
    
    def DisplaySavedGames(self,saved_games_list):
        SaveGameScreen()
        # bg_image=LoadCurrScreen()
        bg_image=pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
        bg_image.fill('black')
        display_surf=pygame.display.get_surface()
        
        rectangles=[]
        surfs=[]
        for index,saved_game in enumerate(saved_games_list):
            #Creating the surfaces.
            saved_game_surf=pygame.Surface((SCREEN_WIDTH-100,60),pygame.SRCALPHA)
            saved_games_screen=pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
            DISPLAY_MSG(f'Name: {saved_game[0]}, Age: {saved_game[1]}', 60,40, SCREEN_WIDTH-100, 60, shd_do_next_msg_prompt=False, is_first_msg=False, display_surf=saved_games_screen)
            saved_game_surf.blit(saved_games_screen,(-60,-40))
            surfs.append(saved_game_surf)

            #Creating the rectangles for the surfaces.
            collideRect=pygame.rect.Rect(60,40+100+index*(60+20),SCREEN_WIDTH-100,60)
            rectangles.append(collideRect)
            pass

        back_to_home_button_text_surf=pygame.font.Font(None,30).render("Back",True,'black')
        back_to_home_rect=pygame.rect.Rect(int(SCREEN_WIDTH_HALF//2),50,int(back_to_home_button_text_surf.get_width()+20),int(back_to_home_button_text_surf.get_height()+20))

        quit_button_text_surf=pygame.font.Font(None,30).render("Quit", True,'black')
        quit_button_rect=pygame.rect.Rect(int((3*SCREEN_WIDTH)//4),50,int(quit_button_text_surf.get_width()+20),int(quit_button_text_surf.get_height()+20))
        
        scroll_settings_screen=0
        accumulated_scroll=0
        SETTINGS_SCREEN_TOP=0
        SETTINGS_SCREEN_BOTTOM=-rectangles[len(rectangles)-1].top + int((3*SCREEN_HEIGHT)//4)

        while True:
            scroll_settings_screen=0
            # print('inside the ')
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEWHEEL:
                    scroll_settings_screen=event.y*SCROLL_SETTINGS_SPEED
                    accumulated_scroll+=scroll_settings_screen

                if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                    mouse_pos=pygame.mouse.get_pos()
                    for index,rect in enumerate(rectangles):
                        if rect.collidepoint(mouse_pos):
                            return index
                    
                    if back_to_home_rect.collidepoint(mouse_pos):
                        return "Back To Home"
                    
                    if quit_button_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
            
            if accumulated_scroll>SETTINGS_SCREEN_TOP:
                accumulated_scroll-=scroll_settings_screen
                scroll_settings_screen=0
            elif accumulated_scroll<SETTINGS_SCREEN_BOTTOM:
                accumulated_scroll-=scroll_settings_screen
                scroll_settings_screen=0

            back_to_home_rect.y+=scroll_settings_screen
            quit_button_rect.y+=scroll_settings_screen
            for rectangle in rectangles:
                rectangle.y+=scroll_settings_screen

            display_surf.blit(bg_image, (0,0))

            pygame.draw.rect(display_surf,'white',back_to_home_rect,0,3)
            display_surf.blit(back_to_home_button_text_surf,(back_to_home_rect.centerx-back_to_home_button_text_surf.get_width()//2, back_to_home_rect.centery-back_to_home_button_text_surf.get_height()//2))

            pygame.draw.rect(display_surf,'white',quit_button_rect,0,3)
            display_surf.blit(quit_button_text_surf,(quit_button_rect.centerx-quit_button_text_surf.get_width()//2, quit_button_rect.centery-quit_button_text_surf.get_height()//2))
            for index,surf in enumerate(surfs):
                #Display the surfaces.
                display_surf.blit(surf,rectangles[index])
                # pass

            pygame.display.flip()

    #A method to load one of the saved games.
    def LoadTheGame(self,folderName):
        folderPath=os.path.join(os.getcwd(),"SAVED_GAMES",folderName)
        print('folderPath: ', folderPath)
        # print('path:', os.path.join(folderPath,"Settings.json"))

        #Loading all the files.
            #Loading the Game Settings variable.
        GameSettings=Settings()
        with open(os.path.join(folderPath,"Settings.json"), 'r') as f:
            gameSettings=json.load(f)
            GameSettings.useSavedData(gameSettings)
        print('GameSettings: ', GameSettings)

            #Loading the Player.
        GamePlayer=Player(GAME_START_PLAYER_POS,GameSettings)
        with open(os.path.join(folderPath,"Player.json"),'r') as f:
            gamePlayer=json.load(f)
            GamePlayer.useSavedData(gamePlayer)
        orig_player_pos=GamePlayer.rect.topleft
        print('GamePlayer: ', GamePlayer)

            #Loading the Levels.
        GameLevels=[]
        levelFilePath=os.path.join(folderPath, "levels")
        fileList=os.listdir(levelFilePath)
        for filename in fileList:
            with open(os.path.join(levelFilePath,filename), 'r') as f:
                levelData=json.load(f)
                newLevel=Level(levelData['level_id'], GamePlayer, GameSettings)
                newLevel.useSavedData(levelData)
                if(newLevel.level_scientist!=None and newLevel.level_scientist.shd_escape_from_ruin):
                    newLevel.level_scientist.initialize_escape_path(newLevel)
                GameLevels.append(newLevel)
                print('GameLevel: ', newLevel)
            
            #Loading the game.
        newGame=Game(self.clock, shd_display_game_lore=0)
        newGame.GameSettings=GameSettings
        newGame.player=GamePlayer
        newGame.levels=GameLevels
        with open(os.path.join(folderPath,"game.json"), 'r') as f:
            savedGameData=json.load(f)
            #Using the saved data to change some of the attribute values.
            curr_level_id=savedGameData['curr_level']
            for level in GameLevels:
                if level.level_id==curr_level_id:
                    newGame.curr_level=level
                    break

            #Loading the curr level's attack and weapon functions to the player.
        GamePlayer.getAttackFunctions(newGame.curr_level.create_attack, newGame.curr_level.destroy_attack)
        GamePlayer.getMagicFunctions(newGame.curr_level.create_magic)
        GamePlayer.rect.x=orig_player_pos[0]
        GamePlayer.rect.y=orig_player_pos[1]

            #Loading the Dialog Logs.
        DialogData=None
        with open(os.path.join(folderPath,"DIALOG_LOGS.json"), 'r') as f:
            DialogData=json.load(f)
        ClearDialogHistory()
        for dialog in DialogData:
            AddDialogToLogs(dialog)
        self.curr_Game=newGame
        self.using_saved_game=1
    
    #A method to display the Starting Screen.
    def startGame(self):
        #The main event loop.
        running=True
        while running:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    running=False

            if(running==False):
                break

            
            #Displaying the appropriate screen after Choosing the required buttons based on current game state.
            self.chooseWhichButtons()
            self.action=self.displayScreen(self.screen_shade_color,self.curr_buttons)

            #Performing the Actions.
            if(self.action=="Resume"):
                self.curr_screen=self.curr_Game.run(self.previous_esc_applied)       #Returns either of ["Pause","Victory","Lose","Quit"]

            elif(self.action=="New Game"):
                self.saveCurrentGame()
                ClearDialogHistory()
                newGame=Game(self.clock)
                self.curr_Game=newGame
                self.curr_screen=self.curr_Game.run(self.previous_esc_applied)

            elif(self.action=="Saved Games"):
                saved_games_list=self.gameDataManager.savedGamesInfo()
                if(len(saved_games_list)>0):
                    # print('there are saved games', saved_games_list)
                    ret_val=self.DisplaySavedGames(saved_games_list)
                    if(ret_val=="Back To Home"):
                        self.curr_screen="Start"
                        pass
                    else:
                        #Load the selected game.
                        folderName=f'{saved_games_list[ret_val][0]}_{saved_games_list[ret_val][1]}'
                        self.LoadTheGame(folderName)
                        print('done loading the game')
                        self.curr_screen="Pause"
                        pass
                    pass

            elif(self.action=="Quit"):
                self.curr_screen="AreYouSureYouWantToQuit"

            elif(self.action=="Settings"):
                self.curr_screen="Settings"

            elif(self.action=="Save"):
                if self.curr_Game!=None and self.curr_Game.curr_level!=None:
                    #Saving the current game.
                    gameDetailsFileName=f'{self.curr_Game.GameSettings.my_Name}_{self.curr_Game.GameSettings.my_age}'       #The folder name for this game.
                    dialog_logs,num_of_dialogs=getDialogLogInfo()
                    self.gameDataManager.createSaveGameDirectory(gameDetailsFileName)
                    self.gameDataManager.saveDialogLogs(dialog_logs, gameDetailsFileName)
                    GameData=self.curr_Game.saveGame()
                    self.gameDataManager.saveTheGame(GameData,gameDetailsFileName)

            elif(self.action=="Back To Home"):
                self.curr_screen="Start"

            elif(self.action=="Restart"):
                ClearDialogHistory()
                self.curr_Game=Game(self.clock)
                self.curr_Game.run(self.previous_esc_applied)

            elif(self.action=="Yes"):
                break

            elif(self.action=="No"):
                if self.curr_Game!=None:
                    self.curr_screen="Pause"
                else:
                    self.curr_screen="Start"

            elif(self.action=="Play Again"):
                ClearDialogHistory()
                self.curr_Game=Game(self.clock)
                self.curr_screen=self.curr_Game.run(self.previous_esc_applied)

            elif(self.action=="NOT_POSSIBLE"):
                self.curr_screen="Start"

            elif(self.action=="Reset Settings"):
                if self.curr_Game!=None:
                    self.curr_Game.GameSettings.reset_settings()

            elif(self.action=="Victory"):
                if self.curr_Game!=None and self.curr_Game.curr_level!=None:
                    #Saving the current game.
                    gameDetailsFileName=f'{self.curr_Game.GameSettings.my_Name}_{self.curr_Game.GameSettings.my_age}'       #The folder name for this game.
                    dialog_logs,num_of_dialogs=getDialogLogInfo()
                    self.gameDataManager.createSaveGameDirectory(gameDetailsFileName)
                    self.gameDataManager.saveDialogLogs(dialog_logs, gameDetailsFileName)
                    GameData=self.curr_Game.saveGame()
                    self.gameDataManager.saveTheGame(GameData,gameDetailsFileName)

            else:
                pass

    #A method to save the current game.
    def saveCurrentGame(self):
        if self.curr_Game!=None:
            pass
        pass


if __name__=='__main__':
    playGame=MyGame()