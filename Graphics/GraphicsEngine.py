import pygame

## Sort function for sorting by y
#
#  Allows things that have smallers y values to be drawn first.
def sortY(a):
    #if int(a.getPos()[1])!=a.getPos()[1]:      #  This is commented out for the sake of the example, because it uses partial pixels.
    #   print "Sort Error: "+str(type(a))
    return int(a.getPos()[1]+a.getHeight())

## Graphics Engine for main portion of game.
#
#  Only one instance of the graphics engine should be running at any given time.
class GraphicsEngine(object):
    
    ## Constructor.
    #  @param screen A reference to either a Pygame screen object or a scaledScreen.
    #  @param isScaled If @c screen is a scaledScreen, then should be @c True.
    def __init__(self,screen):
        self.screen = screen
        self.screenWidth = screen.get_width()
        self.screenHeight = screen.get_height()
        self.objects = []
        self.player = None
        self.background = pygame.surface.Surface([0,0])
        self.cameraPosX = 0
        self.cameraPosY = 0
        self.focus=None
        self.levelName=None
    
    ## Add an object.
    #
    #  Adds an object to the list of objects to be drawn and updated.
    #  @param Object GraphicObject to be added.
    def addObject(self,Object):
        self.objects.append(Object)
    
    ## Clears object list.
    def clearObjects(self):
        self.objects = []
    
    ## Sets who is the player.
    #  @param Player The player's GraphicObject.
    def setPlayer(self,player):
        self.player = player
    
    ## Sets the focus of the camera.
    #
    #  Sets an object for the camera to follow.
    #  @param focus GraphicObject for camera to follow.
    def setFocus(self,focus):
        self.focus = focus
    
    ## Sets the name of the current area.
    #
    #  @param name String that contains the name of the level.
    def setLevelName(self,name):
        self.levelName=name
    
    ## Sets the background.
    #
    #  @param background pygame.Surface that will be displayed behind all other objects.
    def setBackground(self,background):
        self.background = background
    
    ## Returns the screen
    #
    #  For passing the screen to the BattleGraphicsEngine, not for drawing things to the screen without using the engine.
    def getScreen(self):
        return self.screen
    
    ## Updates objects
    #
    #  Updates all objects, draws them in the correct order and in the correct place in relation to the camera.
    #  @param tick Time that has passed since last clock cycle, in seconds.
    def update(self,tick):
        self.screen.fill((0,0,0))
        
        if self.focus != None:
            if self.background.get_width()>self.screenWidth:
                offsetX = self.focus.getX()+(self.focus.getWidth()/2)-(self.screenWidth/2)
            else:
                offsetX = 0
            if self.background.get_height()>self.screenHeight:
                offsetY = self.focus.getY()+(self.focus.getHeight()/2)-(self.screenHeight/2)
            else:
                offsetY = 0
        else:
            offsetX=0
            offsetY=0
        
        for Object in self.objects:
            Object.update(tick)
        
        self.player.update(tick)
        self.objects.append(self.player)
        
        self.screen.blit(self.background,(self.cameraPosX-offsetX,self.cameraPosY-offsetY))
        for go in self.objects:
            if go.layer<0:
                self.screen.blit(go.getSprite(),(go.getX()-offsetX,go.getY()-offsetY))
        
        self.objects.sort(key=sortY,reverse=False)
        for go in self.objects:
            if go.layer==0:
                self.screen.blit(go.getSprite(),(go.getX()-offsetX,go.getY()-offsetY))
        
        for go in self.objects:
            if go.layer==1:
                self.screen.blit(go.getSprite(),(go.getX()-offsetX,go.getY()-offsetY))
        
        self.objects.remove(self.player)
        
        for go in self.objects:
            if go.layer==2:
                self.screen.blit(go.getSprite(),(go.getX()-offsetX,go.getY()-offsetY))
        
        pygame.display.update()
