import pygame
import unittest
from Ship import Ship
from settings import Settings
from alien_invasion import AlienInvasion
class ShipTestCase(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.settings = Settings()  # 假设已创建一个Settings类来存储游戏设置
        self.ai_game = AlienInvasion(self.screen, self.settings)  # 假设已创建一个AlienInvasion类作为游戏主程序
        self.ship = Ship(self.ai_game)

    def test_blitme(self):
        """测试绘制飞船"""
        self.ship.blitme()
        # 进行绘制后的断言，根据具体情况进行判断

if __name__ == '__main__':
    unittest.main()