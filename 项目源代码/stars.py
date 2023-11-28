from random import randint
import pygame
from pygame.sprite import Sprite 

class Stars(Sprite):

    def __init__(self,ai_game):
        super().__init__()
        self.screen=ai_game.screen
        
        #加载星星图片
        self.image=pygame.image.load('images/start.png')
        self.rect=self.image.get_rect()
        
        #随机星星
        self.rect.x=randint(0,ai_game.settings.screen_width)
        self.rect.y=randint(0,ai_game.settings.screen_height)
        self.x = float(self.rect.x)
        
