import random
import arcade
import pygame as ps

# --- Constants ---
SPRITE_SCALING_PLAYER = 1
SPRITE_SCALING_COIN = 0.2
SPRITE_SCALING_COIN_EVIL = 0.2
SPRITE_SCALING_BOX = 0.3
COIN_COUNT = 50
MOVEMENT_SPEED = 2
VIEWPORT_MARGIN = 200
CAMERA_SPEED = 1

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# from arcade academy
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

        #physics
        self.physics_engine = None

        #cam
        self.camera_for_sprites = None
        self.camera_for_gui = None

        self.view_bottom = 0
        self.view_left = 0

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.all_sprites_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.coin_list_evil = arcade.SpriteList()

        self.camera_for_sprites = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.camera_for_gui = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

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

            # Position evil coins
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

            self.wall_list = arcade.SpriteList()

        #walls
        self.x_coordinates = list(range(100,SCREEN_WIDTH,70))
        self.y_coordinates = list(range(200,SCREEN_HEIGHT,50))

        for i in range(50):
            wall = arcade.Sprite("bad_block.png", SPRITE_SCALING_BOX)
            wall.center_x = random.choice(self.x_coordinates)
            wall.center_y = random.choice(self.y_coordinates)
            self.wall_list.append(wall)
            self.all_sprites_list.append(wall)

            # physics
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)


    def on_draw(self):
        """ Draw everything """
        arcade.start_render()

        self.camera_for_sprites.use()
        self.all_sprites_list.draw()
        self.camera_for_gui.use()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)

        if len(self.coin_list) == 0:
            arcade.draw_text("Game Over", 300, 500, arcade.color.WHITE, 28)


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.physics_engine.update()

        self.scroll_to_player()

        # Scroll the window to the player.
        #
        # If CAMERA_SPEED is 1, the camera will immediately move to the desired position.
        # Anything between 0 and 1 will have the camera move to the location with a smoother
        # pan.
        CAMERA_SPEED = 1
        lower_left_corner = (self.player_sprite.center_x - self.width / 2,
                             self.player_sprite.center_y - self.height / 2)
        self.camera_for_sprites.move_to(lower_left_corner, CAMERA_SPEED)

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

        # game over
        if len(self.coin_list) == 0:
            ps.mixer.pause()
            arcade.set_background_color(arcade.color.BLACK)
            for coin_evil in self.coin_list_evil:
                coin_evil.kill()
            for wall in self.wall_list:
                wall.kill()


    def scroll_to_player(self):
        """
        Scroll the window to the player.
        This method will attempt to keep the player at least VIEWPORT_MARGIN
        pixels away from the edge.

        if CAMERA_SPEED is 1, the camera will immediately move to the desired position.
        Anything between 0 and 1 will have the camera move to the location with a smoother
        pan.
        """

        # --- Manage Scrolling ---

        # Scroll left
        left_boundary = self.view_left + VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left

        # Scroll right
        right_boundary = self.view_left + self.width - VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary

        # Scroll up
        top_boundary = self.view_bottom + self.height - VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary

        # Scroll down
        bottom_boundary = self.view_bottom + VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom

        # Scroll to the proper location
        position = self.view_left, self.view_bottom
        self.camera_for_sprites.move_to(position, CAMERA_SPEED)

    def on_resize(self, width, height):
        """
        Resize window
        Handle the user grabbing the edge and resizing the window.
        """
        self.camera_for_sprites.resize(int(width), int(height))
        self.camera_for_gui.resize(int(width+1000), int(height+1000))

def main():
    window = MyWindow()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
