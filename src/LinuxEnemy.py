import arcade
import random
import math

from src.RimboPlayer import RimboPlayer

# Basic attributes
SCREEN_WIDTH = 1324
SCREEN_HEIGHT = 796
CHARACTER_SCALING = 1.5
MOVE_SPEED = 0.5
BLASTER_SCALING = 0.3


class LinuxEnemy:

    def __init__(self):

        self.linux_sprite = None
        self.linux_list = arcade.SpriteList()
        self.linux_bullet = None
        self.linux_bullet_list = arcade.SpriteList()
        self.linux_health = 20

        # Creation variables
        self.direction = 1
        self.angle = 0
        self.exist = 0
        self.linux_isShooting = False

        # Instance of player
        player = RimboPlayer()
        self.player = player

    def linuxSprite(self, position):

        self.exist = 1

        image_source = "/Users/lutelillo/Desktop/DebugTheBug/lib/python3.8/" \
                       "site-packages/arcade/resources/images/createdSprites/final_enemy.png"

        self.linux_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)

        if position == 1:
            self.linux_sprite.center_x = 40
            self.linux_sprite.center_y = SCREEN_HEIGHT/2 - 250

        else:
            self.linux_sprite.center_x = 1284
            self.linux_sprite.center_y = SCREEN_HEIGHT / 2 + 150

        self.linux_list.append(self.linux_sprite)
        return self.linux_sprite

    def move_enemy(self, enemy):

        # Move the sprite up and down
        if self.direction == 1:
            enemy.change_y = math.cos(math.radians(self.angle)) * MOVE_SPEED
            enemy.center_y += enemy.change_y

            if enemy.center_y > 740:
                self.direction = 0

        elif self.direction == 0:
            enemy.change_y = math.cos(math.radians(self.angle)) * -MOVE_SPEED
            enemy.center_y += enemy.change_y

            if enemy.center_y < 25:
                self.direction = 1

    def shoot_player(self, n, linux):

        image_source = "/Users/lutelillo/Desktop/DebugTheBug/lib/python3.8/" \
                       "site-packages/arcade/resources/images/createdSprites/enemy_blast2.png"

        self.linux_bullet = arcade.Sprite(image_source, BLASTER_SCALING)
        self.linux_bullet.center_x = linux.center_x
        self.linux_bullet.center_y = linux.center_y

        self.linux_isShooting = True

        if n == 1:
            self.linux_bullet.angle = -90
            self.linux_bullet.change_x = +2

        elif n == 0:
            self.linux_bullet.angle = 90
            self.linux_bullet.change_x = -2

        self.linux_bullet_list.append(self.linux_bullet)
