class GameStats:
    """此类用于游戏的统计"""
    def __init__(self, ai_game):
        self.setting = ai_game.setting
        self.reset_stats()
        #游戏开始的标志
        self.game_active=False
        #记录分数
        self.score=0
        #展示最高分
        self.heigh_score=0
        #显示等级
        self.level=1
    def reset_stats(self):
        """"初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.setting.ship_limit
        self.score=0
