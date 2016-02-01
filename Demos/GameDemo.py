# Game Engine Demo:
import pygame
from pygame.locals import *

from FlyingSquares.Graphics import *
from FlyingSquares.Game import *

pygame.init()
background = pygame.Surface([640,480])              # Make some background image, would normally get from file?
background.fill((127,127,255))                      #   It will be light blue for now
screen = pygame.display.set_mode((640,480))         # Get screen.
graphicsEngine = GraphicsEngine.GraphicsEngine(screen)      # Start graphics engine.
graphicsEngine.setBackground(background)                    # Set background.

gameEngine = GameEngine.GameEngine(graphicsEngine)  # Set up game engine.

playerG = GraphicObject.createSquareGraphicObject(26,(0,255,0),True,(0,127,0))  # Create a green square that is 26x26 with a dark green outline for the players GraphicObject.

player = GameObject.GameObject(playerG,10,(320,200),100,None,ally=True)     # Create a GameObject for the player with 10 hp at position (320,200)
                                                                            # that moves at 100 pixels per second with no hit box. This player is on the ally team.                                                                         
gameEngine.setPlayer(player)                        # Set the player.

enemyG = GraphicObject.createSquareGraphicObject(13,(255,0,0),True,(127,0,0))  # Create a red square for an enemy.
enemy = GameObject.GameObject(enemyG,10,(320,50),100,pygame.rect.Rect([0,0,13,13]))  #Create an enemy GameObject.
enemy.setVel((50,0))                                # Make the enemy move right
gameEngine.addEnemy(enemy)

clock = pygame.time.Clock()                         # Set up the clock.
move = [0,0]                                        # Movement vector
timeout = 5                                         # Time until next enemy is spawned.
vel = -50                                           # Velocity the next enemy will have in the x direction.

while True:
    tick = clock.tick()/1000.0                      # Calculate tick.
    
    for event in pygame.event.get():                # Event loop.
        if event.type == QUIT:                      #   If quit...
            pygame.quit()
            exit()
        elif event.type == KEYDOWN:                 #   If WASD is pressed, set movement vector appropriately.
            if event.key == K_w:
                move[1] = -100
            elif event.key == K_s:
                move[1] = 100
            elif event.key == K_a:
                move[0] = -100
            elif event.key == K_d:
                move[0] = 100
            elif event.key == K_RETURN:             #   If Enter is pressed, fire laser!
                proj = Projectile.Laser([player.getX()+13,player.getY()],(0,-400),1,True)    # Create laser projectile
                gameEngine.addProjectile(proj)      #     Add projectile
            elif event.key == K_m:                  #   If Enter is pressed, fire Missile!
                proj = Projectile.Missile([player.getX()+13,player.getY()],(0,-4.0),1,True)    # Create missile projectile
                gameEngine.addProjectile(proj)      #     Add projectile
        elif event.type == KEYUP:                   #   If WASD is released, reset movement vector.
            if event.key == K_w or event.key == K_s:
                move[1] = 0
            elif event.key == K_a or event.key == K_d:
                move[0] = 0

    player.setVel(move)                             # Update player's position
    
    for enemy in gameEngine.getEnemies():
        if enemy.getPos()[0]<40:                    # Make the enemy move back and forth
            enemy.setVel((50,0))
        elif enemy.getPos()[0]>600:
            enemy.setVel((-50,0))
    
    if timeout <= 0:                                # If 5 seconds have passed make a new enemy
        enemyG = GraphicObject.createSquareGraphicObject(13,(255,0,0),True,(127,0,0))  # Create a red square for an enemy.
        enemy = GameObject.GameObject(enemyG,10,(320,50),100,pygame.rect.Rect([0,0,13,13]))  #Create an enemy GameObject.
        enemy.setVel((vel,0))                       # Make the enemy move right
        gameEngine.addEnemy(enemy)
        vel *= -1
        timeout = 5
    else:
        timeout -= tick
    
    screen.fill((255,0,0),(40,10,560,10))
    gameEngine.update(tick)                         # Update GameEngine which updates GraphicEngine.
