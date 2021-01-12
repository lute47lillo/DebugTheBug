"""
Starting Template
"""
import arcade
import math

from src.RimboPlayer import RimboPlayer

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 896
SCREEN_TITLE = "Rimbo Rogue"
CHARACTER_SCALING = 0.5
TILE_SCALING = 0.5
GRAVITY = 1


class MyGame(arcade.Window):
    """
    Main application class.
    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # Create the player
        player1 = RimboPlayer()
        self.player1 = player1

        # Create the background
        self.background_game = None

        # Create a list of enemies that interact or not with the player.
        self.listEnemies = arcade.SpriteList(None)

        # Created the basic engine for the movements.
        self.physicsP1 = None

    def setup(self):
        # Create your sprites and sprite lists here

        # Create a map
        self.background_game = arcade.load_texture(":resources:images/backgrounds/stars.png")

        # Created the basic engine for the movements.
        self.physicsP1 = arcade.PhysicsEngineSimple(self.player1.player_sprite, self.listEnemies)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background_game)

        # Call draw() on all your sprite lists below
        self.player1.player_list.draw()
        self.listEnemies.draw()

        if self.player1.isShooting:
            self.player1.blaster_list.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        # Update the basic engine when keys are pressed.
        self.physicsP1.update()
        if self.player1.isShooting:
            self.player1.blaster_sprite.update()

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.
        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """

        self.player1.onKeyPressed(key)

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        self.player1.onKeyReleased(key)

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
