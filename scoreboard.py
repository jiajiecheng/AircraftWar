import pygame.font
from pygame.sprite import Group
from ship import Ship

class ScoreBoard:
    """显示分数信息的类"""

    def __init__(self, ai_game):
        """初始化分数的信息"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.setting = ai_game.setting
        self.stats = ai_game.stats
        self.ai_game=ai_game

        """显示分数时候显示的字体"""
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        """准备得分的图像"""
        self.prep_score()
        self.prep_height_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        rounded_score=round(self.stats.score,-1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.setting.bg_color)

        """显示与屏幕的右上角"""
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """在屏幕上显示得分以及等级"""
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        self.ships.draw(self.screen)

    def prep_height_score(self):
        """将最高分渲染成图像"""
        high_score=round(self.stats.heigh_score,-1)
        high_score_str="{:,}".format(high_score)
        self.high_score_image=self.font.render(high_score_str,True,self.text_color,self.setting.bg_color)

        """展示的位置为屏幕顶端的中间"""
        self.high_score_rect=self.high_score_image.get_rect()
        self.high_score_rect.centerx=self.screen_rect.centerx
        self.high_score_rect.top=self.screen_rect.top

    def check_high_score(self):
        """是否产生了新的高分"""
        if self.stats.score >self.stats.heigh_score:
            self.stats.heigh_score =self.stats.score
            self.prep_height_score()

    def prep_level(self):
        level_str=str(self.stats.level)
        self.level_image=self.font.render(level_str,True,self.text_color,self.setting.bg_color)

        """将等级放在得分的下面"""
        self.level_rect=self.level_image.get_rect()
        self.level_rect.right=self.score_rect.right
        self.level_rect.top=self.score_rect.bottom+10

    def prep_ships(self):
        """显示还剩余多少参数"""
        self.ships=Group()
        for ship_number in range(self.stats.ships_left):
            ship=Ship(self.ai_game)
            ship.rect.x=10+ship_number*ship.rect.width
            ship.rect.y=10
            self.ships.add(ship)

