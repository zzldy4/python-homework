import json
class GameStats:
    
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        
        #在任何情况下都不应重置最高分
        self.read_high_score()
        self.level=1#等级
        
    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score=0#计分
    
    def read_high_score(self):
        filename='hightest_score.json'
        try:
            with open(filename,'r') as file:
                self.high_score=json.load(file)
        except FileNotFoundError:
            #如果文件不存在，说明是第一次运行游戏，最高分设为0
            self.high_score=0
    
    