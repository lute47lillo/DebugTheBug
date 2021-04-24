"""
Author: Lute Lillo Portero
"""

# TODO: Create another enemy that shoots to the player
# TODO: Create Round system

import arcade
import random
import time


from src.RimboPlayer import RimboPlayer
from src.BugEnemy import BugEnemy

# Init variables
SCREEN_WIDTH = 1324
SCREEN_HEIGHT = 796
SCREEN_TITLE = "Debug the bug"
TILE_SCALING = 0.5

# Attributes
CHARACTER_SCALING = 0.5
GRAVITY = 1
LIFE_SCALING = 0.1
BOOSTER_SCALING = 1


# Sounds
MUSIC_VOLUME = 0.2
COLLISION_SOUND = 0.15
GAMEOVER_SOUND = 0.4


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # Create the player
        player1 = RimboPlayer()
        self.player1 = player1

        # Create attributes of the player health
        self.player_health = 10
        self.player_health_sprite = None
        self.player_health_list = arcade.SpriteList()
        self.game_over = False

        # Set the score for debugging bugs
        self.score = 0
        self.actual_round = 0

        # Create Bug Enemy
        bug_enemy = BugEnemy()
        self.bug_enemy = bug_enemy

        # Create coffee booster sprite
        self.coffee_sprite = None
        self.coffee_list = arcade.SpriteList()
        self.boosted = False
        self.coffee_count = 0
        self.booster_sprite = None
        self.boost_list = arcade.SpriteList()

        # Create the background
        self.background_game = None

        # Create a list of enemies that interact or not with the player.
        self.listEnemies = arcade.SpriteList(None)

        # Created the basic engine for the movements.
        self.physicsP1 = None
        self.total_time = 0.0

        # Create different sound effects
        self.kill_sound = None
        self.shoot_sound = None
        self.collision_player_sound = None
        self.game_over_sound = None

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
        self.total_time = 0.0

        # List of music
        self.music_list = [":resources:music/funkyrobot.mp3"]
        # Array index of what to play
        self.current_song_index = 0
        # Play the song
        self.play_song()

        # Set sound for killing bugs
        self.kill_sound = arcade.load_sound(":resources:sounds/hit4.wav")

        # Set sound for collision between player and bugs
        self.collision_player_sound = arcade.load_sound(":resources:sounds/hurt2.wav")

        # Set the sound for picking up the booster
        self.pick_booster_sound = arcade.load_sound(":resources:sounds/upgrade1.wav")

        # Set the players lives
        self.players_health()

        self.game_over_sound = arcade.load_sound(":resources:sounds/gameover2.wav")

    def on_draw(self):

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background_game)

        if self.game_over:
            output = "GAME OVER"
            arcade.draw_text(output, 400, SCREEN_HEIGHT/2, arcade.color.PURPLE_HEART, 70, bold=True)

        # Set up the score for bugs killed
        output_score = f"Bugs debugged {self.score}"
        arcade.draw_rectangle_filled(1395, 740, 800, 50, arcade.color.BLACK)
        arcade.draw_text(output_score, 1000, 720, arcade.color.WHITE, 30, bold=True, italic=True)

        # Call draw() on all your sprite lists below
        self.player1.player_list.draw()
        self.listEnemies.draw()
        self.player_health_list.draw()

        # Draw the enemies
        self.bug_enemy.bug_list.draw()

        if self.player1.isShooting:
            self.player1.blaster_list.draw()

        self.coffee_list.draw()
        self.boost_list.draw()

    def on_update(self, delta_time):

        # Update the basic engine when keys are pressed.
        self.physicsP1.update()

        if self.player1.isShooting:
            self.player1.blaster_list.update()

        # Spawn enemies randomly. If there are more than 10 do not spawn more.
        if random.random() < 0.03 and self.bug_enemy.count < 10 and self.actual_round == 0:
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
                self.score += 1

        # Get collisions of bugs with player
        for bugs in self.bug_enemy.bug_list:
            if arcade.check_for_collision(bugs, self.player1.player_sprite) and not self.game_over and not self.boosted:
                arcade.play_sound(self.collision_player_sound)
                self.player_health_list.pop().remove_from_sprite_lists()
                self.bug_enemy.count -= 1
                self.player_health -= 1
                bugs.remove_from_sprite_lists()
                self.player_health_list.update()
                self.check_player_life()

        # Get the position on the stream of the song to repeatedly play it
        position = self.music.get_stream_position(self.current_player)
        if position == 0.0:
            self.play_song()

        self.total_time += delta_time

        # Start timer for booster. Disappears after x seconds
        start_booster = self.coffee_booster(self.total_time)
        stop_booster = start_booster + 13
        if self.boosted:
            if self.total_time > stop_booster:
                self.boosted = False
                self.boost_list.pop().remove_from_sprite_lists()

        self.coffee_list.update()
        self.boost_list.update()

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
    def coffee_booster(self, actual_time):

        now = 0
        image_source = "/Users/lutelillo/Desktop/DebugTheBug/lib/python3.8/" \
                       "site-packages/arcade/resources/images/createdSprites/coffee_boost.png"

        # Create the booster
        if self.actual_round == 0 and self.coffee_count < 1:
            self.coffee_sprite = arcade.Sprite(image_source, BOOSTER_SCALING)
            rand_center_x = random.randrange(SCREEN_WIDTH)
            rand_center_y = random.randrange(SCREEN_HEIGHT)
            self.coffee_sprite.center_x = rand_center_x
            self.coffee_sprite.center_y = rand_center_y
            self.coffee_list.append(self.coffee_sprite)
            self.coffee_count += 1

        # Check if player picks it up
        for coffee in self.coffee_list:
            if arcade.check_for_collision(self.player1.player_sprite, coffee):
                arcade.play_sound(self.pick_booster_sound)
                self.coffee_list.pop().remove_from_sprite_lists()
                self.boosted = True
                now = actual_time

                # Create visual aid to indicate that the booster has been picked up
                boost_source = "/Users/lutelillo/Desktop/DebugTheBug/lib/python3.8/" \
                               "site-packages/arcade/resources/images/createdSprites/powerup.png"

                self.booster_sprite = arcade.Sprite(boost_source, BOOSTER_SCALING)
                self.booster_sprite.center_x = 50
                self.booster_sprite.center_y = SCREEN_HEIGHT - 50
                self.boost_list.append(self.booster_sprite)

        return now

    # Creates the visual aid for the remaining lives of the player
    def players_health(self):

        image_source = "/Users/lutelillo/Desktop/DebugTheBug/lib/python3.8/" \
                       "site-packages/arcade/resources/images/createdSprites/heart_pixel.png"
        offset = 25
        for i in range(self.player_health):
            self.player_health_sprite = arcade.Sprite(image_source, LIFE_SCALING)
            self.player_health_sprite.center_x = 50 + offset
            self.player_health_sprite.center_y = 20
            self.player_health_list.append(self.player_health_sprite)
            offset += 25

    def check_player_life(self):

        # Check health of player
        if self.player_health == 0 and not self.game_over:
            self.player1.player_sprite.remove_from_sprite_lists()
            self.player1.player_list.update()
            arcade.play_sound(self.game_over_sound, GAMEOVER_SOUND)
            self.game_over = True


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
