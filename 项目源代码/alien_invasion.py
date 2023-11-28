import sys
import pygame
from time import sleep
from random import randint

from settings import Settings
from Ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from stars import Stars
class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()#控制帧率
        
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        
        pygame.display.set_caption("Alien Invasion")
        

        self.stars=pygame.sprite.Group()
        

        pygame.time.set_timer(pygame.USEREVENT + 1, 2000)  # 每2秒触发一次定时器

        self.elapsed_time=0

        self.stats=GameStats(self)
        self.sb=Scoreboard(self)
        
        self.ship = Ship(self)
        self.bullets=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()
        
        self._create_fleet()

        self.game_active=False

        self.play_button=Button(self, "start")
        
    def _ship_hit(self):
        """响应飞船和外星人的碰撞"""
        if self.stats.ships_left>0:
            #将ships_left减1并更新记分牌
            self.ship.hit = True
            self.stats.ships_left-=1
            self.sb.prep_ships()
            
            #清空外星人列表和子弹列表
            self.bullets.empty()
            self.aliens.empty()
            

            self._create_fleet()
            self.ship.center_ship()
            
            #暂停
            sleep(0.5)
        else:
            self.game_active=False
            pygame.mouse.set_visible(True)
    
    def _create_fleet(self):
        alien=Alien(self)
        alien_width,alien_height=alien.rect.size
        
        current_x,current_y=alien_width,alien_height
        while current_y<(self.settings.screen_height-3*alien_height):
            while current_x<(self.settings.screen_width-2*alien_width):
                self._create_alien(current_x,current_y)
                current_x += 2*alien_width
            
            #添加一行外星人后，重置x值并递增y值
            current_x=alien_width
            current_y += 2*alien_height
            
    def _create_alien(self,x_position,y_position):
        """创建一个外星人并将其加入外星舰队"""
        new_alien =Alien(self)
        new_alien.x=x_position
        new_alien.rect.x=x_position
        new_alien.rect.y=y_position
        self.aliens.add(new_alien)
        
    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(60)#时钟计时，尽可能确保这个循环每秒运行60次
    
    def _update_aliens(self):
        """检查是否有外星人位于屏幕边缘,并更新外星舰队中所有外星人的位置"""
        self._check_fleet_edges()
        self.aliens.update()
        
        #检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        #检查是否有外星人到达了屏幕的下边缘
        self._check_aliens_bottom()
        
    
    def _check_fleet_edges(self):
        """在有外星人到达边缘时采取的相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """将整个外星舰队向下移动,并改变它们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction*=-1
    
    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.sb.write_high_score()
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type==pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type==pygame.MOUSEBUTTONDOWN:#监视Play按钮
                mouse_pos=pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.USEREVENT + 1:#计时更新星星位置
                self.stars_update()

        
    def _check_play_button(self,mouse_pos):
        """在玩家单击Play按钮时开始新游戏"""
        
        button_clicked=self.play_button.rect.collidepoint(mouse_pos)
        #当玩家单击了Play按钮且游戏当前处于非活动状态时
        if button_clicked and not self.game_active:
            #还原游戏设置
            self.settings.initialize_dynamic_settings()
            #重置游戏的统计信息
            self.stats.reset_stats()
            self.game_active=True
            self.sb.prep_score()#重置得分
            self.sb.prep_level()#重置等级
            self.sb.prep_ships()
            #清空外星人列表和子弹列表
            self.bullets.empty()
            self.aliens.empty()
            
            #创建一个新的外星舰队，并将飞船放在屏幕底部的中央
            self._create_fleet()
            self.ship.center_ship()
            
            #隐藏光标
            pygame.mouse.set_visible(False)
            
        
    def _check_keydown_events(self,event):
        """响应按下"""
        if event.key==pygame.K_RIGHT:#玩家按下向右键时moving_right为True
            #向右移动飞船
            self.ship.moving_right=True
        elif event.key==pygame.K_LEFT:
            #向左移动
            self.ship.moving_left=True
        elif event.key==pygame.K_q:#按Q键退出
            self.sb.write_high_score()
            sys.exit()
        elif event.key==pygame.K_SPACE:#按空格键发射一颗子弹
            self._fire_bullet()
        elif event.key==pygame.K_UP:
            self.ship.moving_up=True
        elif event.key==pygame.K_DOWN:
            self.ship.moving_down=True
        
    
    def _check_keyup_events(self,event):
        """响应释放"""
        if event.key==pygame.K_RIGHT:#玩家释放向右键时moving_right为False
            self.ship.moving_right=False
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=False
        elif event.key==pygame.K_UP:
            self.ship.moving_up=False
        elif event.key==pygame.K_DOWN:
            self.ship.moving_down=False
            
    
    def _fire_bullet(self):
        """创建一颗子弹,并将其加入编组bullets,但屏幕上最多有self.settings.bullets_allowed颗子弹"""
        if len(self.bullets)<self.settings.bullets_allowed:
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)
        
    def _update_bullets(self):
        """更新子弹的位置并删除已经消失的子弹"""
        #更新子弹的位置
        self.bullets.update()
        
        #删除已经消失的子弹
        #到达屏幕上边缘后消失,删除已消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom<=0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def stars_update(self):
        """在游戏背景中随机放星星"""
        #更新星星的位置
        self.stars.empty()
        for _ in range(10):
                star = Stars(self)
                self.stars.add(star)
            
    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人的碰撞"""
        #删除发生碰撞的子弹和外星人
        #检查是否有子弹击中了外星人
        #如果是，就删除相应的子弹和外星人
        collisions=pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points*len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        
        if not self.aliens:
            #删除现有的子弹并创建一个新的外星舰队
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            
            #提高等级，整个外星舰队都被击落，就提高一个等级
            self.stats.level += 1
            self.sb.prep_level()
    
    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕的下边缘"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >=self.settings.screen_height:
                #像飞船被撞到一样进行处理
                self._ship_hit()
                break
    
    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)#每次循环时都重绘屏幕
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        
        #显示得分
        self.sb.show_score()

        if not self.game_active:
            self.play_button.draw_button()

        self.stars.draw(self.screen)

        pygame.display.flip()
        
        
if __name__=="__main__":
    #创建游戏实例并运行游戏
    ai=AlienInvasion()
    ai.run_game()
    
    
    
    
    