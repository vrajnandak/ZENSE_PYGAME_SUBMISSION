from Settings import *

class CollisionHelper:
    def __init__(self,level):
        self.the_level=level

    #A method to get the max number of pixels that the player can move without having collision.
    def get_pixel_counter(self,entity,sprite,movement,distance_moved,is_horizontal,is_vertical):
        lower_lim=0
        upper_lim=abs(int(distance_moved))
        left=lower_lim
        right=upper_lim
        while left<=right:
            mid=left+(right-left)//2
            #If you were to calculate the offset for only horizontal movement then you would'nt want to consider the movement for y-axis and similarily vice-versa. So, this variable offest term that we're adding would be the same if written separately for horizontal, vertical collisions but since we've wrote them in one function, we set them to 0 appropriately.
            offset_x=sprite.rect.left-entity.rect.left-mid*movement*is_horizontal      #Considering only to add horizontal movement.
            offset_y=sprite.rect.top-entity.rect.top-mid*movement*is_vertical          #Considering only to add vertical movement.
            offset=(offset_x,offset_y)
            if entity.mask.overlap(sprite.mask,offset):
                right=mid-1
            else:
                left=mid+1
        return right
    
    #A method to set the entity as close as possible to the sprite in question, without having collision.
    def handle_horizontal_collision(self,entity,sprite,speed):
        movement= 1 if entity.direction.x > 0 else -1
        distance_moved=entity.direction.x*speed
        entity.rect.x-=distance_moved        #Undoing the added direction in x-axis as this caused mask collision.
        can_move_pixel=self.get_pixel_counter(entity,sprite,movement,distance_moved,1,0)
        new_distance_moved=movement*can_move_pixel
        entity.rect.x+=new_distance_moved

    def handle_vertical_collision(self,entity,sprite,speed):
        movement=1 if entity.direction.y > 0 else -1
        distance_moved=entity.direction.y*speed
        entity.rect.y-=distance_moved        #Undoing the added direction in y-axis as this caused the mask collision.
        can_move_pixel=self.get_pixel_counter(entity,sprite,movement,distance_moved,0,1)
        new_distance_moved=movement*can_move_pixel
        entity.rect.y+=new_distance_moved

    #Returns whether or not a collision with the transportation portal has occured.
    def handle_spritegroup_collision(self,entity,speed,direction, spriteGroup, is_transportation_portal,collision_type="Any"):
        for sprite in spriteGroup:
            if sprite.rect.colliderect(entity.rect) and entity.rect.topleft!=sprite.rect.topleft:       #The 2nd condition is to eliminate an enemy sprite checking collision against itself. This is quite important because without this, an enemy sprite would trigger movement by itself when the player is in the attack radius, leading to absurd movement.
                if(is_transportation_portal):
                    return 1
                elif(collision_type=="rect_collision"):
                    if(direction=="Horizontal"):
                        entity.rect.x-=entity.direction.x*speed
                    elif(direction=="Vertical"):
                        entity.rect.y-=entity.direction.y*speed
                elif(entity.mask.overlap(sprite.mask,(sprite.rect.left-entity.rect.left, sprite.rect.top-entity.rect.top))):
                    if(direction=="Horizontal"):
                        self.handle_horizontal_collision(entity,sprite,speed)
                    elif(direction=="Vertical"):
                        self.handle_vertical_collision(entity,sprite,speed)
        return 0                    #Indicates that the tiles have not been updated by the collision detector.