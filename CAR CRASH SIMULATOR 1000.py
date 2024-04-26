#Car Crash Simulator

import arcade
import arcade.gui
import math


SPRITE_SCALING_CAR = 1
MOVEMENT_SPEED = 5
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700

class OpenScreen(arcade.View):

    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.Welcome_label = arcade.gui.UILabel(
            text = "Welcome to Car Crash Simulator 1000!",
            font_name= "Times New Roman",
            font_size = 26,
            bold = True)

        self.Welcome_anchor = self.manager.add(
            arcade.gui.UIAnchorWidget(
            anchor_x= 'center',
            anchor_y= 'top',
            child = self.Welcome_label))

        self.LvlOne_button = arcade.gui.UIFlatButton(text = 'Level One', width = 125)
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x= 'center',
                align_y= 100,
                child=self.LvlOne_button))

        @self.LvlOne_button.event("on_click")
        def on_click(event):
            self.levelone = LevelOne(self)
            self.window.show_view(self.levelone)

        self.LvlTwo_button = arcade.gui.UIFlatButton(text='Level Two', width=125)
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x='center',
                align_y=40,
                child=self.LvlTwo_button))

        @self.LvlTwo_button.event("on_click")
        def on_click(event):
            self.leveltwo = LevelTwo(self)
            self.window.show_view(self.leveltwo)

        self.LvlThree_button = arcade.gui.UIFlatButton(text='Level Three', width=125)
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x='center',
                align_y=-20,
                child=self.LvlThree_button))

        @self.LvlThree_button.event("on_click")
        def on_click(event):
            self.levelthree = LevelTwo(self)
            self.window.show_view(self.levelthree)

        with open("CCS_Info.txt","r") as self.file:
            self.result = self.file.read()

        self.Welcome_anchor = self.manager.add(
            arcade.gui.UITextArea(
                x=0,
                y=0,
                height = 300,
                width = 900,
                text= self.result,
                font_name = "Times New Roman",
                font_size = 13,
                bold = True,
                multiline = True))



    def on_hide_view(self):
        self.manager.disable()

    def on_show_view(self):
        arcade.set_background_color(arcade.color.ARSENIC)
        self.manager.enable()

    def on_draw(self):
        arcade.start_render()
        self.clear()
        self.manager.draw()

        self.Tessy = arcade.load_texture("CCSTessy1.png")
        self.Benz = arcade.load_texture("CCSBenz1.png")
        self.Lambo = arcade.load_texture("CCSlambo1.png")

        arcade.draw_scaled_texture_rectangle(175, 550, self.Tessy, SPRITE_SCALING_CAR*2, 0)
        arcade.draw_scaled_texture_rectangle(450, 550, self.Benz, SPRITE_SCALING_CAR*2, 0)
        arcade.draw_scaled_texture_rectangle(700, 550, self.Lambo, SPRITE_SCALING_CAR*2, 0)





class LevelOne(arcade.View):

    def __init__(self,main_view):
        super().__init__()

        self.all_sprites_list = arcade.SpriteList()
        self.car_list = arcade.SpriteList()
        self.playerOne_list = arcade.SpriteList()
        self.playerTwo_list = arcade.SpriteList()

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.switch = arcade.gui.UIFlatButton(text="Physics Dashboard", width=125)

        @self.switch.event("on_click")
        def on_click(event):
            dash = PhysicsDashboard(self)
            self.window.show_view(dash)

        self.manager.add(
                arcade.gui.UIAnchorWidget(
                    align_x=350,
                    align_y=-315,
                    child=self.switch))

        self.Home_button = arcade.gui.UIFlatButton(text='Home', width=125)
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                align_x= 200,
                align_y=-315,
                child=self.Home_button))

        @self.Home_button.event("on_click")
        def on_click(event):
            self.home = OpenScreen()
            self.window.show_view(self.home)

        self.playerOne = arcade.Sprite('CCSTessy1.png', SPRITE_SCALING_CAR)
        self.playerOne.center_x = 50
        self.playerOne.center_y = 50
        self.playerOne_list.append(self.playerOne)

        self.playerTwo = arcade.Sprite('CCSTessy1.png', SPRITE_SCALING_CAR)
        self.playerTwo.center_x = 600
        self.playerTwo.center_y = 600
        self.playerTwo_list.append(self.playerTwo)

        self.all_sprites_list.append(self.playerTwo)
        self.car_list.append(self.playerOne)

        self.background = arcade.load_texture('CCSRuralbackground.png')
        self.physics_engine = arcade.PhysicsEngineSimple(self.playerOne, self.all_sprites_list)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.all_sprites_list.draw()
        self.car_list.draw()
        self.manager.draw()

        #need some type of interface in corners that show momentum, change in momentum,
        #heading (in case someone wants to calculate components),


    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.playerOne.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.playerOne.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.playerOne.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.playerOne.change_x = MOVEMENT_SPEED

        if key == arcade.key.W:
            self.playerTwo.change_y = MOVEMENT_SPEED
        elif key == arcade.key.S:
            self.playerTwo.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.A:
            self.playerTwo.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.playerTwo.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.playerOne.change_y = 0
        elif key == arcade.key.DOWN:
            self.playerOne.change_y = 0
        elif key == arcade.key.LEFT:
            self.playerOne.change_x = 0
        elif key == arcade.key.RIGHT:
            self.playerOne.change_x = 0

        if key == arcade.key.W:
            self.playerTwo.change_y = 0
        elif key == arcade.key.S:
            self.playerTwo.change_y = 0
        elif key == arcade.key.A:
            self.playerTwo.change_x = 0
        elif key == arcade.key.D:
            self.playerTwo.change_x = 0

    def on_update(self, delta_time):

        self.physics_engine.update()
        self.all_sprites_list.update()


        # Generate a list of all sprites that collided with the player.
        self.hit_list = arcade.check_for_collision_with_list(self.playerOne,
                                                        self.all_sprites_list)

        self.hit_list_2 = arcade.check_for_collision_with_list(self.playerTwo,
                                                               self.car_list)

        if self.playerTwo in self.hit_list_2:
            self.playerTwo.change_y = 0
            self.playerTwo.change_x = 0

        if self.playerOne.center_y < 0:
            self.playerOne.center_y = 0
        if self.playerOne.center_y > 700:
            self.playerOne.center_y = 700
        if self.playerOne.center_x < 0:
            self.playerOne.center_x = 0
        if self.playerOne.center_x > 900:
            self.playerOne.center_x = 900

        if self.playerTwo.center_y < 0:
            self.playerTwo.center_y = 0
        if self.playerTwo.center_y > 700:
            self.playerTwo.center_y = 700
        if self.playerTwo.center_x < 0:
            self.playerTwo.center_x = 0
        if self.playerTwo.center_x > 900:
            self.playerTwo.center_x = 900


class PhysicsDashboard(arcade.View):

    def __init__(self, game_view):
        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.exit = arcade.gui.UIFlatButton(text="Exit", width=100)

        @self.exit.event("on_click")
        def on_click(event):
            self.levelone = LevelOne(self)
            self.window.show_view(self.levelone)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                align_x=350,
                align_y=-315,
                child=self.exit))

        self.upload = arcade.gui.UIFlatButton(text="Upload", width=100)

        #@self.upload.event("on_click")
        #def on_click(event):
            #needs to return, mass, acceleration (px/s^2), velocity(px/s)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                align_x=225,
                align_y=-315,
                child=self.upload))

    def on_hide_view(self):
        self.manager.disable()

    def on_show_view(self):
        arcade.set_background_color(arcade.color.ARSENIC)
        self.manager.enable()

    def on_draw(self):
        self.clear()
        self.manager.draw()

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Car Crash Simulator 1000")
    main_view = OpenScreen()
    window.show_view(main_view)
    arcade.run()

if __name__ == "__main__":
    main()






