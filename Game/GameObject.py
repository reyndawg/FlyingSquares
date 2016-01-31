## This class contains the information for each object in the game that can be interacted with.
class GameObject(object):
    
    ## Constructor.
    #
    #  @param graphicObject The graphics.GraphicObject that is associated with this object.
    #  @param hp How many hit points this 
    #  @param pos A list describing the absolute position of this object, [x,y].
    #  @param speed Top speed in pixels per second this object can travel at.
    #  @param hitBox A pygame.Rect object that describes the area in which it can be hit and take damage.
    #  @param ally Set to @c True if this object is not an enemy but an ally to the player.
    def __init__(self,graphicObject,hp,pos,speed,hitBox,ally=False):
        self.graphicObject = graphicObject
        self.hp = hp
        self.x = pos[0]
        self.y = pos[1]
        self.graphicObject.setPos(pos)
        self.speed = speed
        self.hitBox = hitBox
        self.ally = ally
        
        self.velx = 0.0
        self.vely = 0.0
    
    ## Returns this object's graphics.GraphicObject.
    def getGraphicObject(self):
        return self.graphicObject
    
    ## Returns this object's health.
    def getHp(self):
        return self.hp
    
    ## Returns the absolute location of this object.
    def getPos(self):
        return [self.x,self.y]
    
    ## Returns the x portion of this object's location.
    def getX(self):
        return self.x
    
    ## Returns the y portion of this object's location.
    def getY(self):
        return self.y
    
    ## Returns the velocity of this object.
    def getVel(self):
        return [self.velx,self.vely]
    
    ## Returns the x portion of this object's velocity.
    def getVelX(self):
        return self.velx
    
    ## Returns the y portion of this object's velocity.
    def getVelY(self):
        return self.vely
    
    ## Returns this object's max speed.
    def getSpeed(self):
        return self.speed
    
    ## Returns this object's hit box.
    def getHitBox(self):
        return self.hitBox
    
    ## Returns @c True if this object is on the player's team, otherwise returns false.
    def isAlly(self):
        return self.ally
    
    ## Sets this object's velocity.
    def setVel(self,vel):
        self.velx = vel[0]
        self.vely = vel[1]
    
    ## Sets where this objects is located.
    def setPos(self,pos):
        self.x = pos[0]
        self.y = pos[1]
        self.graphicObject.setPos(pos)
    
    ## Updates this object.
    def update(self,tick):
        self.x+=self.velx*tick
        self.y+=self.vely*tick
        
        self.graphicObject.setPos([int(self.x),int(self.y)])
