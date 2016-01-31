import pygame.rect

kScrollDirectionForwards = True    #up or to the right 
kScrollDirectionBackwards = False  #down or to the left

class Background(object):
    def __init__(self):
        self.scrollSpeed = (1.0, 1.0)
        self.scrollDirection = (kScrollDirectionForwards,kScrollDirectionBackwards)
        self.surface = None
        
    def getSprite(self,rect):
        if self.scrollDirection[0] == kScrollDirectionBackwards:
            rect.x = (self.surface.w - rect.w) - rect.x
        if self.scrollDirection[1] == kScrollDirectionForwards:
            rect.y = (self.surface.h - rect.h) - rect.y
            
        return rect