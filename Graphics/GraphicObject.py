import pygame

## Container for a single frame in an animation.
#
#  Essentially is a linked list of frames.
#
#  This may not be needed if we are not having sprites...
class AnimationFrame(object):
    
    ## Constructor.
    #  @param image Image data.
    #  @param delay Delay before proceeding to next frame, in seconds.
    #  @param nextFrame Reference to next AnimationFrame. Set to @c None if this is the last frame.
    #  @param number Frame number.
    def __init__(self,image,delay,nextFrame,number):
        self.image = image
        self.delay = delay
        self.nextFrame = nextFrame
        self.number = number
        self.count = 0
    
    ## Returns this frame's image data
    def getImage(self):
        return self.image
    
    ## Returns the delay before proceeding to the next frame, in seconds.
    def getDelay(self):
        return self.delay
    
    ## Returns the next frame.
    def getNextFrame(self):
        return self.nextFrame
    
    ## Returns this frame's frame number.
    def getNumber(self):
        return self.number
    
    ## Updates this frame and returns the current frame.
    #  @param tick Time that has passed since last clock cycle in seconds.
    def update(self,tick):
        self.count += tick
        if self.count >= self.delay:
            self.count=0
            return self.nextFrame
        else:
            return self
    
    ## Resets frame to original state.
    def reset(self):
        self.count = 0

## Container for a sequence of frames.
#
#  Essentially is a linked list of Animations.
#
#  This may not be needed if we are not having sprites...
class Animation(object):
    
    ## Constructor.
    #  @param firstFrame First AnimationFrame in the sequence.
    #  @param nextAnimation Reference to next Animation. Set to @c None if this animation should repeat.
    #  @param name Name of animation.
    def __init__(self,firstFrame,nextAnimation,name):
        self.firstFrame = firstFrame
        self.nextAnimation = nextAnimation
        self.frame = self.firstFrame
        self.name = name
    
    ## Adds a frame to the animation.
    #  @param frame Frame to be added.
    def addFrame(self,frame):
        if self.firstFrame == None:
            self.firstFrame = frame
            self.frame = self.firstFrame
        else:
            temp = self.firstFrame
            while temp.nextFrame != None:
                temp = temp.nextFrame
            temp.nextFrame = frame
    
    ## Returns a list of AnimationFrame objects in the animation.
    def getFrames(self):
        temp = self.firstFrame
        if temp == None:
            return []
        else:
            ret = [temp]
            while temp.nextFrame != None:
                temp = temp.nextFrame
                ret.append(temp)
            return ret
    
    ## Returns the current frame number.
    def getFrame(self):
        return self.frame.number + (float(self.frame.count)/self.frame.delay)
    
    ## Returns the next animation.
    def getNextAnimation(self):
        return self.nextAnimation
    
    ## Returns this animation's name.
    def getName(self):
        return self.name
    
    ## Sets the current frame number.
    def setFrame(self,frame):
        temp = self.firstFrame
        while temp.number != int(frame):
            if temp.nextFrame == None:
                if temp.number<int(frame):
                    self.frame=self.firstFrame
                    return
            temp = temp.nextFrame
        self.frame = temp
        self.frame.count = (frame-int(frame))*self.frame.delay
    
    ## Sets the next animation, useful for manual linking.
    def setNextAnimation(self,animation):
        self.nextAnimation = animation
    
    ## Updates this animation and returns the current animation.
    #
    #  Also updates the current frame.
    #  @param tick Time that has passed since last clock cycle in seconds.
    def update(self,tick):
        self.frame = self.frame.update(tick)
        if self.frame == None:
            self.frame = self.firstFrame
            if self.nextAnimation == None:
                return self
            else:
                return self.nextAnimation
        else:
            return self
    
    ## Resets animation to original state.
    #
    #  Also resets current frame to original state.
    def reset(self):
        self.frame.reset()
        self.frame = self.firstFrame
    
    ## Returns the current frame's image.
    def getSprite(self):
        return self.frame.image

## An object that contains graphics information.
#
#  Anything that the character can interact with should use this.
class GraphicObject(object):
    
    ## Constructor.
    #  @param animations A dictionary of animations
    #  @param parent Reference to parent object, ie. the Player class for the player's graphic object.
    #  @param state Starting state of the object.
    #  @param rot The rotation of the graphic object in radians.
    #  @param layer Sets draw order for objects.  Objects in layer 1 render first, then objects in layer 0, etc.
    #
    #  @todo Rotation not yet implemented
    def __init__(self,animations,parent=None,state="Idle",rot=0,layer=0):
        self.animations = animations
        self.currentAnimation = animations[state]
        
        self.state = state
        self.rot = rot
        self.layer = layer
        self.parent= parent
        
        #Keeping x and y as separate variables is more efficent than tuples and lists when tested with adding, subtracting, and defining.
        self.x = 0
        self.y = 0
    
    ## Sets where the object should be drawn.
    #
    #  Should be integers, as partial pixels mean nothing to pygame.
    def setPos(self,pos):
        self.x=pos[0]
        self.y=pos[1]
    
    ## Returns width of current frame.
    def getWidth(self):
        return self.getSprite().get_width()
    
    ## Returns height of current frame.
    def getHeight(self):
        return self.getSprite().get_height()
    
    ## Returns where the object is being drawn.
    def getPos(self):
        return [self.x,self.y]
    
    ## Returns a reference to the parent object.
    def getParent(self):
        return self.parent
    
    ## Returns the x portion of position.
    def getX(self):
        return self.x
    
    ## Returns the y portion of position.
    def getY(self):
        return self.y
    
    ## Sets the current state of the object.
    def setState(self,state):
        self.state=state
        self.currentAnimation.reset()
        self.currentAnimation = self.animations[self.state]
    
    ## Returns the current frame's image.
    def getSprite(self):
        return self.currentAnimation.getSprite()
    
    ## Returns the current frame number.
    def getFrame(self):
        return self.currentAnimation.getFrame()
    
    ## Sets the current frame number.
    def setFrame(self,frame):
        self.currentAnimation.setFrame(frame)
    
    ## Updates this object.
    #  @param tick Time that has passed since last clock cycle in seconds.
    def update(self,tick):
        self.currentAnimation = self.currentAnimation.update(tick)

## A convenience function that creates a GraphicObject that is a colored square.
#
#  @param size How long each side of the square should be.
#  @param color An RGB tuple describing what color the square should be.
#  @param outline Set to @c True for a 1 pixel outline.
#  @param outlineColor What color the outline should be.
def createSquareGraphicObject(size,color,outline=False,outlineColor=None):
    image = pygame.Surface((size,size))
    if outline:
        image.fill(outlineColor)
        image.fill(color,[1,1,size-2,size-2])
    else:
        image.fill(color)
    animations = {"Idle":Animation(AnimationFrame(image,1,None,1),None,"Idle")}
    return GraphicObject(animations)

## A convenience function that creates a GraphicObject that is a colored square.
#
#  @param size A tuple describing the size of the rectangle.
#  @param color An RGB tuple describing what color the square should be.
#  @param outline Set to @c True for a 1 pixel outline.
#  @param outlineColor What color the outline should be.
def createRectGraphicObject(size,color,outline=False,outlineColor=None):
    image = pygame.Surface(size)
    if outline:
        image.fill(outlineColor)
        image.fill(color,[1,1,size[0]-2,size[1]-2])
    else:
        image.fill(color)
    animations = {"Idle":Animation(AnimationFrame(image,1,None,1),None,"Idle")}
    return GraphicObject(animations)
