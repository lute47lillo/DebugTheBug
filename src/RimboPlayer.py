import arcade
import math

from src.BugEnemy import BugEnemy

SCREEN_WIDTH = 1324
SCREEN_HEIGHT = 796
CHARACTER_SCALING = 0.5
BLASTER_SCALING = 0.30
PLAYER_MOVEMENT_SPEED = 5
SPEED_ANGLE = 5
BLASTER_SPEED = 8
SHOOT_SOUND = 0.2


class RimboPlayer:

    def __init__(self):

        # Create player and blaster lists and sprites
        self.player_sprite = None
        self.player_list = None

        # Instance of bug enemy
        enemy = BugEnemy()
        self.enemy = enemy

        self.blaster_list = arcade.SpriteList()
        self.isShooting = False

        # Set sound for shooting the blaster
        self.shoot_sound = arcade.load_sound(":resources:sounds/laser2.wav")

        # Attributes of player
        self.speed = 0
        self.angle = 0
        self.change_angle = 0
        self.playerSprite()

    # Create Sprite of the player.
    def playerSprite(self):

        self.player_list = arcade.SpriteList()

        image_source = "/Users/lutelillo/Desktop/DebugTheBug/lib/python3.8/" \
                       "site-packages/arcade/resources/images/createdSprites/booster_player.png"

        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)

        self.player_sprite.center_x = 670
        self.player_sprite.center_y = 380

        self.player_list.append(self.player_sprite)

    # Need to separate in two methods, init the sprite and then update the sprite of shooting
    def blasterSprite(self, blaster_center_x, blaster_center_y):

        # Create image of the blast
        imageBlaster = ":resources:images/space_shooter/laserBlue01.png"
        self.blaster_sprite = arcade.Sprite(imageBlaster, BLASTER_SCALING)

        # Get current position of the player
        self.blaster_sprite.center_x = blaster_center_x
        self.blaster_sprite.center_y = blaster_center_y
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

        self.shipUpdate()

    # Update it and add the condition when both are pressed and handle it.
    def onKeyReleased(self, key):

        if key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.speed = 0

        elif key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_angle = 0

        if key == arcade.key.J:
            self.blasterSprite(self.player_sprite.center_x, self.player_sprite.center_y)
            self.blaster_sprite.angle = self.player_sprite.angle
            self.shotUpdate()
            arcade.play_sound(self.shoot_sound, SHOOT_SOUND)

        self.shipUpdate()

    # Rotate the ship
    def shipUpdate(self):

        self.player_sprite.angle += self.player_sprite.change_angle

        self.player_sprite.change_x = -math.sin(math.radians(self.player_sprite.angle)) * self.player_sprite.speed
        self.player_sprite.change_y = math.cos(math.radians(self.player_sprite.angle)) * self.player_sprite.speed

        # Add border limitations to the movement of the player
        if self.player_sprite.center_x < 10:
            self.player_sprite.center_x = 10
        elif self.player_sprite.center_x > SCREEN_WIDTH - 10:
            self.player_sprite.center_x = SCREEN_WIDTH - 10
        else:
            self.player_sprite.center_x += self.player_sprite.change_x

        if self.player_sprite.center_y < 10:
            self.player_sprite.center_y = 10
        elif self.player_sprite.center_y > SCREEN_HEIGHT - 10:
            self.player_sprite.center_y = SCREEN_HEIGHT - 10
        else:
            self.player_sprite.center_y += self.player_sprite.change_y

    # Rotate and create the shooting of the blaster
    def shotUpdate(self):

        self.blaster_sprite.angle = self.blaster_sprite.angle

        self.blaster_sprite.change_x = -math.sin(math.radians(self.blaster_sprite.angle)) * BLASTER_SPEED
        self.blaster_sprite.change_y = math.cos(math.radians(self.blaster_sprite.angle)) * BLASTER_SPEED

        self.blaster_sprite.center_x += self.blaster_sprite.change_x
        self.blaster_sprite.center_y += self.blaster_sprite.change_y

        # Append the last blast to the blaster list. TODO: Create a pool object list for memory management.
        self.blaster_list.append(self.blaster_sprite)


