## Sort function for sorting by y
#
#  Allows things that have smallers y values to be drawn first.
def sortY(a):
	#if int(a.getPos()[1])!=a.getPos()[1]:		#  This is commented out for the sake of the example, because it uses partial pixels.
	#	print "Sort Error: "+str(type(a))
	return int(a.getPos()[1]+a.getHeight())

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

if __name__ == "__main__":								# Example code below:
	import pygame
	from pygame.locals import *
	pygame.init()
	background = pygame.Surface([640,480])				# Make some background image, would normally get from file?
	background.fill((127,127,255))						#   It will be light blue for now
	screen = pygame.display.set_mode((640,480))			# Get screen.
	engine = GraphicsEngine(screen)						# Start graphics engine.
	engine.setBackground(background)					# Set background.
	
	playerImage = pygame.Surface((26,26))				# Make the player's square.
	playerImage.fill((0,255,0))							#   It can be green.
	playerAnimations = {"Idle":Animation(AnimationFrame(playerImage,1,None,1),None,"Idle")}	# This line doesn't really make sense if squares are our end goal but makes things easy if we decide to move to sprites.
	player = GraphicObject(playerAnimations)			# Make the player's graphic object.
	player.setPos([320,200])							# Put the player at (320,200)
	engine.setPlayer(player)							# Set the player.
	
	clock = pygame.time.Clock()							# Set up the clock.
	move = [0,0]										# Movement vector
	
	while True:
		tick = clock.tick()/1000.0						# Calculate tick.
		
		for event in pygame.event.get():				# Event loop.
			if event.type == QUIT:						#   If quit...
				pygame.quit()
				exit()
			elif event.type == KEYDOWN:					#   If WASD is pressed, set movement vector appropriately.
				if event.key == K_w:
					move[1] = -100
				elif event.key == K_s:
					move[1] = 100
				elif event.key == K_a:
					move[0] = -100
				elif event.key == K_d:
					move[0] = 100
			elif event.type == KEYUP:					#   If WASD is released, reset movement vector.
				if event.key == K_w or event.key == K_s:
					move[1] = 0
				elif event.key == K_a or event.key == K_d:
					move[0] = 0

		player.setPos([player.getX()+(move[0]*tick),player.getY()+(move[1]*tick)])		# Update player's position. Because there is no such thing as a part of a pixel,
																						#   The position of graphic objects should usually be integers.
																						#   We will ignore that for this example to make things simpler.
		engine.update(tick)								# Update screen.
