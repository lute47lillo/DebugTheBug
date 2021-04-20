"""
Author: Lute Lillo Portero
"""

import arcade
import random
import time


from src.RimboPlayer import RimboPlayer
from src.BugEnemy import BugEnemy

SCREEN_WIDTH = 1324
SCREEN_HEIGHT = 796
SCREEN_TITLE = "Debug the bug"
CHARACTER_SCALING = 0.5
TILE_SCALING = 0.5
GRAVITY = 1
SEMICOLON_MAX = 15
MUSIC_VOLUME = 0.2


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

        # Create different sound effects
        self.kill_sound = None
        self.shoot_sound = None

        # Attributes of background music
        self.music_list = []
        self.current_song_index = 0
        self.current_player = None
        self.music = None

    def setup(self):

        # Create a map
        self.background_game = arcade.load_texture(":resources:images/backgrounds/Matrix_background.jpeg")

        # Created the basic engine for the movements.
        self.physicsP1 = arcade.PhysicsEngineSimple(self.player1.player_sprite, self.listEnemies)

        # List of music
        self.music_list = [":resources:music/funkyrobot.mp3"]
        # Array index of what to play
        self.current_song_index = 0
        # Play the song
        self.play_song()

        # Set sound for killing bugs
        self.kill_sound = arcade.load_sound(":resources:sounds/hit4.wav")

    def on_draw(self):

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
                arcade.play_sound(self.kill_sound)
                self.bug_enemy.count -= 1

        # Get the position on the stream of the song to repeatedly play it
        position = self.music.get_stream_position(self.current_player)
        if position == 0.0:
            self.play_song()

    def on_key_press(self, key, key_modifiers):

        self.player1.onKeyPressed(key)

    def on_key_release(self, key, key_modifiers):

        self.player1.onKeyReleased(key)

    # Plays background music
    def play_song(self):
        self.music = arcade.Sound(self.music_list[self.current_song_index], streaming=True)
        self.current_player = self.music.play(MUSIC_VOLUME)
        time.sleep(0.03)

    # Spawn coffee booster
    def coffee_buster(self):
        pass


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
