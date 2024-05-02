#Car Crash Simulator

import arcade
from arcade.experimental.uislider import UISlider
from arcade.gui.events import UIOnChangeEvent
import arcade.gui
import math
import time



SPRITE_SCALING_CAR = 1
MOVEMENT_SPEED = 4
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
            self.levelthree = LevelThree(self)
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

        self.collision = arcade.load_texture("CCScollision_nobg.png")

        arcade.draw_scaled_texture_rectangle(435, 550, self.collision, SPRITE_SCALING_CAR*0.5, 0)


class LevelOne(arcade.View):

    def __init__(self,main_view):
        super().__init__()

        self.all_sprites_list = arcade.SpriteList()
        self.car_list = arcade.SpriteList()
        self.playerOne_list = arcade.SpriteList()
        self.playerTwo_list = arcade.SpriteList()
        self.playerCrash_list = arcade.SpriteList()

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.switch = arcade.gui.UIFlatButton(text="Physics Dashboard", width=125)

        self.movement = True
        self.show_velocities = True
        self.collision = False
        self.crashsprite = False

        self.crash_sound = arcade.Sound("CCScar-crash-edited_2ojEpOXe.wav")

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
                align_x= 350,
                align_y=-260,
                child=self.Home_button))

        @self.Home_button.event("on_click")
        def on_click(event):
            self.home = OpenScreen()
            self.window.show_view(self.home)

        self.Reset_button = arcade.gui.UIFlatButton(text='Reset Position', width=125)
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                align_x=350,
                align_y=-205,
                child=self.Reset_button))

        @self.Reset_button.event("on_click")
        def on_click(event):
            if len(self.all_sprites_list) == 0 and len(self.car_list) == 0:
                self.playerOne = arcade.Sprite('CCSTessy1_Flipped.png', SPRITE_SCALING_CAR)


                self.playerTwo = arcade.Sprite('CCSTessy1.png', SPRITE_SCALING_CAR)


                # Add back to sprite lists
                self.all_sprites_list.append(self.playerTwo)
                self.car_list.append(self.playerOne)

                self.playerOne.change_y = 0
                self.playerOne.change_x = 0

                self.playerTwo.change_y = 0
                self.playerTwo.change_x = 0

            self.playerOne.center_x = 50
            self.playerOne.center_y = 50

            self.playerTwo.center_x = 600
            self.playerTwo.center_y = 600

            self.show_velocities = True
            self.movement = True
            self.collision = False
            self.crashsprite = False
            self.playerCrash_list = arcade.SpriteList()  # Clear any crash sprites


        self.playerOne = arcade.Sprite('CCSTessy1_Flipped.png', SPRITE_SCALING_CAR)
        self.playerOne.center_x = 50
        self.playerOne.center_y = 50

        self.playerTwo = arcade.Sprite('CCSTessy1.png', SPRITE_SCALING_CAR)
        self.playerTwo.center_x = 600
        self.playerTwo.center_y = 600

        self.all_sprites_list.append(self.playerTwo)
        self.car_list.append(self.playerOne)

        self.background = arcade.load_texture('CCSRuralbackground.png')
        self.physics_engine = arcade.PhysicsEngineSimple(self.playerOne, self.all_sprites_list)
        self.physics_engine2 = arcade.PhysicsEngineSimple(self.playerTwo, self.car_list)


    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH-200, SCREEN_HEIGHT, self.background)

        self.all_sprites_list.draw()
        self.car_list.draw()

        # Player One#

        arcade.draw_text('Player One', 750, 666, arcade.color.WHITE, 14, bold = True)

        if not self.crashsprite:
            self.position = f"Position: {round(self.playerOne.center_x,2)},{round(self.playerOne.center_y,2)}"
            arcade.draw_text(self.position, 715, 640, arcade.color.WHITE, 10)
        else:
            self.position = f"Position: {round(self.playerCrash.center_x, 2)},{round(self.playerCrash.center_y, 2)}"
            arcade.draw_text(self.position, 715, 640, arcade.color.WHITE, 10)

        self.playerOne.angle = math.atan2(self.playerOne.change_y, self.playerOne.change_x)
        self.playerOne_angle_deg = math.degrees(self.playerOne.angle)

        self.angle = f"Angle: {self.playerOne_angle_deg}"
        arcade.draw_text(self.angle, 715, 620, arcade.color.WHITE, 10)


        if self.show_velocities:
            arcade.draw_text(f'X-velocity: {round(self.playerOne.change_x,2)}', 715, 600, arcade.color.WHITE, 10)
            arcade.draw_text(f'Y-velocity: {round(self.playerOne.change_y,2)}', 715, 580, arcade.color.WHITE, 10)
        else:
            arcade.draw_text(f'Final X-Velocity: {round(self.final_x,2)}', 715, 600, arcade.color.WHITE, 10,
                             bold=True)
            arcade.draw_text(f'Final Y-Velocity: {round(self.final_y, 2)}', 715, 580, arcade.color.WHITE, 10,
                             bold=True)

        #Player Two#

        arcade.draw_text('Player Two', 750, 400, arcade.color.WHITE, 14, bold=True)

        if not self.crashsprite:
            self.position2 = f"Position: {round(self.playerTwo.center_x,2)},{round(self.playerTwo.center_y,2)}"
            arcade.draw_text(self.position2, 715, 380, arcade.color.WHITE, 10)

            self.playerTwo.angle = math.atan2(self.playerTwo.change_y, self.playerTwo.change_x)
            self.playerTwo_angle_deg = math.degrees(self.playerTwo.angle)
        else:
            self.position2 = f"Position: {round(self.playerCrash.center_x, 2)},{round(self.playerCrash.center_y, 2)}"
            arcade.draw_text(self.position2, 715, 380, arcade.color.WHITE, 10)

            self.playerTwo.angle = math.atan2(self.playerTwo.change_y, self.playerTwo.change_x)
            self.playerTwo_angle_deg = math.degrees(self.playerTwo.angle)


        self.angle2 = f"Angle: {self.playerTwo_angle_deg}"
        arcade.draw_text(self.angle2, 715, 360, arcade.color.WHITE, 10)

        if self.show_velocities:
            arcade.draw_text(f'X-velocity: {round(self.playerTwo.change_x,2)}', 715, 340, arcade.color.WHITE, 10)
            arcade.draw_text(f'Y-velocity: {round(self.playerTwo.change_y,2)}', 715, 320, arcade.color.WHITE, 10)
        else:
            arcade.draw_text(f'Final X-Velocity: {round(self.final_x,2)}', 715, 340, arcade.color.WHITE, 10,
                             bold=True)
            arcade.draw_text(f'Final Y-Velocity: {round(self.final_y, 2)}', 715, 320, arcade.color.WHITE, 10,
                             bold=True)

        if self.collision:
            self.playerOne.kill()
            self.playerTwo.kill()
            self.playerCrash_list.draw()

        self.manager.draw()

    def on_key_press(self, key, modifiers):
        if not self.movement:
            return

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

        if not self.movement:
            return

        if key in [arcade.key.UP, arcade.key.DOWN]:
            self.playerOne.change_y = 0
        if key in [arcade.key.LEFT, arcade.key.RIGHT]:
            self.playerOne.change_x = 0

        if key in [arcade.key.W, arcade.key.S]:
            self.playerTwo.change_y = 0
        if key in [arcade.key.A, arcade.key.D]:
            self.playerTwo.change_x = 0

    def on_update(self, delta_time):

        self.physics_engine.update()
        self.physics_engine2.update()

        self.all_sprites_list.update()
        self.car_list.update()
        self.playerCrash_list.update()

        if arcade.check_for_collision(self.playerOne, self.playerTwo):
            self.collisions()

        if self.playerOne.center_y < 0:
            self.playerOne.center_y = 0
        if self.playerOne.center_y > 700:
            self.playerOne.center_y = 700
        if self.playerOne.center_x < 0:
            self.playerOne.center_x = 0
        if self.playerOne.center_x > 666:
            self.playerOne.center_x = 666

        if self.playerTwo.center_y < 0:
            self.playerTwo.center_y = 0
        if self.playerTwo.center_y > 700:
            self.playerTwo.center_y = 700
        if self.playerTwo.center_x < 0:
            self.playerTwo.center_x = 0
        if self.playerTwo.center_x > 666:
            self.playerTwo.center_x = 666

        if self.crashsprite:
            if self.playerCrash.center_y < 40:
                self.playerCrash.center_y = 40
            if self.playerCrash.center_y > 660:
                self.playerCrash.center_y = 660
            if self.playerCrash.center_x < 40:
                self.playerCrash.center_x = 40
            if self.playerCrash.center_x > 640:
                self.playerCrash.center_x = 640

    def collisions(self):
        self.movement = False
        self.show_velocities = False
        self.collision = True

        self.mass_PO = 10
        self.mass_PT = 50
        self.combined_mass = self.mass_PO + self.mass_PT

        self.final_x = ((self.mass_PO*self.playerOne.change_x)/(self.combined_mass)) +((self.mass_PT*self.playerTwo.change_x)/(self.combined_mass))
        self.final_y = ((self.mass_PO*self.playerOne.change_y)/(self.combined_mass)) +((self.mass_PT*self.playerTwo.change_y)/(self.combined_mass))

        if not self.crashsprite:
            self.playerCrash = arcade.Sprite('carcrash.png', SPRITE_SCALING_CAR)
            self.playerCrash.center_x = (self.playerOne.center_x + self.playerTwo.center_x) / 2
            self.playerCrash.center_y = (self.playerOne.center_y + self.playerTwo.center_y) / 2
            self.playerCrash.change_x = self.final_x
            self.playerCrash.change_y = self.final_y
            self.playerCrash_list.append(self.playerCrash)
            self.crashsprite = True


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

        self.upload = arcade.gui.UIFlatButton(text="Upload Settings", width=100)

        #@self.upload.event("on_click")
        #def on_click(event):
            #needs to return, mass, acceleration (px/s^2), velocity(px/s)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                align_x=225,
                align_y=-315,
                child=self.upload))

        #player one#

        self.p1xacceleration_slider = UISlider(text="acceleration", width=200, value = 0)
        self.p1xacceleration = self.p1xacceleration_slider.value / 10
        self.p1axlabel = arcade.gui.UILabel(text=f"player one acceleration: {self.p1xacceleration:02.0f}")

        @self.p1xacceleration_slider.event()
        def on_change(event: UIOnChangeEvent):
            self.p1xacceleration = self.p1xacceleration_slider.value / 10
            self.p1axlabel.text = f"player one x acceleration: {self.p1xacceleration:02.0f}"
            self.p1axlabel.fit_content()

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                align_x=-150,
                align_y=200,
                child=self.p1xacceleration_slider))
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                align_x=-150,
                align_y=220,
                child=self.p1axlabel))





        self.p1yacceleration_slider = UISlider(text="acceleration", width=200, value = 0)
        self.p1yacceleration = self.p1yacceleration_slider.value / 10
        self.p1aylabel = arcade.gui.UILabel(text=f"player one y acceleration: {self.p1yacceleration:02.0f}")

        @self.p1yacceleration_slider.event()
        def on_change(event: UIOnChangeEvent):
            self.p1yacceleration = self.p1yacceleration_slider.value / 10
            self.p1aylabel.text = f"player one y acceleration: {self.p1yacceleration:02.0f}"
            self.p1aylabel.fit_content()

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                align_x=-150,
                align_y=100,
                child=self.p1yacceleration_slider))
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                align_x=-150,
                align_y=120,
                child=self.p1aylabel))

        self.p1mass_slider = UISlider(text="mass",width = 200, value = 0)
        self.p1mass = self.p1mass_slider.value
        self.p1masslabel = arcade.gui.UILabel(text = f"player one mass: {self.p1mass:02.0f}")

        @self.p1mass_slider.event()
        def on_change(event: UIOnChangeEvent):
            self.p1mass = self.p1mass_slider.value
            self.p1masslabel.text = f"player one mass: {self.p1mass:02.0f}"
            self.p1masslabel.fit_content()

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                align_x=-150,
                align_y=0,
                child=self.p1mass_slider))
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                align_x=-150,
                align_y=20,
                child=self.p1masslabel))

        #player two#

        self.p2xacceleration_slider = UISlider(text="acceleration", width=200)
        self.p2xacceleration = self.p2xacceleration_slider.value / 10
        self.p2axlabel = arcade.gui.UILabel(text = f"player two x acceleration: {self.p2xacceleration:02.0f}")

        @self.p2xacceleration_slider.event()
        def on_change(event: UIOnChangeEvent):
            self.p2xacceleration = self.p2xacceleration_slider.value / 10
            self.p2axlabel.text = f"player two x acceleration: {self.p2xacceleration:02.0f}"
            self.p2axlabel.fit_content()

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                align_x=150,
                align_y=200,
                child=self.p2xacceleration_slider))
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                align_x=150,
                align_y=220,
                child=self.p2axlabel))

        self.p2yacceleration_slider = UISlider(text="acceleration", width=200)
        self.p2yacceleration = self.p2yacceleration_slider.value/10
        self.p2aylabel = arcade.gui.UILabel(text= f"player two y acceleration: {self.p2yacceleration:02.0f}")

        @self.p2yacceleration_slider.event()
        def on_change(event: UIOnChangeEvent):
            self.p2yacceleration = self.p2yacceleration_slider.value / 10
            self.p2aylabel.text = f"player two y acceleration: {self.p2yacceleration:02.0f}"
            self.p2aylabel.fit_content()

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                align_x=150,
                align_y=100,
                child=self.p2yacceleration_slider))
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                align_x=150,
                align_y=120,
                child=self.p2aylabel))

        self.p2mass_slider = UISlider(text="mass",width = 200)
        self.p2mass = self.p2mass_slider.value
        self.p2masslabel = arcade.gui.UILabel(text = f"player two mass: {self.p2mass:02.0f}")

        @self.p2mass_slider.event()
        def on_change(event: UIOnChangeEvent):
            self.p2mass = self.p2mass_slider.value
            self.p2masslabel.text = f"player two mass: {self.p2mass:02.0f}"
            self.p2masslabel.fit_content()

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                align_x=150,
                align_y=0,
                child=self.p2mass_slider))
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                align_x=150,
                align_y=20,
                child=self.p2masslabel))

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






