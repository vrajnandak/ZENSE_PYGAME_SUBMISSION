import pygame
from Settings import *

#Each button will be basically 2 rectangles with the top rectangle having the text and the bottom being a lighter shade of the background color.
class Button:
    def __init__(self,pos,width,height,text,font,start_left_pos,text_color=TEXT_COLOR,bg_color=BUTTON_BACKGROUND_COLOR,hover_color=BUTTON_HOVER_COLOR,click_color=BUTTON_CLICK_COLOR):
        #Initializing the arguments.
        self.pos=pos
        self.width=width
        self.height=height
        self.text=text
        self.font=font
        self.start_left_pos=start_left_pos
        self.text_color=text_color
        self.normal_bg_color=bg_color
        self.hover_color=hover_color
        self.click_color=click_color

        #Rendering the text into a surface, getting it's width,height(inorder to position the surface properly)
        self.text_surf=self.font.render(text,True,self.text_color)          #Renders 'self.text' with anti-aliasing(smooth appearance of text) and text is of color 'self.text_color'.
        self.text_width=self.text_surf.get_width()
        self.text_height=self.text_surf.get_height()
        self.font=None          #As font objects are not serializable.

        #Rectangles
        self.border_radius=int(min(self.width,self.height)//3)
        self.border_thickness=3
            #Top Rectangle - Is the smaller rectangle, contains the text
        self.top_color=self.normal_bg_color
        self.top_rect=pygame.rect.Rect(self.pos,(self.width,(4*self.height)//5))           #The color to be drawn on this rect will be chosen in the draw() method itself.
        self.top_rect_bottom_left_radius=self.border_radius//5
        self.top_rect_bottom_right_radius=int(self.border_radius*1.5)
            #Default Top rectangle values.
        self.default_top_rect_height=(4*self.height)//5
        self.default_top_rect_bottom_left_radius=self.border_radius//5
        self.default_top_rect_bottom_right_radius=int(self.border_radius*1.5)
            #Bottom Rectangle - Is the larger rectangle.
        self.bottom_rect=pygame.rect.Rect(self.pos,(self.width,self.height))               #The color,border-radius to be drawn on this rect will be chosen in the draw() method itself
        self.bottom_color=tuple(min(c + 50, 255) for c in self.top_color)
        self.bottom_rect_bottom_left_radius=self.border_radius
        self.bottom_rect_bottom_right_radius=self.border_radius

        #Animation variables - To make the button appear from left to it's specified position. It has 2 phases (1st from outside screen to a right position) and (2nd from right position to specified position)
        self.animation_phase=1                          #Will be 'None' when the animation is done.
        self.curr_left=self.start_left_pos
            #Phase 1 variables.
        self.phase1_left_pos=self.pos[0]+50
        self.pase1_animation_movement_speed=1           #Speed positive as box moves to right.
            #Phase 2 variables.
        self.phase2_left_pos=self.pos[0]
        self.phase2_animate_movement_speed=-1.8         #Speed negative as box moves to left.

    #A method to apply the animation of the button.
    def starting_button_animation(self):
        #The button_sliding animation. Since the rect's need to have int values, we cannot directly increment them with a decimal value(Hence the need for self.curr_left).
        if(self.animation_phase==1):
            if(self.curr_left<self.phase1_left_pos):
                self.curr_left+=self.pase1_animation_movement_speed
            else:
                self.animation_phase=2

        elif(self.animation_phase==2):
            if(self.curr_left>self.phase2_left_pos):
                self.curr_left+=self.phase2_animate_movement_speed
            else:
                self.animation_phase=None

        self.top_rect.left=self.curr_left
        self.bottom_rect.left=self.curr_left
    
    #Method to change the color of button based on whether or not the mouse is hovering or clicking the button.
    def set_top_color(self):
        mouse_pos=pygame.mouse.get_pos()

        #The default radius values, height of the top and bottom rectangle. Change when the button is clicked.
        self.top_rect.height=self.default_top_rect_height
        self.top_rect_bottom_left_radius=self.default_top_rect_bottom_left_radius
        self.top_rect_bottom_right_radius=self.default_top_rect_bottom_right_radius

        if(self.bottom_rect.collidepoint(mouse_pos)):
            self.top_color=self.hover_color
            if(pygame.mouse.get_pressed()[0]):      #If you've done a left click
                self.top_color=self.click_color
                self.top_rect.height=self.bottom_rect.height
                self.top_rect_bottom_left_radius=self.bottom_rect_bottom_left_radius
                self.top_rect_bottom_right_radius=self.bottom_rect_bottom_right_radius
        else:
            self.top_color=self.normal_bg_color
    
    #A method to update the button's information or apply scroll or animate etc.
    def update(self,display_surf,scroll_settings_screen):
        #Applying the scroll
        self.scroll(scroll_settings_screen)

        self.starting_button_animation()

        #Setting the top color based on mouse position (Color for hover, click, or normal background color)
        self.set_top_color()                                                    #We ignore the return value as we only want to set the top_color here.
        self.bottom_color=tuple(min(c + 50, 255) for c in self.top_color)       #Updating the bottom color to be a lighter shade of top_color.

        self.draw(display_surf)

    #A method to draw the button.
    def draw(self,display_surf):
        #Drawing the Bottom rectangle. The '0' represents to fill the self.bottom_rect with self.bottom_color.
        pygame.draw.rect(display_surf, self.bottom_color, self.bottom_rect,0,self.border_radius,border_bottom_left_radius=self.bottom_rect_bottom_left_radius,border_bottom_right_radius=self.bottom_rect_bottom_right_radius)
        #Drawing the top rectangle.
        pygame.draw.rect(display_surf, self.top_color, self.top_rect,0,self.border_radius,border_bottom_left_radius=self.top_rect_bottom_left_radius,border_bottom_right_radius=self.top_rect_bottom_right_radius)

        #Drawing the text on the button.
        display_surf.blit(self.text_surf,(self.top_rect.centerx-self.text_width//2,self.top_rect.centery-self.text_height//3))

        #Drawing the border. The '2'(is >0) means to draw a border with the color (0,0,0) i.e., black.
        pygame.draw.rect(display_surf,(0,0,0),self.bottom_rect,self.border_thickness,self.border_radius)

    #A method to add scroll to the button by changing the top of both the bottom and top rectangles.
    def scroll(self,scroll_settings_screen):
        for rect in [self.bottom_rect,self.top_rect]:
            rect.top+=scroll_settings_screen