from FlyingSquares.Graphics.GraphicObject import createRectGraphicObject
import pygame

## Base class for projectiles.
class Projectile(object):
	
	## Constructor
	#
	#  @param graphicObject This projectile's GraphicObject.
	#  @param pos This projectile's position.
	#  @param vel This projectile's velocity.
	#  @param dmg The base damage this projectile does when it hits a Game Object.
	#  @param ally Set to @c True if was shot by an ally.
	def __init__(self,graphicObject,hitBox,pos,vel,dmg,ally):
		self.graphicObject = graphicObject
		self.hitBox = hitBox
		self.x = pos[0]
		self.y = pos[1]
		self.velx = vel[0]
		self.vely = vel[1]
		self.dmg = dmg
		self.ally = ally
		self.life = 500
	
	## Returns this projectile's graphic object.
	def getGraphicObject(self):
		return self.graphicObject
	
	## Returns this projectile's
	
	## Returns the position of this projectile.
	def getPos(self):
		return [self.x,self.y]
	
	## Returns the velocity of this projectile.
	def getVel(self):
		return [self.velx,self.vely]
	
	## Returns how much damage this projectile does.
	def getDmg(self):
		return self.dmg
	
	## Returns whether or not this projectile was shot by an ally.
	def getAlly(self):
		return self.ally
	
	def getHitBox(self):
		return self.hitBox.move(self.getGraphicObject().getX(),self.getGraphicObject().getY())
	
	## Updates this projectile.
	def update(self,tick):
		self.x += self.velx*tick
		self.y += self.vely*tick
		self.life -= max(abs(self.velx),abs(self.vely))*tick
		self.graphicObject.setPos([int(self.x),int(self.y)])
		if self.life <=0:
			return True

## A laser beam!
class Laser(Projectile):
	## Constructor.
	def __init__(self,pos,vel,dmg,ally):
		Projectile.__init__(self,createRectGraphicObject((3,10),(0,0,127),True,(0,0,255)),pygame.rect.Rect([0,0,3,10]),pos,vel,dmg,ally)

## A missile for Chris!
class Missile(Projectile):
	## Constructor.
	def __init__(self,pos,vel,dmg,ally):
		Projectile.__init__(self,createRectGraphicObject((3,10),(127,64,0),True,(255,127,0)),pygame.rect.Rect([0,0,3,10]),pos,vel,dmg,ally)
	
	## Updates this projectile.
	def update(self,tick):
		self.velx *= 1+10*tick
		self.vely *= 1+10*tick
		if self.velx >= 10:
			self.velx = 10
		if self.vely >= 10:
			self.vely = 10
		self.x += self.velx*tick
		self.y += self.vely*tick
		self.life -= max(abs(self.velx),abs(self.vely))*tick
		self.graphicObject.setPos([int(self.x),int(self.y)])
		if self.life <=0:
			return True
