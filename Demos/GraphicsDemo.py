# Graphics Demo:
import pygame
from pygame.locals import *

from FlyingSquares.Graphics import *

pygame.init()
background = pygame.Surface([640,480])				# Make some background image, would normally get from file?
background.fill((127,127,255))						#   It will be light blue for now
screen = pygame.display.set_mode((640,480))			# Get screen.
engine = GraphicsEngine.GraphicsEngine(screen)		# Start graphics engine.
engine.setBackground(background)					# Set background.

#Original code before conveniece function.	
#playerImage = pygame.Surface((26,26))				# Make the player's square.
#playerImage.fill((0,255,0))						#   It can be green.
#playerAnimations = {"Idle":Animation(AnimationFrame(playerImage,1,None,1),None,"Idle")}	# This line doesn't really make sense if squares are our end goal but makes things easy if we decide to move to sprites.
#player = GraphicObject(playerAnimations)			# Make the player's graphic object.

player = GraphicObject.createSquareGraphicObject(26,(0,255,0),True,(0,127,0))	# Create a green square that is 26x26 with a dark green outline.
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
