import arcade
import math

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
CHARACTER_SCALING = 0.5
BLASTER_SCALING = 0.25
PLAYER_MOVEMENT_SPEED = 5
SPEED_ANGLE = 5
BLASTER_SPEED = 8


class RimboPlayer:

    def __init__(self):

        self.player_sprite = None
        self.player_list = None

        self.blaster_sprite = None
        self.blaster_list = None
        self.isShooting = False

        # Attributes of player
        self.speed = 0
        self.angle = 0
        self.change_angle = 0
        self.playerSprite()


    # Create Sprite of the player.
    def playerSprite(self):
        self.player_list = arcade.SpriteList()
        image_source = ":resources:images/space_shooter/playerShip1_green.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 300
        self.player_sprite.center_y = 500
        self.player_list.append(self.player_sprite)

    # Need to separate in two methods, init the sprite and then update the sprite of shoooting
    def blasterSprite(self, blaster_center_x, blaster_center_y):
        self.blaster_list = arcade.SpriteList()
        imageBlaster = ":resources:images/space_shooter/laserBlue01.png"
        self.blaster_sprite = arcade.Sprite(imageBlaster, BLASTER_SCALING)

        self.blaster_sprite.center_x = blaster_center_x
        self.blaster_sprite.center_y = blaster_center_y
        self.blaster_list.append(self.blaster_sprite)
        self.isShooting = True

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

        # Shooting action
        if key == arcade.key.J:
            pass

        self.update()

    # Update it and add the condition when both are pressed and handle it.
    def onKeyReleased(self, key):

        if key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.speed = 0

        elif key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_angle = 0

        if key == arcade.key.J:
            self.blasterSprite(self.player_sprite.center_x, self.player_sprite.center_y)
            self.blaster_sprite.angle = self.player_sprite.angle
            #self.isShooting = True
            self.shotUpdate()

        self.update()

    def update(self):
        # Rotate the ship

        self.player_sprite.angle += self.player_sprite.change_angle

        self.player_sprite.change_x = -math.sin(math.radians(self.player_sprite.angle)) * self.player_sprite.speed
        self.player_sprite.change_y = math.cos(math.radians(self.player_sprite.angle)) * self.player_sprite.speed

        self.player_sprite.center_x += self.player_sprite.change_x
        self.player_sprite.center_y += self.player_sprite.change_y

    # Rotate and create the shooting of the blaster
    def shotUpdate(self):

        self.blaster_sprite.angle = self.blaster_sprite.angle

        self.blaster_sprite.change_x = -math.sin(math.radians(self.blaster_sprite.angle)) * BLASTER_SPEED
        self.blaster_sprite.change_y = math.cos(math.radians(self.blaster_sprite.angle)) * BLASTER_SPEED

        self.blaster_sprite.center_x += self.blaster_sprite.change_x
        self.blaster_sprite.center_y += self.blaster_sprite.change_y










