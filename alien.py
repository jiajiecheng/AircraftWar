import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """表示外星人的类"""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        """设置属性"""
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()
        """出现在屏幕的左上角"""
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        """外星人精确的位置"""
        self.x = float(self.rect.x)
        self.setting = ai_game.setting

    def update(self):
        """向右边移动外星人"""
        self.x += (self.setting.alien_speed * self.setting.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """外星人处于边缘的时候返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
