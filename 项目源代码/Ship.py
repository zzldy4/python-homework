import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """管理飞船的类"""
    def __init__(self,ai_game):
        """初始化飞船并设置其初始位置"""
        super().__init__()
        self.screen=ai_game.screen
        self.settings=ai_game.settings
        
        self.screen_rect=ai_game.screen.get_rect()
        
        #加载飞船图像并获取其外接矩形
        self.image=pygame.image.load('images/ship.bmp')
        self.rect=self.image.get_rect()
        
        #每艘新飞船都放在屏幕底部的中央
        # self.rect.midbottom=self.screen_rect.midbottom
        #每艘飞船都放在屏幕底部的左侧
        self.rect.bottomleft=self.screen_rect.bottomleft
        
        #在飞船的属性x中存储一个浮点数
        self.x=float(self.rect.x)
        # 在飞船的属性y中存储一个浮点数
        self.y = float(self.rect.y)
        
        #移动标志（飞船一开始不移动）
        self.moving_right=False
        self.moving_left=False
        self.moving_up=False#向上移动标志
        self.moving_down=False#向下移动标志

        self.hit = False
        self.hitnum = 0
        self.bomb_lists = []  # 用来存储爆炸时需要的图片
        self.image_num = 0  # 用来记录while循环的次数,当次数达到一定值时才显示一张爆炸的图,然后清空,当这个次数再次达到时,再显示下一个爆炸效果的图片
        self.image_index = 0  # 用来记录当前要显示的爆炸效果的图片的序号
    def crate_images(self):  # 将爆炸需要的图片添加到self.bomb_lists中
        self.bomb_lists.append(pygame.image.load("./images/enemy0.png"))
        self.bomb_lists.append(pygame.image.load("./images/enemy0_down1.png"))
        self.bomb_lists.append(pygame.image.load("./images/enemy0_down2.png"))
        self.bomb_lists.append(pygame.image.load("./images/enemy0_down3.png"))
        print("爆炸了")
    
    def update(self):
        """根据移动标志调整飞船的位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left>0:
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.top>0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom<self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        
        #根据self.x更新rect对象
        self.rect.x=self.x
        self.rect.y=self.y
    def blitme(self):
        """在指定位置绘制飞船"""
        if self.hit == True:  # 如果满足爆炸条件，就显示爆炸的图片
            self.crate_images()
            self.screen.blit(self.bomb_lists[self.image_index], (self.x, self.y))
            self.image_num += 1  # 这是统计循环次数，为了使玩家看清爆炸效果
            if self.image_num == 7:  # 如果循环次数达到7次
                self.image_num = 0  # 将循环次数改为0次
                self.image_index += 1  # 图片显示序号+1，换为另一张图
            if self.image_index > 3:  # 这里爆炸图片一共是四张，所以是图片序号大于三次
                self.image_index = 0
                # exit()  #调用exit让游戏退出
                self.hit = False
                self.hitnum += 1
                print(self.hitnum)
        else:
            self.screen.blit(self.image,self.rect)
        
    def center_ship(self):
        """让飞船在屏幕底部的左侧"""
        #底部中央
        # self.rect.midbottom=self.screen_rect.midbottom
        self.rect.bottomleft=self.screen_rect.bottomleft
        self.x=float(self.rect.x)
        self.y=float(self.rect.y)
