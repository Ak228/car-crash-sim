#Car Crash Simulator

import arcade
from tkinter import *
import random
import math

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

        if self.LevelVar.get() == '1':
            self.lvlone = LevelOne()
        elif self.LevelVar.get() == '2':
            self.lvltwo = LevelTwo()
        else:
            self.lvlthree = LevelThree()


#class LevelOne():








root = Tk()
screen = OpenScreen(root)
root.mainloop()



