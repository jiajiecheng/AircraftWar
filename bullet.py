import pygame
from pygame.sprite import Sprite
class Bullet (Sprite):
    """管理飞机发射子弹的类"""
    def __init__(self,ai_game):
        """在飞船的位置创建子弹"""
        super().__init__()
        self.screen=ai_game.screen
        self.setting=ai_game.setting
        self.color=self.setting.bullet_color

        #在0,0处创建一个表示子弹的矩形,在设置正确的位置
        self.rect =pygame.Rect(0,0,self.setting.bullet_width,self.setting.bullet_height)
        self.rect.midtop=ai_game.ship.rect.midtop

        #使用小数来表示子弹的位置
        self.y=float(self.rect.y)

    def update(self):
        """向上移动子弹"""
        self.y-=self.setting.bullet_speed
        """更新子弹的位置"""
        self.rect.y=self.y

    """在屏幕上绘制子弹"""
    def draw_bullet(self):
        pygame.draw.rect(self.screen,self.color,self.rect)

