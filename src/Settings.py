import pygame
import os
from csv import reader
import sys
from math import sin        #To toggle between 0 to 255 for the flicker animation when the enemy or player sprite gets hit.
from random import randint
import json

pygame.init()
pygame.font.init()


#######################Original Settings####################
#Speeds
GAME_FPS=30
PLAYER_SPEED=10
ENEMY_SPEED=5
KEYBOARD_CAMERA_SPEED=20
MOUSE_CAMERA_SPEED=20
SCROLL_SETTINGS_SPEED=15


#Potion values. The specs of the potions dropped based on enemy type.
HEALTH_POTION_VAL=[100,150,200,300,500]
EXP_POTION_VAL=[200,300,400,600,1000]
ENERGY_POTION_VAL=[20,30,40,50,100]

#Others
GAME_TITLE="Time Rift Rescue"
GAME_START_PLAYER_POS=(1979,1206)
STARTING_LEVEL_ID=0
DRAW_TO_ENEMY=300               #In pixels.
DIRECTION2_ENEMY_RADIUS=200
TELEPORTATION_MAP={             #A dictionary of key (<level_id>_<teleportation_portal_top_left>) and value (a list of form [new_level_to_transport_to, new_player_pos])
    '0': [],
    '1': [],
    '2': [],
    '3': []
}
ENEMY_HEALTH=200
ENEMY_NOTICE_RADIUS=9         #A radius 5 BASE_SIZE's
ENEMY_ATTACK_RADIUS=1
INC_EXP_CAP=1.9                #A variable to indicate the factor by which the exp cap grows for the player.
    #A dictionary of key(weapon name) and value(a dictionary containing {cooldown_time, damage})
WEAPON_INFO={           #The last 3 attributes are list containing the said values for cooldown, damage respectively in the list.   
    'sword':{'cooldown': 200, 'damage': 30, 'min_val': [100,20], 'max_val': [300,50], 'cost_to_upgrade_one_unit': [10,40]},
    'lance':{'cooldown': 100, 'damage': 20, 'min_val': [100,20], 'max_val': [200,40], 'cost_to_upgrade_one_unit': [10,40]},
    'axe':{'cooldown': 150, 'damage': 40, 'min_val': [100,30], 'max_val': [200,70], 'cost_to_upgrade_one_unit': [10,40]},
}
MAGIC_INFO={
    'flame':{'cooldown':100,'strength':15,'cost':30, 'min_val': [100,15,25], 'max_val': [250,50,40], 'cost_to_upgrade_one_unit': [20,50,70]},
    'heal':{'cooldown':150,'strength':20,'cost':40, 'min_val': [100,15,25], 'max_val': [250,40,40], 'cost_to_upgrade_one_unit': [20,50,80]}
}
ZOMBIE_ENEMIES_INFO={
    'zombie1':{'health':100,'exp':50,'damage':10, 'resistance':2, 'attack_radius': ENEMY_ATTACK_RADIUS, 'notice_radius':ENEMY_NOTICE_RADIUS, 'attack_type': 'claw', 'speed':ENEMY_SPEED},
    'zombie2':{'health':150,'exp':100,'damage':20, 'resistance':2, 'attack_radius': ENEMY_ATTACK_RADIUS, 'notice_radius':ENEMY_NOTICE_RADIUS, 'attack_type': 'claw', 'speed':ENEMY_SPEED},
    'zombie3':{'health':200,'exp':200,'damage':50, 'resistance':2, 'attack_radius': ENEMY_ATTACK_RADIUS+1, 'notice_radius':ENEMY_NOTICE_RADIUS, 'attack_type': 'slash', 'speed':ENEMY_SPEED+1},
    'zombie4':{'health':400,'exp':500,'damage':75, 'resistance':2, 'attack_radius': ENEMY_ATTACK_RADIUS+2, 'notice_radius':ENEMY_NOTICE_RADIUS, 'attack_type': 'sparkle', 'speed':ENEMY_SPEED+2},
    'zombieBoss':{'health':1000,'exp':5000,'damage':150, 'resistance':2, 'attack_radius': ENEMY_ATTACK_RADIUS+4, 'notice_radius':ENEMY_NOTICE_RADIUS, 'attack_type': 'thunder', 'speed':ENEMY_SPEED+5}
}

#Sizes
BASE_SIZE=32
SCREEN_WIDTH=1240
SCREEN_HEIGHT=800
SCREEN_WIDTH_HALF=SCREEN_WIDTH//2
SCREEN_HEIGHT_HALF=SCREEN_HEIGHT//2
SCREEN_SIZE=(SCREEN_WIDTH,SCREEN_HEIGHT)
PLAYER_SIZE=(2*BASE_SIZE,3*BASE_SIZE)
ENEMY_SIZE=(2*BASE_SIZE,3*BASE_SIZE)
STRONG_ENEMY_SIZE=(3*BASE_SIZE,3*BASE_SIZE)


#Colors
SCREEN_BG_SHADE_COLOR=(127,127,127,0)
SCREEN_BG_DARK_COLOR=(0,255,0)
TEXT_COLOR=(255,255,255)
BUTTON_BACKGROUND_COLOR=(133,133,133)
BUTTON_HOVER_COLOR=(83,83,83)
BUTTON_CLICK_COLOR=(0,0,0)



#Folder Paths
WORKING_DIRECTORY_PATH=os.getcwd()
GRAPHICS_DIR_PATH=os.path.join(WORKING_DIRECTORY_PATH,"graphics")
PLAYER_DIRECTORY_PATH=os.path.join(GRAPHICS_DIR_PATH,"Player")
MAPS_DIRECTORY_PATH=os.path.join(GRAPHICS_DIR_PATH,"Ruins")            #Folder path to getting Maps and Other Graphics
PLAYER_MAGIC_DIRECTORY_PATH=os.path.join(GRAPHICS_DIR_PATH,"PLAYER_MAGIC")
PLAYER_WEAPONS_DIRECTORY_PATH=os.path.join(GRAPHICS_DIR_PATH,"PLAYER_WEAPON")
BASEMAP_NAME="BaseMap.png"                          #Name of Floor maps which are basically the 1st drawn image.
FLOORINFO_DIR_NAME="FloorInfo"
BLOCKS_PATH=os.path.join(GRAPHICS_DIR_PATH,"Blocks.png")



#The Background Shade when a Screen is active. These are the default values used.
bg_image=pygame.image.load(os.path.join(GRAPHICS_DIR_PATH,"GameStartingScreen.png"))
SCREEN_BG_SHADE_SURF=pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
SCREEN_BG_SHAD_POS=(0,0)


#Display Dialog Logs
DIALOG_LOGS=[]              #Contain only the messages. It would be better to make a global list containing all the dialogs and to this list, we can append a unique id associated with each Global Dialog instead of appending the whole dialog itself.
DIALOG_BOXES={}
NUM_OF_DIALOGS=0
DisplayDialogIMG=pygame.image.load(os.path.join(GRAPHICS_DIR_PATH,"Message_icon.png"))


#UI Information.
UI_TEXT_FONT=pygame.font.Font(None,20)
BAR_HEIGHT=20                       #Common for all the bars being displayed
HEALTH_BAR_WIDTH=int(SCREEN_WIDTH//8)
HEALTH_BAR_BGCOLOR=(60,60,60)
HEALTH_BAR_COLOR=(0,255,0)
HEALTH_BAR_BORDER_COLOR=(0,0,0)
ENERGY_BAR_WIDTH=int((3*HEALTH_BAR_WIDTH)//4)
ENERGY_BAR_BGCOLOR=(60,60,60)
ENERGY_BAR_COLOR=(103,146,160)
ENERGY_BAR_BORDER_COLOR=(0,0,0)
EXP_BAR_WIDTH=int(HEALTH_BAR_WIDTH//2)
EXP_BAR_BGCOLOR=(60,60,60)
EXP_BAR_COLOR=(255,255,0)
EXP_BAR_BORDER_COLOR=(0,0,0)
ITEM_BOX_SIZE=80
ITEM_BOX_BG_COLOR=(60,60,60)
ITEM_BOX_BORDER_COLOR=(0,0,0)
ITEM_BOX_BORDER_COLOR_ACTIVE=(255,215,0)


#COLORS for Changing the Settings.
TEXT_COLOR='white'
TEXT_COLOR_SELECTED='black'
BG_COLOR=BUTTON_BACKGROUND_COLOR
BG_COLOR_SELECTED='white'
BG_BORDER_COLOR='black'
BAR_COLOR='white'
BAR_COLOR_SELECTED='black'


#COST TO UPGRADE ANYTHING THAT IS UPGRADABLE.
COST_TO_UPGRADE_SPEEDS={
    "GAME_FPS":[30,60,10],
    "PLAYER_SPEED":[8,20,50],
    "ENEMY_SPEED":[4,15,20],
    "KEYBOARD_CAMERA_SPEED":[15,35,40],
    "MOUSE_CAMERA_SPEED":[15,35,40],
}



#######Game portal rectangles
Ruin0_rect_enterCode=pygame.rect.Rect(1184-BASE_SIZE,2528-BASE_SIZE,5*BASE_SIZE,5*BASE_SIZE)            #Is the Entrance to Ruin1
Ruin0_rect_Ruin2=pygame.rect.Rect(3424-BASE_SIZE,1440-BASE_SIZE,5*BASE_SIZE,5*BASE_SIZE)
Ruin0_rect_Ruin3=pygame.rect.Rect(4224-BASE_SIZE,3232-BASE_SIZE,5*BASE_SIZE,5*BASE_SIZE)

Ruin1_rect_Ruin0=pygame.rect.Rect(864,0,2*BASE_SIZE,2*BASE_SIZE)
Ruin1_rect_Ruin1_Dummy=pygame.rect.Rect(3134,960,2*BASE_SIZE,2*BASE_SIZE)
Ruin1_rect_Ruin1_hidden=pygame.rect.Rect(1056,2496,2*BASE_SIZE,2*BASE_SIZE)

Ruin2_rect_Ruin0=pygame.rect.Rect(2112,0,2*BASE_SIZE,2*BASE_SIZE)
Ruin2_rect_Ruin2_Dummy=pygame.rect.Rect(0,1632,2*BASE_SIZE,2*BASE_SIZE)
Ruin2_rect_Ruin2_hidden=pygame.rect.Rect(3168-BASE_SIZE,896,2*BASE_SIZE,2*BASE_SIZE)

Ruin3_rect_Ruin0=pygame.rect.Rect(704,2528-32,2*BASE_SIZE,2*BASE_SIZE)
Ruin3_rect_Ruin3_hidden=pygame.rect.Rect(0,672,2*BASE_SIZE,2*BASE_SIZE)




#########SCIENTIST DIALOG RECTANGELS, are created when the scientists are created.
SCIENTIST_DIALOG_COLLIDE_RECTS={
    '0':None,           #This value won't be changed and is simply going to get ignored. To remove this you would have to add an additional if statement in display_dialog_box_by_scientist method of Level
    '1':None,
    '2':None,
    '3':None
}




#A method to continuously toggle between 0 and 255.
def wave_value():
    value=sin(pygame.time.get_ticks()//2)
    if value>=0:
        return 255
    return 0

#Function to display the textbox along with the value in the string.
def display_textbox(display_surf,text_surf,text_rect,user_info,text_color,font):
    #Drawing the text_surf using text_rect.
    pygame.draw.rect(display_surf,'white',text_rect,0,border_radius=3)
    display_surf.blit(text_surf,(text_rect.centerx-text_surf.get_width()//2,text_rect.centery-text_surf.get_height()//2))

    #Drawing the user string.
    user_surf=font.render(user_info,True,text_color)
    white_bgrect=pygame.rect.Rect(text_rect.right+30, text_rect.top,user_surf.get_width()+(20 if len(user_info)>0 else 0),user_surf.get_height()+20)
    pygame.draw.rect(display_surf,'white',white_bgrect,0,border_radius=3)
    display_surf.blit(user_surf,(white_bgrect.centerx-user_surf.get_width()//2, white_bgrect.centery-user_surf.get_height()//2))

#Function to get the required credentials from the user.
def getRequiredInfo(textBoxNames,font,text_color='black',start_pos_y=50,bg_image=None,display_this_msg_and_pos=None,textBoxes_left=100):
    display_surf=pygame.display.get_surface()
    user_strings=[]             #Holds the strings obtained from the user. This is what is returned by this function.
    textBoxSurfs=[]             #Hold the rendered surfaces for the textboxNames.
    textBoxCollideRects=[]      #The rectangles on these rendered surfaces to check for collision.
    extra_box_space=20          #Used to maintain a bit more space in the textboxes.
    for index,textboxname in enumerate(textBoxNames):
        text_surf=font.render(textboxname,True,text_color)
        text_box=pygame.rect.Rect(textBoxes_left,start_pos_y+index*100, text_surf.get_width()+extra_box_space, text_surf.get_height()+extra_box_space)
        textBoxSurfs.append(text_surf)
        textBoxCollideRects.append(text_box)
        user_strings.append("")

    #Submit button and surface.
    submit_surf=font.render("Submit",True,text_color)
    submit_rect=pygame.rect.Rect(int((3*SCREEN_WIDTH)//4), SCREEN_HEIGHT_HALF, submit_surf.get_width()+extra_box_space, submit_surf.get_height()+extra_box_space)
    submit_rect_pos=(submit_rect.centerx-submit_surf.get_width()//2,submit_rect.centery-submit_surf.get_height()//2)

    display_msg=None
    if(display_this_msg_and_pos!=None):
        display_msg=display_this_msg_and_pos[0]
        display_msg_pos=display_this_msg_and_pos[1]
        display_msg_left=display_msg_pos[0]
        display_msg_top=display_msg_pos[1]
        display_msg_width=display_msg_pos[2]
        display_msg_height=display_msg_pos[3]

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:      #1st condition to check for mouse click, 2nd condition to check for left click.
                mouse_pos=pygame.mouse.get_pos()
                if submit_rect.collidepoint(mouse_pos):
                    return user_strings
            if event.type==pygame.KEYDOWN:      #If user clicks enter(which is often referred to as 'carriage return'), then return the strings.
                if event.key==pygame.K_RETURN:
                    return user_strings
                mouse_pos=pygame.mouse.get_pos()
                for index,rect in enumerate(textBoxCollideRects):
                    if rect.collidepoint(mouse_pos):
                        if event.key==pygame.K_BACKSPACE:
                            user_strings[index]=user_strings[index][:-1]
                        else:
                            user_strings[index]+=event.unicode
        
        #Blitting all the textboxes and the submit button.
        if(bg_image!=None):
            display_surf.blit(bg_image,(0,0))
        else:
            display_surf.fill('black')
        
        if(display_msg!=None):
            DISPLAY_MSG(display_msg,display_msg_left,display_msg_top,display_msg_width,display_msg_height,shd_do_next_msg_prompt="")
        
        for index,text_surf in enumerate(textBoxSurfs):
            display_textbox(display_surf,text_surf,textBoxCollideRects[index],user_strings[index],text_color,font)
        pygame.draw.rect(display_surf,'white',submit_rect,0,border_radius=3)
        display_surf.blit(submit_surf,submit_rect_pos)

        pygame.display.flip()

#Function to draw a half-transparent background with a shade of the given color. Used only when displaying a screen.
def drawShadedBGScreen(display_surf,shaded_color=SCREEN_BG_SHADE_COLOR):
    pygame.draw.rect(bg_image,shaded_color,[0,0,SCREEN_WIDTH,SCREEN_HEIGHT])       #Fills the rectangle with specified color and draws this on the surface.
    display_surf.blit(bg_image,SCREEN_BG_SHAD_POS)

#Function to save the image of the screen whenever a different screen is going to be displayed.
def SaveGameScreen(display_surf=None,filename="Curr_Screen.png"):
    if(display_surf==None):
        display_surf=pygame.display.get_surface()
    rect=pygame.rect.Rect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT)
    screenshot=pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
    screenshot.blit(display_surf,rect.topleft,area=rect)
    pygame.image.save(screenshot,os.path.join(GRAPHICS_DIR_PATH,filename))

#Function to load the Current screen image
def LoadCurrScreen():
    return pygame.image.load(os.path.join(GRAPHICS_DIR_PATH,"Curr_Screen.png"))

#Function to clear the dialogs.
def ClearDialogHistory():
    global DIALOG_BOXES, DIALOG_LOGS, NUM_OF_DIALOGS
    DIALOG_BOXES.clear()
    DIALOG_LOGS.clear()
    NUM_OF_DIALOGS=0

#Function to return the dialogs, num of dialogs.
def getDialogLogInfo():
    global DIALOG_LOGS, NUM_OF_DIALOGS
    return DIALOG_LOGS, NUM_OF_DIALOGS

#A Function Add the Dialog to the Dialog Logs
def AddDialogToLogs(dialog):
    if len(dialog)==0:
        return
    
    global DIALOG_LOGS
    global DIALOG_BOXES
    global NUM_OF_DIALOGS

    DIALOG_LOGS.append(dialog)

    msg_box_width=SCREEN_WIDTH-100
    msg_box_height=int(SCREEN_HEIGHT_HALF//2)
    msg_box_left=60
    msg_box_top=100 + (NUM_OF_DIALOGS*(msg_box_height + 20))
    DialogSurf=pygame.Surface((msg_box_width,msg_box_height),pygame.SRCALPHA)
    DialogScreen=pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)

    DISPLAY_MSG(dialog[0],60,40,msg_box_width,msg_box_height,is_first_msg=True,display_surf=DialogScreen)
    DialogSurf.blit(DialogScreen,(-60,-40))
    
    DIALOG_BOXES[f'{NUM_OF_DIALOGS}']=[DialogSurf,pygame.rect.Rect(msg_box_left,msg_box_top,msg_box_width,msg_box_height)]
    NUM_OF_DIALOGS += 1

#A helper Function to simply reset the scrolled positions back to original values. This helper is necessary because we are dynamically adding new dialog boxes(rectangles) and if they happen to collide with the scrolled positions of other dialogs, it would result in unwanted behaviour. In SETTINGS page, this is not required as we have only a fixed number of visible item boxes.
def reset_scroll_of_dialog_boxes(accumulated_scroll,escape_button_rect):
    for index in list(DIALOG_BOXES.keys()):
        rect=DIALOG_BOXES[index][1]
        rect.y-=accumulated_scroll

    escape_button_rect.y-=accumulated_scroll

#A Function to Display the Dialogs Log.
def DisplayDialogHistory(bg_image=None):

    screen=pygame.display.get_surface()

    global NUM_OF_DIALOGS
    global DIALOG_BOXES
    num_of_dialogs=NUM_OF_DIALOGS

    scroll_settings_screen=0
    accumulated_scroll=0
    SETTINGS_SCREEN_TOP=0
    SETTINGS_SCREEN_BOTTOM=-DIALOG_BOXES[f'{len(DIALOG_BOXES)-1}'][1].top + SCREEN_HEIGHT_HALF + int(SCREEN_HEIGHT_HALF//2) - 40

    escape_button_text_surf=pygame.font.Font(None,30).render("Back",True,'black')
    escape_button_rect=pygame.rect.Rect(int(SCREEN_WIDTH_HALF//2),50,int(escape_button_text_surf.get_width()+20),int(escape_button_text_surf.get_height()+20))

    quit_button_text_surf=pygame.font.Font(None,30).render("Quit", True,'black')
    quit_button_rect=pygame.rect.Rect(int((3*SCREEN_WIDTH)//4),50,int(quit_button_text_surf.get_width()+20),int(quit_button_text_surf.get_height()+20))

    running=True
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                running=False
                reset_scroll_of_dialog_boxes(accumulated_scroll,escape_button_rect)
                break
            if event.type == pygame.MOUSEWHEEL:
                scroll_settings_screen=event.y*SCROLL_SETTINGS_SPEED
                accumulated_scroll+=scroll_settings_screen
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_g:
                    reset_scroll_of_dialog_boxes(accumulated_scroll,escape_button_rect)
                    return None
            if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:      #1st condition to check for mouse click, 2nd condition to check for left click.
                mouse_pos=pygame.mouse.get_pos()
                for index in list(DIALOG_BOXES.keys()):
                    rect=DIALOG_BOXES[index][1]
                    if rect.collidepoint(mouse_pos):
                        reset_scroll_of_dialog_boxes(accumulated_scroll,escape_button_rect)
                        return int(index)
                    
                if escape_button_rect.collidepoint(mouse_pos):
                    reset_scroll_of_dialog_boxes(accumulated_scroll,escape_button_rect)
                    return None
                
                if quit_button_rect.collidepoint(mouse_pos):
                    reset_scroll_of_dialog_boxes(accumulated_scroll,escape_button_rect)
                    return "QUIT"
                pass
    
        if running==False:
            return "QUIT"

        if accumulated_scroll>SETTINGS_SCREEN_TOP:
            accumulated_scroll-=scroll_settings_screen
            scroll_settings_screen=0
        elif accumulated_scroll<SETTINGS_SCREEN_BOTTOM:
            accumulated_scroll-=scroll_settings_screen
            scroll_settings_screen=0
        
        if bg_image!=None:
            screen.blit(bg_image,(0,0))
        else:
            screen.fill((27,27,27))

        #Updating the rect positions of the escape button, dialog buttons.
        escape_button_rect.y+=scroll_settings_screen
        quit_button_rect.y+=scroll_settings_screen
        for index in list(DIALOG_BOXES.keys()):
            rect=DIALOG_BOXES[index][1]
            rect.y+=scroll_settings_screen

        pygame.draw.rect(screen,'white',escape_button_rect,0,3)
        screen.blit(escape_button_text_surf,(escape_button_rect.centerx-escape_button_text_surf.get_width()//2, escape_button_rect.centery-escape_button_text_surf.get_height()//2))

        pygame.draw.rect(screen,'white',quit_button_rect,0,3)
        screen.blit(quit_button_text_surf,(quit_button_rect.centerx-quit_button_text_surf.get_width()//2, quit_button_rect.centery-quit_button_text_surf.get_height()//2))

        for i in range(num_of_dialogs):
            surf_rect=DIALOG_BOXES[f'{i}']
            screen.blit(surf_rect[0],(surf_rect[1].left,surf_rect[1].top))
        
        scroll_settings_screen=0
        pygame.display.flip()

#A function which uses the DISPLAY_MSG to continuously display all the messages.
def DISPLAY_DIALOGS(DialogBox,message_box_left,message_box_top,message_box_width,message_box_height,bg_image=None,font=pygame.font.Font(None,30),shd_log_dialogs=True):
    if len(DialogBox)==0:
        return
    
    if shd_log_dialogs==True:
        AddDialogToLogs(DialogBox)

    if bg_image==None:
        bg_image=pygame.surface(SCREEN_WIDTH,SCREEN_HEIGHT)
        bg_image.fill('black')
    display_msg_index=0
    dialogs=list(DialogBox)
    num_of_msgs=len(dialogs)
    
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    display_msg_index+=1
                    if(display_msg_index>=num_of_msgs):
                        return
                elif event.key==pygame.K_BACKSPACE:
                    display_msg_index-=1
                    display_msg_index=0 if display_msg_index<=0 else display_msg_index
        
        pygame.display.get_surface().blit(bg_image,(0,0))
        is_first_msg=(display_msg_index==0)
        DISPLAY_MSG(dialogs[display_msg_index],message_box_left,message_box_top,message_box_width,message_box_height,font,is_first_msg=is_first_msg)
        pygame.display.flip()

#A function to display a message. The function splits the message into different lines if the message is long.
def DISPLAY_MSG(message, message_box_left,message_box_top,message_box_width,message_box_height,font=pygame.font.Font(None,30),shd_do_next_msg_prompt=None,is_first_msg=False,display_surf=None, next_msg_prompt=""):
    if(message==None):
        return
    if display_surf==None:
        display_surf=pygame.display.get_surface()

    pygame.draw.rect(display_surf,BG_COLOR,(message_box_left,message_box_top,message_box_width,message_box_height),0,border_radius=10)
    pygame.draw.rect(display_surf,BG_BORDER_COLOR,(message_box_left,message_box_top,message_box_width,message_box_height),3,border_radius=10)

    collection=[word.split(' ') for word in message.splitlines()]
    space=font.size(' ')[0]
    x=message_box_left+20
    y=message_box_top+20
    for lines in collection:
        for words in lines:
            word_surf=font.render(words,True,'white')
            word_width, word_height=word_surf.get_size()
            if x+word_width>=message_box_width:
                x=message_box_left+20
                y+=word_height+20
            display_surf.blit(word_surf,(x,y))

            x+=word_width+space
        x=message_box_left+20
        y+=word_height+20
    
    if(shd_do_next_msg_prompt==None):
        next_msg_prompt="'Enter' - next message,'Backspace' - previous message"
        if is_first_msg:
            next_msg_prompt="'Enter' - next message"
        next_msg_surf=font.render(next_msg_prompt,False,'white')
        next_msg_rect=pygame.rect.Rect(message_box_width-next_msg_surf.get_width()-20,message_box_height-next_msg_surf.get_height(),next_msg_surf.get_width(),next_msg_surf.get_height())
        display_surf.blit(next_msg_surf,next_msg_rect)
    elif(shd_do_next_msg_prompt!=""):
        # pass
        next_msg_surf=font.render(next_msg_prompt,False,'white')
        next_msg_rect=pygame.rect.Rect(message_box_width-next_msg_surf.get_width()-20,message_box_height-next_msg_surf.get_height(),next_msg_surf.get_width(),next_msg_surf.get_height())
        display_surf.blit(next_msg_surf,next_msg_rect)


#A function to display the given text on the screen.
debug_font=pygame.font.Font(None,30)
def debug_print(text,pos,display_surf=None):
    if display_surf==None:
        display_surf=pygame.display.get_surface()
    debug_surf=debug_font.render(str(text),'True','Black')
    display_surf.blit(debug_surf,pos)


#Function to save rectangles as they are not serializable.
def rect_to_dict(rect):
    if(rect==None):
        return None
    return {
        'type': "pygame.rect.Rect",
        'x':rect.x,
        'y':rect.y,
        'width':rect.width,
        'height':rect.height,
    }

#Function to save vectors as they are not serializable.
def vect2_to_dict(vector):
    if vector==None:
        return None
    return {
        'type':'pygame.math.Vector2',
        'x':vector.x,
        'y':vector.y
    }

#Function to save font as they are not serializable.
def font_to_dict(font):
    if font==None:
        return None
    return {
        'type':'pygame.font.Font',
        'font_size':font.get_linesize()
    }

#Function to save sprite as they are not serializable.
def sprite_to_dict(sprite):
    spriteData=sprite.__dict__.copy()
    spriteData['_Sprite__g']=None           #Enemy sprites will automatically be added to the level.enemy_sprites as we are only saving them.
    spriteData['graphics']=None             #Enemy sprites will automatically have their sprites done.
    spriteData['img']=None
    spriteData['mask']=None
    spriteData['rect']=rect_to_dict(sprite.rect)
    spriteData['direction']=vect2_to_dict(sprite.direction)
    return spriteData

#Function save spriteGroup as they are not serializable.
def enemySprites_to_dict(spriteGroup):
    sprites=[]
    for sprite in spriteGroup:
        sprites.append(sprite_to_dict(sprite))
    return sprites

def lootsprite_to_dict(sprite):
    spriteData=sprite.__dict__.copy()
    spriteData['_Sprite__g']=None
    spriteData['img']=None
    spriteData['rect']=rect_to_dict(sprite.rect)

    return spriteData

#Function to save loot sprites as they are not serializable.
def lootSprites_to_dict(spriteGroup):
    sprites=[]
    for sprite in spriteGroup:
        sprites.append(lootsprite_to_dict(sprite))
    return sprites

#Function to save the scientist.
def scientist_to_dict(scientist):
    if scientist==None:
        return None
    
    scientistData=scientist.__dict__.copy()
    scientistData['_Sprite__g']=None
    scientistData['img']=None
    scientistData['rect']=rect_to_dict(scientist.rect)
    scientistData['finder']=None
    scientistData['direction']=vect2_to_dict(scientist.direction)
    scientistData['escape_path']=None

    return scientistData

# # SOME FORMATS I USED WHILE CREATING MAPS IN TILED.
# # #ALL_BLOCKS - Has 'elem_id' as key, the block 'img' as value. This will be initialized in the Level object's using 'load_ALL_BLOCKS()'.
# #     #elem_id: 500      ==> 'Gate_being_opened'              ==>"BROWN". The image will have id of 500. When player kills all zombies, this sprite will be killed so that player can move to original gate.
# #     #elem_id: 300      ==> 'Scientist1'                       ==>"ORANGE" color in Tiled map.
# #     #elem_id: 301      ==> 'Scientist2'                       ==>"MAGENTA" color in Tiled map.
# #     #elem_id: 302      ==> 'Scientist3'                       ==>"WHITE" color in Tiled map.

# #     #elem_id: 100      ==> 'zombie1 start position'           ==>"PINK" color in Tiled map.
# #     #elem_id: 101      ==> 'zombie2 start position'           ==>"YELLOW" color in Tiled map.
# #     #elem_id: 102      ==> 'zombie3 start position'           ==>"PURPLE" color in Tiled map.
# #     #elem_id: 103      ==> 'zombie4 start position'           ==>"BLUE" color in Tiled map.
# #     #elem_id: 104      ==> 'zombieBoss start position'        ==>"SILVER" color in Tiled map.
# #     #elem_id: 1000     ==> 'Invisible'                        ==>"RED" color in Tiled map.
    ###################################################### elem_id: 1001     ==> 'Player start position'            ==>"GREEN" color in Tiled map.
# #     #elem_id: 1003     ==> 'Transport gates'                  ==>"BLACK" color in Tiled map.
# # ALL_BLOCKS={}
# # def load_ALL_BLOCKS():
# #     ALL_BLOCKS[1000]=getSpriteFromSpriteSheet(BLOCKS_PATH,32,32,0,0,'Black')
# #     ALL_BLOCKS[1001]=getSpriteFromSpriteSheet(BLOCKS_PATH,32,32,32,0,'Black')


SUB_SURFACE=SCREEN_BG_SHADE_SURF
SUB_SURFACE.fill('green')


#This class contains the variables that can be changed in the game.
class Settings:
    def __init__(self):
        self.my_Name=None
        self.my_age=None

        #Speeds
        self.GAME_FPS=GAME_FPS
        self.PLAYER_SPEED=PLAYER_SPEED
        self.ENEMY_SPEED=ENEMY_SPEED
        self.KEYBOARD_CAMERA_SPEED=KEYBOARD_CAMERA_SPEED
        self.MOUSE_CAMERA_SPEED=MOUSE_CAMERA_SPEED

        #A dictionary of key(weapon name) and value(a dictionary containing {cooldown_time, damage})
        self.WEAPON_INFO=WEAPON_INFO.copy()
        self.MAGIC_INFO=MAGIC_INFO.copy()
        self.ZOMBIE_ENEMIES_INFO=ZOMBIE_ENEMIES_INFO.copy()


        #Attributes you can change .
        self.attributes_num=10         #To change the 5 speed attributes, WEAPON_INFO, MAGIC_INFO attributes.
        self.attribute_names=[
            "GAME_FPS",
            "PLAYER_SPEED",
            "ENEMY_SPEED",
            "KEYBOARD_CAMERA_SPEED",
            "MOUSE_CAMERA_SPEED",
            "Weapon1 Cooldown",              
            "Weapon1 Damage",
            "Weapon2 Cooldown",              
            "Weapon2 Damage",
            "Weapon3 Cooldown",              
            "Weapon3 Damage",
            "Magic1 Cooldown",
            "Magic1 Strength",
            "Magic1 Cost",
            "Magic2 Cooldown",
            "Magic2 Strength",
            "Magic2 Cost",
        ]

        #Player information variables.
        self.NamePos=[SCREEN_WIDTH//3,20]
        self.AgePos=[SCREEN_WIDTH//2 + SCREEN_WIDTH//6,20]

        #The weapon and magic names
        self.Names=[key for key in WEAPON_INFO for _ in range(2)] + [key for key in MAGIC_INFO for _ in range(3)]

        #Attributes for selecting the value you want to change.
        self.selected_attr_index=0
        self.selected_time=None
        self.can_select_different=True
        self.can_select_duration=300

        #Value changer dimensions.
        self.val_changer_height=int((3*SCREEN_HEIGHT)//9)
        self.val_changer_width=int(SCREEN_WIDTH//6)
        self.width_gap=35
        self.height_gap=60
        self.base_height=200

        self.items=None
        self.item_count=0
        self.create_items()
        self.total_rows=(self.item_count-1)//5
        self.extra_cols=self.item_count-((self.total_rows)*5)

        self.info_font=pygame.font.Font(None,40)

    #A method to reset the settings to the original game's settings.
    def reset_settings(self):
        self.GAME_FPS=GAME_FPS
        self.PLAYER_SPEED=PLAYER_SPEED
        self.ENEMY_SPEED=ENEMY_SPEED
        self.KEYBOARD_CAMERA_SPEED=KEYBOARD_CAMERA_SPEED
        self.MOUSE_CAMERA_SPEED=MOUSE_CAMERA_SPEED

        self.WEAPON_INFO=WEAPON_INFO.copy()
        self.MAGIC_INFO=MAGIC_INFO.copy()
        self.ZOMBIE_ENEMIES_INFO=ZOMBIE_ENEMIES_INFO.copy()
        
        for item in self.items:
            item.has_been_selected=False

    #Displaying only the speed related settings when in start settings.            ######NOT USED CURRENTLY ##########
    def DisplayStartSettings(self,display_surf):
        for index,item in enumerate(self.items):
            if(index<5):
                attr_name=self.attribute_names[index]
                upgrading_costs=COST_TO_UPGRADE_SPEEDS[attr_name]
                item.display_item(display_surf,attr_name,self.selected_attr_index,getattr(self,attr_name),upgrading_costs[0],upgrading_costs[1],upgrading_costs[2],0)

    #A cooldown for the timer to select a different item from the settings screen.
    def apply_cooldown(self):
        if not self.can_select_different:
            if pygame.time.get_ticks()-self.selected_time >= self.can_select_duration:
                self.can_select_different=True

    #A method to select the item in the settings screen.
    def select_the_item(self,can_change_values):
        keys=pygame.key.get_pressed()
        
        if(self.can_select_different and can_change_values):
            previous_index=self.selected_attr_index
            previous_row=previous_index//5
            previous_col=previous_index%5
            
            #Handling the selected index's movement when moving outside certain limits(as visible on the settings screen).
            if(keys[pygame.K_RIGHT]):
                self.selected_attr_index+=1
                self.can_select_different=False
                self.selected_time=pygame.time.get_ticks()
                if(self.selected_attr_index>self.item_count-1):
                    self.selected_attr_index=(previous_row)*5
                elif(self.selected_attr_index//5!=previous_index//5):
                    self.selected_attr_index=(previous_index//5)*5
            elif(keys[pygame.K_LEFT]):
                self.selected_attr_index-=1
                self.can_select_different=False
                self.selected_time=pygame.time.get_ticks()
                if(previous_row==self.total_rows and previous_col==0):
                    self.selected_attr_index=self.item_count-1
                elif(self.selected_attr_index//5!=previous_index//5):
                    self.selected_attr_index=((previous_index//5)*5)+4
            elif(keys[pygame.K_UP]):
                self.selected_attr_index-=5         #Assuming there are 5 value changers being displayed in one row.
                self.can_select_different=False
                self.selected_time=pygame.time.get_ticks()
                if(self.selected_attr_index<0):
                    if(previous_col>(self.extra_cols-1)):
                        self.selected_attr_index=((self.total_rows-1)*5)+previous_col
                    else:
                        self.selected_attr_index=(self.total_rows*5)+previous_col
            elif(keys[pygame.K_DOWN]):
                self.selected_attr_index+=5         #Assuming there are 5 value changers being displayed in one row.
                self.can_select_different=False
                self.selected_time=pygame.time.get_ticks()
                if(self.selected_attr_index>self.item_count-1):
                    self.selected_attr_index=previous_index%5

    #A method to display the name, age.
    def display_my_information(self,display_surf,scroll_settings_screen):
        name_surf=self.info_font.render(self.my_Name,False,'black')
        age_surf=self.info_font.render(self.my_age,False,'black')

        display_surf.blit(name_surf,self.NamePos)
        display_surf.blit(age_surf,self.AgePos)

    #A method to display all the game's settings which can be changed(the value).
    def display_settings(self,display_surf,Game,can_change_values=0,scroll_settings_screen=0):
        self.NamePos[1]+=scroll_settings_screen
        self.AgePos[1]+=scroll_settings_screen
        self.display_my_information(display_surf,scroll_settings_screen)
        self.select_the_item(can_change_values)
        self.apply_cooldown()

        for index,item in enumerate(self.items):
            #Displaying the speed related game settings.
            if(index<5):
                attr_name=self.attribute_names[index]
                upgrading_costs=COST_TO_UPGRADE_SPEEDS[attr_name]
                item.display_item(display_surf,attr_name,self.selected_attr_index,getattr(Game.GameSettings,attr_name),upgrading_costs[0],upgrading_costs[1],upgrading_costs[2],scroll_settings_screen)

            #Displaying the player attack options.
            elif(index<11):
                WeaponName=self.Names[index-5]
                curr_weapon=Game.GameSettings.WEAPON_INFO[WeaponName]
                curr_vals=[curr_weapon['cooldown'],curr_weapon['damage']]
                index_to_use=(index-1)%2
                item.display_item(display_surf,WeaponName,self.selected_attr_index,curr_vals[index_to_use],curr_weapon['min_val'][index_to_use],curr_weapon['max_val'][index_to_use],curr_weapon['cost_to_upgrade_one_unit'][index_to_use],scroll_settings_screen)

            #Displaying the player magic options.
            else:
                MagicName=self.Names[index+6-11]
                curr_magic=Game.GameSettings.MAGIC_INFO[MagicName]
                curr_vals=[curr_magic['cooldown'],curr_magic['strength'],curr_magic['cost']]
                index_to_use=(index-2)%3
                item.display_item(display_surf,MagicName,self.selected_attr_index,curr_vals[index_to_use],curr_magic['min_val'][index_to_use],curr_magic['max_val'][index_to_use],curr_magic['cost_to_upgrade_one_unit'][index_to_use],scroll_settings_screen)

    #A method to create items whose values can be changed in the settings option.
    def create_items(self):
        self.items=[]
        #########The first list being multiplied is for the attacks, with the number of attack available. The second list being multiplied is for the magic, with the number of magic available.
        extra_attr_names=['(Cooldown)','(Damage)']*3 + ['(Cooldown)','(Strength)','(Cost)']*2
        for index,item_name in enumerate(self.attribute_names):
            left=self.width_gap+(index%5)*self.val_changer_width+self.width_gap*(index%5)
            top=self.base_height+int(index//5)*(self.val_changer_height + self.height_gap)
            extra_attr=None
            if(index>4):
                extra_attr=extra_attr_names[index-5]
            item=Item(left,top,self.val_changer_width,self.val_changer_height,index,UI_TEXT_FONT,extra_attr)
            self.items.append(item)
            self.item_count+=1
    
    #A method to apply changes to the selected item.
    def apply_changes(self,game):
        for index,item in enumerate(self.items):
            if index<5:
                if(item.apply_changes(self.selected_attr_index,self.attribute_names[index],game,COST_TO_UPGRADE_SPEEDS[self.attribute_names[index]][0],COST_TO_UPGRADE_SPEEDS[self.attribute_names[index]][1])=="Applied"):
                    if index==1:
                        game.player.speed=self.PLAYER_SPEED

            elif(index<11):
                WeaponName=self.Names[index-5]
                curr_weapon=game.GameSettings.WEAPON_INFO[WeaponName]
                index_to_use=(index-1)%2
                extra_attr_name=['cooldown','damage']
                item.apply_changes(self.selected_attr_index,WeaponName,game,curr_weapon['min_val'][index_to_use],curr_weapon['max_val'][index_to_use],extra_attr_name[index_to_use])

            else:
                MagicName=self.Names[index+6-11]
                curr_magic=game.GameSettings.MAGIC_INFO[MagicName]
                extra_attr_name=['cooldown','strength','cost']
                index_to_use=(index-2)%3
                item.apply_changes(self.selected_attr_index,MagicName,game,curr_magic['min_val'][index_to_use],curr_magic['max_val'][index_to_use],extra_attr_name[index_to_use])

    def saveItems(self):
        items=[]
        for item in self.items:
            items.append(item.saveItem())
        return items
    
    def saveSettings(self):
        settingsData=self.__dict__.copy()
        settingsData['items']=self.saveItems()
        settingsData['info_font']=font_to_dict(self.info_font)
        # with open('dataSettings.json','w') as f:
        #     json.dump(settingsData,f)
        # # print(self.__dict__.copy())
        return settingsData
    
    #A method to make a serializable copy of all the items.
    def useItemData(self, itemDatas):
        items=[]
        for itemData in itemDatas:
            newItem=Item(itemData['rect']['x'], itemData['rect']['y'], itemData['rect']['width'], itemData['rect']['height'], itemData['index'], UI_TEXT_FONT, itemData['extra_attr_name'])
            newItem.useSavedData(itemData)
            items.append(newItem)
        
        return items
    
    #A method to make load the settings using the saved data.
    def useSavedData(self, settingsData):
        self.GAME_FPS=settingsData['GAME_FPS']
        self.PLAYER_SPEED=settingsData['PLAYER_SPEED']
        self.ENEMY_SPEED=settingsData['ENEMY_SPEED']
        self.KEYBOARD_CAMERA_SPEED=settingsData['KEYBOARD_CAMERA_SPEED']
        self.MOUSE_CAMERA_SPEED=settingsData['MOUSE_CAMERA_SPEED']

        #A dictionary of key(weapon name) and value(a dictionary containing {cooldown_time, damage})
        self.WEAPON_INFO=settingsData['WEAPON_INFO']
        self.MAGIC_INFO=settingsData['MAGIC_INFO']
        self.ZOMBIE_ENEMIES_INFO=settingsData['ZOMBIE_ENEMIES_INFO']

        self.items=self.useItemData(settingsData['items'])
        self.my_Name=settingsData['my_Name']
        self.my_age=settingsData['my_age']
        self.selected_attr_index=settingsData['selected_attr_index']
        self.item_count=settingsData['item_count']


        print('done saving the items')
        pass

#A class for displaying one of the game's attributes that can be changed(the value).
class Item:
    def __init__(self,left,top,width,height,index,font,extra_attr_name=None):
        self.scroll_top_limit=top
        self.rect=pygame.rect.Rect(left,top,width,height)
        self.index=index
        self.font=font
        self.extra_attr_name=extra_attr_name

        #Item ui related variables.
        self.top=self.rect.midtop+pygame.math.Vector2(0,35)
        self.bottom=self.rect.midbottom-pygame.math.Vector2(0,55)
        self.has_extra_attr=False
        if(extra_attr_name!=None):
            self.has_extra_attr=True
            self.top=self.top + pygame.math.Vector2(0,20)
        
        #Upgrade related variables.
        self.curr_rect=pygame.rect.Rect(self.top[0]-10,self.top[1],20,5)
        self.curr_from_bottom_pos=None
        self.has_been_selected=False
        self.cost_for_upgrading=None
        self.mouse_collider_rect=pygame.rect.Rect(self.rect.centerx-10,self.top[1],20,self.bottom[1]-self.top[1])

    #A method to apply changes to the game settings.
    def apply_changes(self,selected_index,attr_name,game,min_val,max_val,extra_attr_name=None):
        if selected_index==self.index:
            #Find the curr_val value.
            if(self.has_been_selected and game.player.exp >= self.cost_for_upgrading):
                game.player.exp -= self.cost_for_upgrading
                self.cost_for_upgrading=0
                self.has_been_selected=False

                #Based on mouse pos, get the curr_val.
                #self.curr_from_bottom_pos is the selected position to change the value to.
                height_of_line=self.bottom[1]-self.top[1]
                distance_from_bottom=self.bottom[1]-self.curr_from_bottom_pos
                curr_new_val=min_val+ (((max_val-min_val)*distance_from_bottom)//height_of_line)

                #Updating the appropriate game setting.
                if self.index<5:
                    setattr(game.GameSettings,attr_name,curr_new_val)
                elif self.index<11:
                    game.GameSettings.WEAPON_INFO[attr_name][extra_attr_name]=curr_new_val
                else:
                    game.GameSettings.MAGIC_INFO[attr_name][extra_attr_name]=curr_new_val
                return "Applied"
            
            elif(self.has_been_selected):
                self.cost_for_upgrading=0
                self.has_been_selected=False
                return "Could Not Apply, NOT ENOUGH EXP"
            
        return ""

    #A method to select a value of the item.
    def select_the_upgraded_val(self,is_selected,curr_val,min_val,max_val,cost_of_one_unit):
        if(is_selected):
            is_left_click=pygame.mouse.get_pressed()[0]
            mouse_pos=pygame.mouse.get_pos()
            if(is_left_click and self.mouse_collider_rect.collidepoint(mouse_pos)):
                self.curr_from_bottom_pos=mouse_pos[1]
                self.has_been_selected=True

                height_of_line=self.bottom[1]-self.top[1]
                curr_val_height_from_bottom=((curr_val-min_val)*height_of_line)//(max_val-min_val)
                curr_pos=self.bottom[1]-curr_val_height_from_bottom
                self.cost_for_upgrading=(abs(curr_pos-mouse_pos[1])*(cost_of_one_unit*(max_val-min_val)))//(height_of_line)

    #A method to display the item's name.
    def display_name(self,surface,name,cost,curr_val,is_selected):
        #Displaying attribute name
        txt_color=TEXT_COLOR_SELECTED if is_selected else TEXT_COLOR
        text_surf=self.font.render(str(name).capitalize(),True,txt_color)
        text_rect=text_surf.get_rect(midtop=self.rect.midtop + pygame.math.Vector2(0,10))
        surface.blit(text_surf,text_rect)

        #Displaying the extra attribute name if any.
        if(self.index>4):
            extra_text_surf=self.font.render(str(self.extra_attr_name),True,txt_color)
            surface.blit(extra_text_surf,(text_rect.centerx-extra_text_surf.get_width()//2, text_rect.bottom + 10))

        #Displaying the current value.
        curr_val_surf=self.font.render(f'Current val: {curr_val}',False,txt_color)
        surface.blit(curr_val_surf,(self.rect.centerx-curr_val_surf.get_width()//2,self.rect.bottom-2*curr_val_surf.get_height()-20))

        #Displaying the cost.
        cost_surf=self.font.render(f'upgrade cost: {cost}', False, txt_color)
        surface.blit(cost_surf,(self.rect.centerx-cost_surf.get_width()//2, self.rect.bottom-cost_surf.get_height()-10))

    def display_bar(self,surface,curr_val,min_val,max_val,is_selected,scroll_settings_screen):
        #Drawing the line.
        bar_color=BAR_COLOR_SELECTED if is_selected else BAR_COLOR
        pygame.draw.line(surface,bar_color,self.top,self.bottom,width=3)

        #Drawing the curr_rect for curr_val
        curr_pos=None
        if(self.has_been_selected):
            curr_pos=self.curr_from_bottom_pos
        else:
            height_of_line=self.bottom[1]-self.top[1]
            curr_val_height_from_bottom=((curr_val-min_val)*height_of_line)//(max_val-min_val)
            curr_pos=self.bottom[1]-curr_val_height_from_bottom
            curr_pos+=scroll_settings_screen

        #Drawing the selector.
        self.curr_rect=pygame.rect.Rect(self.top[0]-10,curr_pos,20,5)
        pygame.draw.rect(surface,bar_color,self.curr_rect)
    
    #A method to scroll the item(some of the rectangles used for blitting the item).
    def scroll(self,scroll_settings_screen):
        self.rect.top+=scroll_settings_screen
        self.top=self.rect.midtop+pygame.math.Vector2(0,35)
        self.bottom=self.rect.midbottom-pygame.math.Vector2(0,55)
        if(self.has_extra_attr):
            self.top=self.top + pygame.math.Vector2(0,20)
        self.mouse_collider_rect.top+=scroll_settings_screen

    #A method to display one attribute of the game. Min val is bottom position. Max val is top position.
    def display_item(self,display_surf,attr_name,selected_index,curr_val,min_val,max_val,cost_to_upgrade_by_one_unit,scroll_settings_screen=0):
        #Scrolling the item.
        self.scroll(scroll_settings_screen)

        #Drawing the box.
        is_selected=1 if (self.index==selected_index) else 0
        if is_selected:
            pygame.draw.rect(display_surf,BG_COLOR_SELECTED, self.rect,border_radius=3)
        else:
            pygame.draw.rect(display_surf,BG_COLOR, self.rect,border_radius=3)

        #Drawing the border.
        pygame.draw.rect(display_surf,BG_BORDER_COLOR,self.rect,4,border_radius=3)

        #Selecting
        self.select_the_upgraded_val(is_selected,curr_val,min_val,max_val,cost_to_upgrade_by_one_unit)

        #Scrolling the items selector.
        if(self.curr_from_bottom_pos!=None):
            self.curr_from_bottom_pos+=scroll_settings_screen           #To account for when you select a value and so that it continues to scroll wrt to the item box in the page.

        #Updating the cost.
        cost_to_upgrade=0
        if(self.has_been_selected):
            cost_to_upgrade=self.cost_for_upgrading

        #Displaying the name, the line(to select new value)
        self.display_name(display_surf,attr_name,cost_to_upgrade,curr_val,is_selected)
        self.display_bar(display_surf,curr_val,min_val,max_val,is_selected,scroll_settings_screen)

    #A method to make a serializable copy of the data
    def saveItem(self):
        itemData=self.__dict__.copy()
        itemData['rect']=rect_to_dict(self.rect)
        itemData['font']=font_to_dict(self.font)
        itemData['top']=vect2_to_dict(self.top)
        itemData['bottom']=vect2_to_dict(self.bottom)
        itemData['curr_rect']=rect_to_dict(self.curr_rect)
        itemData['mouse_collider_rect']=rect_to_dict(self.mouse_collider_rect)
        return itemData
    
    #A method to load the item using the saved data.
    def useSavedData(self,itemData):
        self.curr_rect=pygame.rect.Rect(itemData['curr_rect']['x'],itemData['curr_rect']['y'],itemData['curr_rect']['width'],itemData['curr_rect']['height'])
        self.curr_from_bottom_pos=itemData['curr_from_bottom_pos']
        self.has_been_selected=itemData['has_been_selected']
        self.cost_for_upgrading=itemData['cost_for_upgrading']
        self.mouse_collider_rect=pygame.rect.Rect(itemData['mouse_collider_rect']['x'],itemData['mouse_collider_rect']['y'],itemData['mouse_collider_rect']['width'],itemData['mouse_collider_rect']['height'])