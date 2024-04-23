#Car Crash Simulator

import arcade
from tkinter import *
import random
import math
import time

SPRITE_SCALING_CAR = 1
SPRITE_SCALING_PED = 0.2
MOVEMENT_SPEED = 2
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700

class OpenScreen():

    def __init__(self,root):
        self.root = root
        root.title("Car Crash Simulator 1000")
        self.font = ("Times New Roman",20)

        self.topFrame = Frame(self.root)
        self.topFrame.pack()

        #need welcome label
        #need start button and level selection

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

        #hides root, maybe prevents conflict with arcade interfaces
        self.root.withdraw()

        if self.LevelVar.get() == '1':
            start_game_one()
        elif self.LevelVar.get() == '2':
            start_game_two()
        else:
            start_game_three()



class LevelOne(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH,SCREEN_HEIGHT,"Level One")
        #sprite/background setup (pls finish this andrea)
        self.all_sprites_list = []
        self.car_list = []

        self.playerOne_list = []
        self.playerTwo_list = []

        self.set_mouse_visible(False)

        self.background = None

        #physics
        self.physics_engine = None

    def setup(self):

        self.all_sprites_list = arcade.SpriteList()
        self.car_list = arcade.SpriteList()
        self.playerOne_list = arcade.SpriteList()
        self.playerTwo_list = arcade.SpriteList()


        self.playerOne = arcade.Sprite('CCSTessy.png', SPRITE_SCALING_CAR)
        self.playerOne_center_x = 50
        self.playerOne_center_y = 50
        self.playerOne_list.append(self.playerOne)

        self.playerTwo = arcade.Sprite('CCSTessy.png', SPRITE_SCALING_CAR)
        self.playerTwo_center_x = 500
        self.playerTwo_center_y = 500
        self.playerTwo_list.append(self.playerTwo)

        self.all_sprites_list.append(self.playerTwo)

        self.car_list.append(self.playerOne)
        self.car_list.append(self.playerTwo)

        self.background = arcade.load_texture('CCSRuralbackground.png')
        self.physics_engine = arcade.PhysicsEngineSimple(self.playerOne, self.all_sprites_list)

    def on_draw(self):

        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)

    def on_key_press(self, key, modifiers):

        #need to change movement speed to stuff in terms of velocity/acceleration

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
        hit_list = arcade.check_for_collision_with_list(self.playerOne,
                                                        self.all_sprites_list)

        if self.playerOne in hit_list:
            self.playerOne.change_y = 0
            self.playerOne.change_x = 0


def start_game_one():
    window = LevelOne()
    window.setup()
    arcade.run()

def start_game_two():
    window = LevelTwo()
    window.setup()
    arcade.run()

def start_game_three():
    window = LevelThree()
    window.setup()
    arcade.run()


root = Tk()
screen = OpenScreen(root)
root.mainloop()



