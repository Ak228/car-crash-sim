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

class OpenScreen(arcade.Window):

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

        self.newWindow = Toplevel(root)

        with open("CCS_Info.txt","r") as self.file:
            self.result = self.file.read()

        self.text = Text(self.newWindow, font = self.font)
        self.text.pack()
        self.text.insert(END,self.result)

    def start(self):

        #hides root, maybe prevents conflict with arcade interfaces
        self.root.withdraw()

        if self.LevelVar.get() == '1':
            self.lvlone = LevelOne()
            self.lvlone.run()
        elif self.LevelVar.get() == '2':
            self.lvltwo = LevelTwo()
            self.lvltwo.run()
        else:
            self.lvlthree = LevelThree()
            self.lvlthree.run()



class LevelOne():

    def __init__(self):
        super.__init__(SCREEN_WIDTH,SCREEN_HEIGHT,"Level One")
        #sprite/background setup (pls finish this andrea)
        self.all_sprites_list = None
        self.car_list = None

        self.playerOne_list = None
        self.playerTwo_list = None

        self.set_mouse_visible(False)

        self.background = None

        #physics
        self.physics_engine = None

    def setup(self):
        
        self.all_sprites_list = arcade.SpriteList()
        self.car_list = arcade.SpriteList()
        
        #andrea
        #self.playerOne = arcade.Sprite(arguments)
        #self.playerOne_center_x = 
        #self.playerOne_center_y = 

        # self.playerTwo = arcade.Sprite(arguments)
        # self.playerTwo_center_x = 
        # self.playerTwo_center_y = 
        
        #self.background = arcade.load_texture(file name)
        
        #self.physics_engine = arcade.PhysicsEngineSimple(self.playerOne, self.playerTwo)
        

root = Tk()
screen = OpenScreen(root)
root.mainloop()



