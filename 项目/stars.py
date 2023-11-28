from random import randint
import pygame
from pygame.sprite import Sprite 

class Stars(Sprite):
    """表示背景中的星星的类"""
    
    def __init__(self,ai_game):
        """初始化星星并设置其初始位置"""
        super().__init__()
        self.screen=ai_game.screen
        
        #加载星星图片，并在屏幕上创建星星的矩形
        self.image=pygame.image.load('images/start.png')
        self.rect=self.image.get_rect()
        
        #在屏幕范围内随机放置星星
        self.rect.x=randint(0,ai_game.settings.screen_width)
        self.rect.y=randint(0,ai_game.settings.screen_height)
        
        self.x = float(self.rect.x)
        
