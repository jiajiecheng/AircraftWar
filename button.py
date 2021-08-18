import pygame.font
class Button:
    """游戏按钮类"""
    def __init__(self,ai_game,msg):
        """初始化按按钮"""
        self.screen=ai_game.screen
        self.screen_rect =self.screen.get_rect()
        """尺寸以及其他的属性"""
        self.width,self.height=200,50
        self.button_color=(0,255,0)
        self.text_color=(0,0,0)
        self.font=pygame.font.SysFont(None,48)

        """创建一个rect对象,并使其居中"""
        self.rect=pygame.Rect(0,0,self.width,self.height)
        self.rect.center=self.screen_rect.center

        """按钮标签只需要创建一次"""
        self._perp_msg(msg)

    def _perp_msg(self,msg):
        """将MSG渲染成为图形,并且在按钮上居中"""
        self.msg_imge=self.font.render(msg,True,self.text_color,self.button_color)
        self.msg_imge_rect=self.msg_imge.get_rect()
        self.msg_imge_rect.center=self.rect.center

    def draw_button(self):
        """绘制一个按钮,而且绘制文本"""
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_imge,self.msg_imge_rect)
