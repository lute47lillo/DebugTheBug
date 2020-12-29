import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
CHARACTER_SCALING = 3


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



