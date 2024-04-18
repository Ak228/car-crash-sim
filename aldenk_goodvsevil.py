
import random
import arcade
import pygame as ps

# --- Constants ---
SPRITE_SCALING_PLAYER = 1
SPRITE_SCALING_COIN = 0.2
SPRITE_SCALING_COIN_EVIL = 0.2
COIN_COUNT = 50

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#from arcade academy
class Coin(arcade.Sprite):

    def __init__(self, filename, sprite_scaling):

        super().__init__(filename, sprite_scaling)

        self.change_x = 0
        self.change_y = 0

    def update(self):

        # Move the coin
        self.center_x += self.change_x
        self.center_y += self.change_y

        # If we are out-of-bounds, then 'bounce'
        if self.center_x < 0 or self.right > SCREEN_WIDTH:
            self.change_x *= -1

        if self.bottom < 0 or self.top > SCREEN_HEIGHT:
            self.change_y *= -1

class MyWindow(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Sprite Example")

        # Variables that will hold sprite lists
        self.all_sprites_list = None
        self.coin_list = None
        self.coin_list_evil = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        self.background = None
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.all_sprites_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.coin_list_evil = arcade.SpriteList()

        # Score
        self.score = 0

        # Set up the player
        # Character image from kenney.nl
        self.player_sprite = arcade.Sprite('sprite.png', SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.all_sprites_list.append(self.player_sprite)

        self.background = arcade.load_texture("boring background.png")

        # Create the coins
        for i in range(COIN_COUNT):

            # Create the coin instance
            # Coin image from kenney.nl
            coin = Coin('cat_goodvsevil1.png', SPRITE_SCALING_COIN)
            coin_evil = Coin('dog_goodvsevil1.png', SPRITE_SCALING_COIN_EVIL)

            # Position the coin
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)
            coin.change_x = random.randrange(-1, 1)
            coin.change_y = random.randrange(-3, 3)

            #Position evil coins
            coin_evil.center_x = random.randrange(SCREEN_WIDTH)
            coin_evil.center_y = random.randrange(SCREEN_HEIGHT)
            coin.change_x = random.choice([-3, 3])
            coin.change_y = random.choice([-3, 3])
            coin_evil.change_x = random.choice([-1, 1])
            coin_evil.change_y = random.choice([-1, 1])

            # Add the coin to the lists
            self.all_sprites_list.append(coin)
            self.all_sprites_list.append(coin_evil)
            self.coin_list.append(coin)
            self.coin_list_evil.append(coin_evil)

    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        self.all_sprites_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)

        if len(self.coin_list) == 0:
            arcade.draw_text("Game Over", 300, 500, arcade.color.WHITE, 28)
            
    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """

        # Move the center of the player sprite to match the mouse x, y
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.all_sprites_list.update()

        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                        self.coin_list)
        hit_list_evil = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list_evil)

        # Loop through each colliding sprite, remove it, and add to the score.
        for coin in hit_list:
            coin.kill()
            self.score += 1
            ps.mixer.init()
            sound = ps.mixer.Sound("cat.mp3")
            sound.play()

        for coin_evil in hit_list_evil:
            coin_evil.kill()
            self.score -= 1
            ps.mixer.init()
            sound = ps.mixer.Sound("frogs.mp3")
            sound.play()

        #game over
        if len(self.coin_list) == 0:
            ps.mixer.pause()
            arcade.set_background_color(arcade.color.BLACK)
            for coin_evil in self.coin_list_evil:
                coin_evil.kill()

def main():
    window = MyWindow()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
