import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
CHARACTER_SCALING = 3
PLAYER_MOVEMENT_SPEED = 5


class RimboPlayer:

    def __init__(self):
        """self.health = health
        self.xPos = xPos
        self.yPos = yPos"""

        self.player_sprite = None
        self.player_list = None
        self.startSprite()

    #Create Sprite of the player.
    def startSprite(self):
        self.player_list = arcade.SpriteList()
        image_source = ":resources:images/createdSprites/Rimbona.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.player_list.append(self.player_sprite)

    def onKeyPressed(self, key):
        #Create an action for different movements

        if key == arcade.key.W:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED

        #Update it and add the condition when both are pressed and handle it.

    def onKeyReleased(self, key):

        if key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.D:
            self.player_sprite.change_x = 0




