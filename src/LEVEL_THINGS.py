from Settings import *
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

#This map contains the information related to each level that has to be displayed or shown.

#This is used only when the game is started.
game_lore=[
    "In a world with advanced technology, evil organizations, adventurers and more, 3 scientists are curious about the recently discovered ruins which are rumored to hold an ancient device, capable of travelling through space and time.", "Intrigued by these rumors, the scientists decide to explore the ruins before anyone else and try to unlock the secrets to time-travelling. They bring with them a famous adventurer, who has survived all by himself in many islands and discovered hidden treasures.", "To their surprise however, they lose each other while exploring the island and each gets sent to a different ruin entrance. The protagonist, an old friend of theirs and the number one adventurer in the world(who's now retired), gets a call from one of these scientist's colleagues asking him to rescue to them.", "The protagonist, with no hesitation, sets out to the island in hopes of rescuing them."
]
game_info=[
    "Player Movement Controls: [w,a,s,d] or [up,left,down,right arrow keys]",
    "Player attack: [space bar]\n Player magic: [left_control]",
    "Switch weapon: [n,p] for next and previous weapon\nSwitch magic: [m,o] for next and previous magic",
    "Camera Movement: [b] for box camera, [i,j,k,l] for keyboard camera movement, hover mouse close to screen end for mouse camera movement",
    "Pause screen: [esc] for pause screen. Another esc to go back to the game from pause screen",
    "Dialogs: [g] to view the Dialog History, Click on one of the visible dialogs to view the entire dialog box.",
    "Inventory: [v] to go into the inventory, [t],[y] to select previous and next item in the inventory. [e] to consume the item.",
    "Settings: Current weapon, magic information is displayed. Can purchase upgrades only if you have sufficient exp.",
]


EVENT_CODES=['BeforeKillingAnyEnemy','AfterKillingAllEnemy','PortalCollision','FoundKeyPressingE','DestroyedRuin3Once']
RUIN0_ENTRY_CODE=106

start_msg={         #The key is the level id.
    '0':["Find the code to save the scientist.\n'To the one who explores this island, the key shall reveal itself'\nPress '9' near the portal to type the code."],              #Have to constantly check if the player is colliding with a particular rect and pressing 9.
    '1':["Save the Scientist by unlocking the cage.\nTalk with the scientist to get a clue where the key is."],                                                                 #Event handled when level's enemy counter reaches 0.
    '2':["Save the scientist from the ruins.\nTalk with the scientist to help him escape."],
    '3':["Save the scientist and leave these ruins."],
}

Scientist1={    #Is Stuck in Ruin1
    'dialog':{ EVENT_CODES[0]: ['Please Find the key to this cell.',
                                'I Think the key should be somewhere here. Can you check around',
                                'Hmmm, Maybe the cage will unlock if you destroy all the enemies in this room.',
                                'Can you please help me.'
                            ],
                EVENT_CODES[1]: ['Thank you so much for saving me.',
                                'Can you also save the other 2.',
                                'I think each of us got taken into different ruins',
                                'I wish you best of luck'
                            ]
            }
}

Scientist2={
    'dialog':{
        EVENT_CODES[0]:['Please save me from these Ruins.',
                        'I Think you need to find the hidden Key.',
                        "I don't know the exact location but press 'E' when near it."
        ],
        EVENT_CODES[1]:['Wow, You killed all the zombies.'],
        EVENT_CODES[3]:['Finally, You have found the key.',
                        'Thank you so much for saving me'
        ]
    }
}

Scientist3={
    'dialog':{
        EVENT_CODES[0]:["WELL, WELL, WELL... Look who's here\nLooks like you've saved the other 2.",
                        "I really wished you didn't make it this far.",
                        "I guess it is what it is.",
                        "Time for you to die.",
                        "Kill All The Enemies within the Time Limit."
        ],
        EVENT_CODES[1]:["AGGHHHHHHH... You have foiled my plans.",
                        "I will be back"
        ],
        EVENT_CODES[4]:["Sure You've Killed them. But did you really think that killing them once would be enough?",
                        "Destroy the enemies once again to clear the level."
        ]
    }
}



class LEVEL_INFO:
    def __init__(self,level_id):
        self.level_id=level_id
        self.start_msg=start_msg[str(level_id)]

        self.codeEnterImg=pygame.image.load(os.path.join(GRAPHICS_DIR_PATH,"Code_Enter_image.png"))
        self.codeEnterImg_rect=self.codeEnterImg.get_rect(topleft=(200,200))
        pass

    #A method to get the correct code from the player.
    def getCorrectCodeFromPlayer(self):
        bg=pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
        bg.fill('black')
        bg.blit(self.codeEnterImg,self.codeEnterImg_rect.topleft)
        display_surf=pygame.display.get_surface()
        rectangles=[]
        rectangles_left=[278,568,860]
        rectangle_top=[325,413,499]
        rectangle_sizes=60
        for top in rectangle_top:
            for left in rectangles_left:
                rectangle=pygame.rect.Rect(left,top,rectangle_sizes,rectangle_sizes)
                rectangles.append(rectangle)
        rectangles.append(pygame.rect.Rect(568,582,rectangle_sizes,rectangle_sizes))

        enter_button=pygame.rect.Rect(860,582,rectangle_sizes,rectangle_sizes)
        clear_button=pygame.rect.Rect(278,582,rectangle_sizes,rectangle_sizes)
        pass_code=""
        font=pygame.font.Font(None,60)

        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        if(pass_code==""):
                            return 1
                        return int(pass_code)
                    elif event.key==pygame.K_BACKSPACE:
                        pass_code=pass_code[:-1]
                    elif event.key>=pygame.K_0 and event.key<=pygame.K_9:
                        num_entered=str(event.key-pygame.K_0)
                        pass_code+=num_entered
                if event.type==pygame.MOUSEBUTTONDOWN:
                    mouse_pos=pygame.mouse.get_pos()
                    for index,rect in enumerate(rectangles):
                        if rect.collidepoint(mouse_pos):
                            index+=1
                            if(index==10):
                                index=0
                            pass_code+=str(index)
                    if clear_button.collidepoint(mouse_pos):
                        pass_code=pass_code[:-1]
                    if enter_button.collidepoint(mouse_pos):
                        if(pass_code==""):
                            return 1
                        return int(pass_code)
                    pass
            display_surf.blit(bg,(0,0))
            pass_code_surf=font.render(pass_code,True,'black')
            pass_code_rect=pass_code_surf.get_rect(topright=(932,228)) #pygame.rect.Rect(932,228,pass)
            display_surf.blit(pass_code_surf,pass_code_rect.topleft)
            pygame.display.flip()
            
        pass

    #A method to handle the different events that happen in the game.
    def handle_event(self,event_code,level=None):
        if event_code==EVENT_CODES[0]:
            pass
        elif event_code==EVENT_CODES[1]:        #Handling the event of when player has killed all enemies.
            if level:
                if not level.has_triggered_event1 and level.level_id==1:        #Display the messages the messages and kill the gate sprites.
                    #Display the message
                    SaveGameScreen()
                    bg_image=LoadCurrScreen()
                    DISPLAY_DIALOGS(level.level_scientist.dialogs[EVENT_CODES[1]],60,40,SCREEN_WIDTH-100,int(SCREEN_HEIGHT_HALF//2),bg_image)
                    sprite_positions=[]
                    if level.unlockable_gate_sprites:
                        for sprite in level.unlockable_gate_sprites:
                            sprite_positions.append(sprite.rect.center)
                            sprite.kill()
                elif level.level_id==2 and not level.has_triggered_event1:      #Display the messages only.
                    SaveGameScreen()
                    bg_image=LoadCurrScreen()
                    DISPLAY_DIALOGS(level.level_scientist.dialogs[EVENT_CODES[1]],60,40,SCREEN_WIDTH-100,int(SCREEN_HEIGHT_HALF//2),bg_image)

                elif not level.has_triggered_event1 and level.level_id==3 and not level.has_triggered_event4:       #Display the messages and recreate the enemies.
                    #Have to recreate the map once.
                    self.enemy_sprites=pygame.sprite.Group()
                    self.enemy_counter=0
                    self.visible_sprites=pygame.sprite.Group()
                    self.obstacle_sprites=pygame.sprite.Group()
                    self.transport_sprites=pygame.sprite.Group()
                    self.attack_sprites=pygame.sprite.Group()
                    self.loot_drops=pygame.sprite.Group()
                    self.unlockable_gate_sprites=pygame.sprite.Group()

                    player_prev_pos=level.player.rect.topleft
                    level.createMap()
                    SaveGameScreen()
                    bg_image=LoadCurrScreen()
                    DISPLAY_DIALOGS(level.level_scientist.dialogs[EVENT_CODES[4]],60,40,SCREEN_WIDTH-100,int(SCREEN_HEIGHT_HALF//2),bg_image)
                    level.player.rect.topleft=player_prev_pos

                    level.has_triggered_event4=True

                elif level.has_triggered_event1 and level.level_id==3 and level.has_triggered_event4:       #Display the game finished.
                    SaveGameScreen()
                    bg_image=LoadCurrScreen()
                    DISPLAY_DIALOGS(["AGHHHH I WILL GET YOU NEXT TIME...."],60,40,SCREEN_WIDTH-100,int(SCREEN_HEIGHT_HALF//2),bg_image)
                    level.game_finished=True

        elif event_code==EVENT_CODES[2]:        #Handling the event of transporting to other maps only if the condition is satisfied.
            if level!=None:
                if self.level_id==0:
                    if level.player.rect.colliderect(Ruin0_rect_Ruin2):
                        if level.player.has_cleared_maps[1]==True:
                            return 1
                        else:
                            SaveGameScreen()
                            bg_image=LoadCurrScreen()
                            DISPLAY_DIALOGS(["Please Clear Ruin1 Before entering this Ruin."],60,40,SCREEN_WIDTH-100,int(SCREEN_HEIGHT_HALF//2),bg_image=bg_image)
                            return 0
                        pass
                    elif level.player.rect.colliderect(Ruin0_rect_Ruin3):
                        if level.player.has_cleared_maps[2]==True:
                            return 1
                        else:
                            SaveGameScreen()
                            bg_image=LoadCurrScreen()
                            DISPLAY_DIALOGS(["Please Clear Ruin2 Before entering this Ruin."],60,40,SCREEN_WIDTH-100,int(SCREEN_HEIGHT_HALF//2),bg_image=bg_image)
                            return 0
                    elif level.player.has_entered_correct_code==False:
                        SaveGameScreen()
                        bg_image=LoadCurrScreen()
                        if level.player.rect.colliderect(Ruin0_rect_enterCode) and pygame.key.get_pressed()[pygame.K_9]:
                            code=self.getCorrectCodeFromPlayer()
                            if(code!=RUIN0_ENTRY_CODE):
                                DISPLAY_DIALOGS(["You have entered the Wrong Code. Dash into the portal while pressing '9' and try again\n(The code is a 3-digit code.)","Hint: The Seas are vast and have yet to be explored."],60,40,SCREEN_WIDTH-100,int(SCREEN_HEIGHT_HALF//2),bg_image=bg_image)
                                return 0
                            else:
                                level.player.has_entered_correct_code=True
                                return 1        #Indicates that the map should be changed. The map will be chosen in Game.py
                    
                        pass

                elif self.level_id==1:
                    if level.player.rect.colliderect(Ruin1_rect_Ruin0) and level.player.has_cleared_maps[1]==False:
                        SaveGameScreen()
                        bg_image=LoadCurrScreen()
                        DISPLAY_DIALOGS(["Please Clear This Ruin Before Moving Back to the Island."],60,40,SCREEN_WIDTH-100,int(SCREEN_HEIGHT_HALF//2),bg_image=bg_image)
                    pass
                elif self.level_id==2:
                    if level.player.rect.colliderect(Ruin2_rect_Ruin0) and level.player.has_cleared_maps[2]==False:
                        SaveGameScreen()
                        bg_image=LoadCurrScreen()
                        DISPLAY_DIALOGS(["Please Clear This Ruin Before Moving Back to the Island."],60,40,SCREEN_WIDTH-100,int(SCREEN_HEIGHT_HALF//2),bg_image=bg_image)
                    pass
                elif self.level_id==3:
                    if level.player.rect.colliderect(Ruin3_rect_Ruin0) and level.player.has_cleared_maps[3]==False:
                        SaveGameScreen()
                        bg_image=LoadCurrScreen()
                        DISPLAY_DIALOGS(["Please Clear This Ruin Before Moving Back to the Island."],60,40,SCREEN_WIDTH-100,int(SCREEN_HEIGHT_HALF//2),bg_image=bg_image)
                    pass
            return 1
        else:
            pass
        pass


class Scientist(pygame.sprite.Sprite):
    def __init__(self,pos,groups,scientist_id):
        super().__init__(groups)
        self.pos=pos
        self.scientist_id=scientist_id
        self.graphics_path=os.path.join(GRAPHICS_DIR_PATH,"SCIENTISTS",f'Scientist{self.scientist_id}')

        self.img=pygame.image.load(os.path.join(self.graphics_path,f'Scientist{self.scientist_id}.png'))
        self.rect=self.img.get_rect(topleft=pos)

        self.speed=0

        self.dialogs={}

        #Variables for letting the scientist to escape from the Level.
        self.shd_escape_from_ruin=False
        self.end_rect_topleft=None
        self.escape_path=[]

        self.finder=AStarFinder()

        self.initialize_dialogs()

        #Direction vectors.
        self.direction=pygame.math.Vector2(0,0)

    def initialize_dialogs(self):
        if self.scientist_id==1:
            self.dialogs=Scientist1["dialog"]
            self.end_rect_topleft=(Ruin1_rect_Ruin0.left,Ruin1_rect_Ruin0.top+BASE_SIZE)
            self.speed=8        #Changing the speed might result in bad behaviour of movement(continuous movement between 2 spots only)
        elif self.scientist_id==2:
            self.dialogs=Scientist2["dialog"]
            self.end_rect_topleft=(Ruin2_rect_Ruin0.left,Ruin1_rect_Ruin0.top+BASE_SIZE)
            self.speed=8        #Changing the speed might result in bad behaviour of movement(continuous movement between 2 spots only)
        elif self.scientist_id==3:
            self.dialogs=Scientist3["dialog"]
            self.end_rect_topleft=Ruin3_rect_Ruin0.topleft
            self.speed=8

    def initialize_escape_path(self,level):
        start_node_row=int(self.rect.top//BASE_SIZE)
        start_node_col=int(self.rect.left//BASE_SIZE)

        end_node_col=int(self.end_rect_topleft[0]//BASE_SIZE)
        end_node_row=int(self.end_rect_topleft[1]//BASE_SIZE)

        grid=Grid(matrix=level.detection_tiles)
        start_node=grid.node(start_node_col,start_node_row)
        end_node=grid.node(end_node_col,end_node_row)

        path,runs=self.finder.find_path(start_node,end_node,grid)

        self.escape_path=path
        if len(path)>0:
            self.escape_path.pop(0)

    def draw(self,display_surf,offset):
        newpos=self.rect.topleft-offset
        display_surf.blit(self.img,newpos)

    #A method to set the direction of the scientist to move along the escape path, if any.
    def set_direction(self):
        if len(self.escape_path)>1:
            next_node=self.escape_path[0]
            if (self.rect.left//BASE_SIZE == next_node.x) and (self.rect.top//BASE_SIZE == next_node.y):
                self.escape_path.pop(0)

            next_node=self.escape_path[0]
            next_cell_col=next_node.x*BASE_SIZE
            next_cell_row=next_node.y*BASE_SIZE
            self.direction.x=next_cell_col-self.rect.x
            self.direction.y=next_cell_row-self.rect.y

            if self.direction.magnitude()!=0:
                self.direction=self.direction.normalize()
        else:
            self.kill()
        pass

    #Moving the scientist along the escape path if possible.
    def move(self):
        if self.shd_escape_from_ruin==True:
            self.set_direction()
            self.rect.x=self.rect.x+self.direction.x*self.speed
            self.rect.y=self.rect.y+self.direction.y*self.speed

    def update(self,display_surf,offset):
        if self.shd_escape_from_ruin==True:
            self.move()
        self.draw(display_surf,offset)