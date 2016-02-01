## This class contains the code for game mechanics.
class GameEngine(object):
    
    ## Constructor.
    #
    #  @param graphicsEngine A reference to the graphic engine.
    def __init__(self,graphicsEngine):
        self.graphicsEngine = graphicsEngine
        self.points = 0
        
        self.player = None
        self.allies = []
        self.enemies = []
        self.projectiles = []
    
    ## Sets the player.
    def setPlayer(self,player):
        self.player = player
        self.graphicsEngine.setPlayer(player.getGraphicObject())
    
    ## Adds a game object to the allies team.
    def addAlly(self,ally):
        self.allies.append(ally)
        self.graphicsEngine.addObject(ally.getGraphicObject())
    
    ## Adds a game object to the enemies team.
    def addEnemy(self,enemy):
        self.enemies.append(enemy)
        self.graphicsEngine.addObject(enemy.getGraphicObject())
    
    ## Adds a projectile.
    def addProjectile(self,proj):
        self.projectiles.append(proj)
        self.graphicsEngine.addObject(proj.getGraphicObject())
    
    ## Gives the player points.
    def addPoints(self,amt):
        self.points+=amt
    
    ## Returns how many points the player has earned.
    def getPoints(self):
        return self.points
    
    ## Returns the list of enemies. Probably shouldn't be used but makes the GameDemo simpler.
    def getEnemies(self):
        return self.enemies
    
    ## Updates all game objects.
    def update(self,tick):
        self.player.update(tick)
        
        for ally in self.allies:
            ally.update(tick)
        
        for enemy in self.enemies:
            enemy.update(tick)
            if enemy.getHp()<=0:
                self.graphicsEngine.removeObject(enemy.getGraphicObject())
                self.enemies.remove(enemy)
        
        for proj in self.projectiles:
            if proj.update(tick):
                self.projectiles.remove(proj)
                self.graphicsEngine.removeObject(proj.getGraphicObject())
            if proj.getAlly():
                for enemy in self.enemies:
                    if enemy.getHitBox().colliderect(proj.getHitBox()):
                        enemy.takeDamage(proj.getDmg())
                        self.graphicsEngine.removeObject(proj.getGraphicObject())
                        self.projectiles.remove(proj)
                        break
        
        self.graphicsEngine.update(tick)
