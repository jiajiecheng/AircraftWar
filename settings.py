class Settings:
    """游戏的设置类"""

    def __init__(self):
        """初始化游戏设置"""
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        # 飞船的移动速度
        self.ship_speed = 1.5
        # 子弹的设置
        self.bullet_speed = 1.5
        self.ship_limit = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        # 子弹的最大的数量
        self.bullets_allowed = 5

        # 外星人设置
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        """这个参数等于1表示右边移动,等于-1表示左边"""
        self.fleet_direction = 1

        # 加快游戏的节奏
        self.speedup_scale = 1.1
        #外星人分数提高速度
        self.sccore_scale=1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        self.fleet_direction = 1
        """击杀得分"""
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points=int(self.alien_points*self.sccore_scale)