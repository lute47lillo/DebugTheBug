import arcade
import random
import math


SCREEN_WIDTH = 1324
SCREEN_HEIGHT = 796
CHARACTER_SCALING = 0.5
SEMICOLON_MAX = 15
SPRITE_SPEED = 0.5


class BugEnemy:

    def __init__(self):
        self.bug_sprite = None
        self.bug_list = arcade.SpriteList()
        self.count = 0

        self.bugSprite()

    # Create the bug sprite and defines its original position
    def bugSprite(self):
        image_source = ":resources:images/enemies/fly.png"

        self.bug_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)

        rand_center_x = random.randrange(SCREEN_WIDTH)
        rand_center_y = random.randrange(SCREEN_HEIGHT)
        self.bug_sprite.center_x = rand_center_x
        self.bug_sprite.center_y = rand_center_y

        self.bug_list.append(self.bug_sprite)
        self.count += 1

    # Following of player movement
    def followSprite(self, player, enemy):

        enemy.center_x += enemy.change_x
        enemy.center_y += enemy.change_y

        start_x = enemy.center_x
        start_y = enemy.center_y

        dest_x = player.center_x
        dest_y = player.center_y

        x_diff = (dest_x - start_x)
        y_diff = (dest_y - start_y)

        angle = math.atan2(y_diff, x_diff)

        enemy.change_x = math.cos(angle) * SPRITE_SPEED
        enemy.change_y = math.sin(angle) * SPRITE_SPEED
