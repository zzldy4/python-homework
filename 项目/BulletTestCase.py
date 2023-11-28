#bullet类的update单元测试
import pygame
import unittest
from bullet import Bullet
from settings import Settings
from alien_invasion import AlienInvasion
class BulletTestCase(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.settings = Settings()  # 假设已创建一个Settings类来存储游戏设置
        self.ai_game = AlienInvasion(self.screen, self.settings)  # 假设已创建一个AlienInvasion类作为游戏主程序
        self.bullet = Bullet(self.ai_game)

    def test_update_bullet_position(self):
        """测试更新子弹位置"""
        initial_y = self.bullet.rect.y
        self.bullet.update()
        updated_y = self.bullet.rect.y
        self.assertEqual(updated_y, initial_y - self.settings.bullet_speed)

    def test_draw_bullet(self):
        """测试绘制子弹"""
        self.bullet.draw_bullet()
        # 进行绘制后的断言，根据具体情况进行判断

if __name__ == '__main__':
    unittest.main()