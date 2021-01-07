import arcade
import math

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
CHARACTER_SCALING = 0.5
PLAYER_MOVEMENT_SPEED = 5
SPEED_ANGLE = 5


class RimboPlayer:

    def __init__(self):

        self.player_sprite = None
        self.player_list = None

        arcade.set_background_color(arcade.color.BLACK)

        self.speed = 0
        self.angle = 0
        self.change_angle = 0
        self.max_speed = 4
        self.thrust = 0
        self.startSprite()

    # Create Sprite of the player.
    def startSprite(self):
        self.player_list = arcade.SpriteList()
        image_source = ":resources:images/space_shooter/playerShip1_green.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 300
        self.player_sprite.center_y = 500
        self.player_list.append(self.player_sprite)

    def onKeyPressed(self, key):

        # Create an action for different movements
        if key == arcade.key.W:
            self.player_sprite.speed = PLAYER_MOVEMENT_SPEED

        elif key == arcade.key.S:
            self.player_sprite.speed = -PLAYER_MOVEMENT_SPEED

        elif key == arcade.key.D:
            self.player_sprite.change_angle = -SPEED_ANGLE

        elif key == arcade.key.A:
            self.player_sprite.change_angle = SPEED_ANGLE

        self.update()

        # Update it and add the condition when both are pressed and handle it.

    def onKeyReleased(self, key):

        if key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.speed = 0

        elif key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_angle = 0

        self.update()

    def update(self):
        # Rotate the ship
        self.player_sprite.angle += self.player_sprite.change_angle

        self.player_sprite.change_x = -math.sin(math.radians(self.player_sprite.angle)) * self.player_sprite.speed

        self.player_sprite.change_y = math.cos(math.radians(self.player_sprite.angle)) * self.player_sprite.speed

        self.player_sprite.center_x += self.player_sprite.change_x

        self.player_sprite.center_y += self.player_sprite.change_y






