import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        #加载外星人图像并设置其rect属性
        self.image=pygame.image.load('images/1.png')
        self.rect=self.image.get_rect()
    
        #每个外星人最初都在屏幕的左上角附近
        self.rect.x=self.rect.width
        self.rect.y=self.rect.height
        
        #存储外星人的精确水平位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        self.x += self.settings.alien_speed*self.settings.fleet_direction
        self.rect.x = self.x
    
    def check_edges(self):
        screen_rect=self.screen.get_rect()
        return (self.rect.right >= screen_rect.right)or(self.rect.left <= 0)
    