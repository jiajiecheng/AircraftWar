import pygame
from pygame.sprite import Sprite
"""用于管理飞机"""


class Ship(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        """获取AlienInvasion类中的信息,也就是屏幕的大小"""
        self.screen = ai_game.screen
        self.setting = ai_game.setting
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()
        """新的飞船放入屏幕底下"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        # 移动的标志
        self.moveing_right = False
        self.moveing_left = False

    def updata(self):
        """根据移动标志移动飞船的位置"""
        if self.moveing_right and self.rect.right < self.screen_rect.right:
            self.x += self.setting.ship_speed
        if self.moveing_left and self.rect.left > 0:
            self.x -= self.setting.ship_speed
        """根据self.x更新rect对象"""
        self.rect.x = self.x

    def blitme(self):
        """指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.midbottom=self.screen_rect.midbottom
        self.x=float(self.rect.x)
