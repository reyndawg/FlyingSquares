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
    
    ## Gives the player points.
    def addPoints(self,amt):
        self.points+=amt
    
    ## Returns how many points the player has earned.
    def getPoints(self):
        return self.points
    
    ## Updates all game objects.
    def update(self,tick):
        self.player.update(tick)
        
        for ally in self.allies:
            ally.update(tick)
        
        for enemy in self.enemies:
            enemy.update(tick)
        
        self.graphicsEngine.update(tick)
