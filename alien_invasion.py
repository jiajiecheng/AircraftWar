import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard

"""窗口主类"""


class AlienInvasion:
    def __init__(self):
        """进行游戏资源初始化"""
        pygame.init()
        self.setting = Settings()
        """窗口大小"""
        # 将屏幕设置为全屏
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        #self.setting.screen_width = self.screen.get_rect().width
        #self.setting.screen_height = self.screen.get_rect().height
        #如果需要将屏幕大小设置为特定的值就只需要留下这一行代码即可
        self.screen = pygame.display.set_mode((self.setting.screen_width, self.setting.screen_height))
        """"设置窗口显示游戏名字"""
        pygame.display.set_caption("飞机大战")
        """初始化飞机的模型"""
        self.ship = Ship(self)
        """初始化子弹模型"""
        self.bullets = pygame.sprite.Group()
        """初始化外星人模型"""
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        """计游戏的实例"""
        self.stats = GameStats(self)
        """创建按钮的实例"""
        self.play_button = Button(self, "Play")

        """创建一个分数的实例"""
        self.sb = ScoreBoard(self)

    """
    游戏运行的主要方法,所有辅助方法在其中调用
    """

    def run_game(self):
        """开始游戏的主循环,检测游戏鼠标以及键盘的点击"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.updata()
                self._update_bullets()
                self._update_aliens()
            self._updata_screen()

    """响应键盘以及鼠标时间"""

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    """响应按下键盘"""

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moveing_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moveing_left = True
        # 按下Q键退出游戏
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _fire_bullet(self):
        """创建子弹,加入编组"""
        if len(self.bullets) < self.setting.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    """响应松开键盘"""

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moveing_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moveing_left = False

    """用于更新图像"""

    def _updata_screen(self):
        self.screen.fill(self.setting.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        """处于非游戏状态的时候绘制button"""
        if not self.stats.game_active:
            self.play_button.draw_button()
        """每一次的循环重新绘制屏幕"""
        pygame.display.flip()

    """更新子弹"""

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collections = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collections:
            for alinens in collections.values():
                self.stats.score += self.setting.alien_points * len(alinens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            # 删除当前的子弹,并且新建敌人
            self.bullets.empty()
            self._create_fleet()
            self.setting.increase_speed()

            #提升等级
            self.stats.level+=1
            self.sb.prep_level()

    def _create_fleet(self):
        """创建外星人群体"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.setting.screen_width - (2 * alien_width)
        numbers_aliens_x = available_space_x // (2 * alien_width)
        """计算可以容纳多少行外星人"""
        ship_height = self.ship.rect.height
        available_space_y = (self.setting.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        for row_number in range(number_rows):
            for alien_number in range(numbers_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """创建一组外星人并且放在当前行"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        """更新所有外星人的位置"""
        """检查是否有外星人在边缘,如果有调整位置"""
        self._check_fleet_edges()
        self.aliens.update()

        # 检测外星人与飞机之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # 检测外星人与底部的碰撞
        self._check_aliens_bottom()

    """外星人达到边缘"""

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """外星人整体往下面移动,并且改变方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.setting.fleet_drop_speed
        self.setting.fleet_direction *= -1

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            """飞船被转撞到了"""
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            """清空子弹和外星人"""
            self.aliens.empty()
            self.bullets.empty()
            """船舰一群新的外星人,并且将飞船放在屏幕底端的中央"""
            self._create_fleet()
            self.ship.center_ship()
            # 暂停
            sleep(0.5)
        else:
            self.stats.game_active = False
            """显示鼠标光标"""
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """检查是否触碰到的了底部"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom > screen_rect.bottom:
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos):
        """玩家点击按钮开始游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.setting.initialize_dynamic_settings()
            """重置统计的信息"""
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            """清空剩余的子弹以及外星人"""
            self.aliens.empty()
            self.bullets.empty()

            """创建一批新的外星人并且让外星人居中"""
            self._create_fleet()
            self.ship.center_ship()
            """隐藏鼠标的光标"""
            pygame.mouse.set_visible(False)


def main():
    ai = AlienInvasion()
    ai.run_game()


if __name__ == '__main__':
    main()
