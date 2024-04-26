#Car Crash Simulator

import arcade
import arcade.gui
from tkinter import *
import math


SPRITE_SCALING_CAR = 1
MOVEMENT_SPEED = 5
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700

class OpenScreen():

    def __init__(self,root):
        self.root = root
        root.title("Car Crash Simulator 1000")
        self.font = ("Times New Roman",20)

        self.topFrame = Frame(self.root)
        self.topFrame.pack()

        self.Welcomelabel = Label(self.topFrame, text = 'Welcome to Car Crash Simulator 1000!',
                            font = self.font)
        self.Welcomelabel.pack()

        self.LevelLabel = Label(self.topFrame, text = 'Level',font =('Times 18 underline'))
        self.LevelList = [1,2,3]
        self.LevelVar = StringVar(self.topFrame)
        self.LevelVar.set(1)
        self.Level = OptionMenu(self.topFrame, self.LevelVar, *self.LevelList,)

        self.LevelLabel.pack()
        self.Level.pack()

        self.StartButton = Button(self.topFrame, text = 'Start', command=self.start)
        self.StartButton.pack()

        self.InstructionsButton = Button(self.topFrame, text = 'Instructions',command = self.getinfo)
        self.InstructionsButton.pack()

    def getinfo(self):

        self.newWindow = Toplevel(self.root)

        with open("CCS_Info.txt","r") as self.file:
            self.result = self.file.read()

        self.text = Text(self.newWindow, font = self.font)
        self.text.pack()
        self.text.insert(END,self.result)

    def start(self):

        selected_level = int(self.LevelVar.get())

        if selected_level == 1:
            start_game(selected_level)
        elif selected_level == 2:
            start_game(selected_level)
        elif selected_level == 3:
            start_game(selected_level)

class LevelOne(arcade.View):

    def __init__(self):
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

    def __init__(self, main_view):
        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.exit = arcade.gui.UIFlatButton(text="Exit", width=100)

        @self.exit.event("on_click")
        def on_click(event):
            self.levelone = LevelOne()
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

def start_game(selected_level):

    if selected_level == 1:
        window = arcade.Window(SCREEN_WIDTH,SCREEN_HEIGHT,"Level One")
        main_view = LevelOne()
        window.show_view(main_view)
        arcade.run()
    elif selected_level == 2:
        window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Level Two")
        main_view = LevelTwo()
        window.show_view(main_view)
        arcade.run()
    else:
        window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Level Three")
        main_view = LevelThree()
        window.show_view(main_view)
        arcade.run()

root = Tk()
screen = OpenScreen(root)
root.mainloop()





