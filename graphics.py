## An object that contains graphics information.
#
#  Anything that the character can interact with should use this.
class GraphicObject(object):
	
	## Constructor.
	#  @param parent Reference to parent object, ie. the Player class for the player's graphic object.
	#  @param state Starting state of the object.
	#  @param rot The rotation of the graphic object in radians.
	#  @param layer Sets draw order for objects.  Objects in layer 1 render first, then objects in layer 0, etc.
	def __init__(self,parent=None,state="Idle",rot=0,layer=0):
		self.state = state
		self.direction = direction	#0-N, 1-E, 2-S, 3-W
		self.layer = layer
		self.parent= parent
		
		#Keeping x and y as separate variables is more efficent than tuples and lists when tested with adding, subtracting, and defining.
		self.x = 0
		self.y = 0
	
	## Sets where the object should be drawn.
	#
	#  Does not change where object is in regards to interactions with objects.
	#  See game.GameObject.setPos().
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
		self.currentAnimation = self.animations[self.state][self.direction]
	
	## Sets the direction the object is facing.
	def setDirection(self,direction):
		self.direction=direction
		f = self.currentAnimation.getFrame()
		self.currentAnimation.reset()
		self.currentAnimation = self.animations[self.state][self.direction]
		self.currentAnimation.setFrame(f)
	
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

## Graphics Engine for main portion of game.
#
#  Only one instance of the graphics engine should be running at any given time.
class GraphicsEngine(object):
	
	## Constructor.
	#  @param screen A reference to either a Pygame screen object or a scaledScreen.
	#  @param isScaled If @c screen is a scaledScreen, then should be @c True.
	def __init__(self,screen,isScaled=False):
		self.screen = screen
		self.isScaled = isScaled
		self.objects = []
		self.Player = None
		self.background = pygame.surface.Surface([0,0])
		self.cameraPosX = 0
		self.cameraPosY = 0
		self.focus=None
		self.talking=None
		self.shop=False
		self.paused=False
		self.inven=False
		self.levelName=None
	
	## Add an object.
	#
	#  Adds an object to the list of objects to be drawn and updated.
	#  @param Object Object to be added.
	def addObject(self,Object):
		self.objects.append(Object)
	
	## Clears object list.
	def clearObjects(self):
		self.objects = []
	
	## Sets who is the player.
	#  @param Player The player.
	def setPlayer(self,Player):
		self.Player = Player
	
	## Sets the focus of the camera.
	#
	#  Sets an object for the camera to follow.
	#  @param focus Object for camera to follow.
	def setFocus(self,focus):
		self.focus = focus
	
	## Sets up the GUI for who the player is talking to.
	#  @param talking The NPC the player is talking to.
	def setTalking(self,talking):
		self.talking=gui.Dialog(talking,self.Player.getParent())
	
	## Exits a conversation.
	def resetTalking(self):
		self.talking=None
	
	## Returns whether or not the player is talking to someone.
	def getTalking(self):
		return self.talking
	
	## Sets which shop the player is interacting with
	def setShop(self,shop):
		self.shop = shop
	
	## Returns which shop the player is interacting with
	def getShop(self):
		return self.shop
	
	## Sets the name of the current area.
	def setLevelName(self,name):
		self.levelName=name
	
	## Toggles whether or not the player's inventory is open.
	def toggleInven(self):
		if self.inven:
			self.inven=False
		else:
			self.inven=gui.InvenMenu(self.Player.getParent(),self.levelName)
	
	## Returns the InvenMenu object for the player.
	def getInven(self):
		return self.inven
	
	## Toggles the pause menu.
	def togglePause(self):
		if self.paused:
			self.paused=False
		else:
			self.paused=gui.PauseMenu()
	
	## Returns the PauseMenu object.
	def getPause(self):
		return self.paused
	
	## Loads a new area
	def loadLevel(self,level):
		self.background = pygame.image.load("Backgrounds/Images/"+level+".png").convert()
	
	## Returns the screen
	#
	#  For passing the screen to the BattleGraphicsEngine, not for drawing things to the screen without using the engine.
	def getScreen(self):
		return self.screen
	
	## Returns if is using a ScaledScreen
	#
	#  For passing to the BattleGraphicsEngine
	def getIsScaled(self):
		return self.isScaled
	
	## Updates objects
	#
	#  Updates all objects, draws them in the correct order and in the correct place in relation to the camera.
	#  @param tick Time that has passed since last clock cycle, in seconds.
	def update(self,tick):
		self.screen.fill((0,0,0))
		
		if self.focus != None:
			if self.background.get_width()>320:
				offsetX = self.focus.getX()+(self.focus.getWidth()/2)-160
			else:
				offsetX = 0
			if self.background.get_height()>240:
				offsetY = self.focus.getY()+(self.focus.getHeight()/2)-120
			else:
				offsetY = 0
		else:
			offsetX=0
			offsetY=0
		
		for Object in self.objects:
			Object.update(tick)
		
		
		self.Player.update(tick)
		self.objects.append(self.Player)
		
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
		
		self.objects.remove(self.Player)
		
		if self.inven:
			if self.inven.update(self.screen,tick):
				self.toggleInven()
		
		if self.shop != False:
			if self.shop.update(self.screen,tick):
				self.shop = False
		
		if self.paused:
			self.paused.update(self.screen,tick)
		
		if self.talking != None:
			if self.talking.update(self.screen,tick)==False:
				if self.talking.getShop() == "Buy":
					self.setShop(gui.ShopBuyMenu(self.Player.getParent(),self.talking.talking.getShop()))
				elif self.talking.getShop() == "Sell":
					self.setShop(gui.ShopSellMenu(self.Player.getParent()))
				self.talking.talking.setTalking(False)
				self.talking=False
		
		for go in self.objects:
			if go.layer==2:
				self.screen.blit(go.getSprite(),(go.getX()-offsetX,go.getY()-offsetY))
		
		if self.isScaled:
			self.screen.update()
		pygame.display.update()
