"""
Author: Lute Lillo Portero
"""

import arcade
import random


from src.RimboPlayer import RimboPlayer
from src.BugEnemy import BugEnemy

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 896
SCREEN_TITLE = "Debug the bug"
CHARACTER_SCALING = 0.5
TILE_SCALING = 0.5
GRAVITY = 1
SEMICOLON_MAX = 15


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # Create the player
        player1 = RimboPlayer()
        self.player1 = player1

        # Create SemiColon Enemy
        bug_enemy = BugEnemy()
        self.bug_enemy = bug_enemy

        # Create the background
        self.background_game = None

        # Create a list of enemies that interact or not with the player.
        self.listEnemies = arcade.SpriteList(None)

        # Created the basic engine for the movements.
        self.physicsP1 = None

    def setup(self):
        # Create your sprites and sprite lists here

        # Create a map
        self.background_game = arcade.load_texture(":resources:images/backgrounds/Matrix_background.jpeg")

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

        # Draw the enemies
        self.bug_enemy.bug_list.draw()

        if self.player1.isShooting:
            self.player1.blaster_list.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        """

        # Update the basic engine when keys are pressed.
        self.physicsP1.update()

        if self.player1.isShooting:
            self.player1.blaster_list.update()

        # Spawn enemies randomly. If there are more than 10 do not spawn more.
        if random.random() < 0.03 and self.bug_enemy.count < 10:
            self.bug_enemy.bugSprite()

        self.bug_enemy.bug_list.update()

        # Makes the bugs follow the player
        i = 0
        while i < self.bug_enemy.count:
            self.bug_enemy.followSprite(self.player1.player_sprite, self.bug_enemy.bug_list[i])
            i += 1

        # Get collisions of blasters with the bugs and kill them
        for shots in self.player1.blaster_list:
            bug_hit_list = arcade.check_for_collision_with_list(shots, self.bug_enemy.bug_list)
            for bugs in bug_hit_list:
                bugs.remove_from_sprite_lists()
                shots.remove_from_sprite_lists()
                self.bug_enemy.count -= 1

    def on_key_press(self, key, key_modifiers):

        self.player1.onKeyPressed(key)

    def on_key_release(self, key, key_modifiers):

        self.player1.onKeyReleased(key)


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
