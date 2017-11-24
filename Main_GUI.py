from Tkinter import Tk, Button, Frame, Canvas
from tkFont import Font
from copy import deepcopy
import random
from enum import Enum
import time
from PlayerAgent import *
from ConnectBoard import *

class GUI:
  def __init__(self):
    self.board = Board()
    self.app = Tk()
    message  = "Connect" + str(self.board.connect) + " on Board : " + str(self.board.width)+"x"+str(self.board.height)
    self.app.title(message)
    self.app.resizable(width=False, height=False)
    self.buttons = {}
    self.frame = Frame(self.app, borderwidth=1, relief="raised")
    self.tiles = {}
    self.flag = True
    self.game = False
    self.inputx = []
    self.turnCount = 0
    self.p1_positions, self.p2_positions = [], []
    self.p1 = PlayerType(int(input('Player 1 is :\n1. Human \n2. Bot \n3. Random \n\n')))
    self.p2 = PlayerType(int(input('\nPlayer 2 is :\n1. Bot \n2. Random \n\n'))+1)
    self.human_flag = self.p1.name=="Human" or self.p2.name=="Human"
    for x in range(self.board.width):
      handler = lambda x=x: self.input(x)
      button = Button(self.app, command=handler, font=Font(family="Helvetica", size=14), text=x+1)
      button.grid(row=0, column=x, sticky="WE")
      self.buttons[x] = button
    self.frame.grid(row=1, column=0, columnspan=self.board.width)
    if not self.human_flag:
      for x in range(self.board.width):
        self.buttons[x]['state'] = 'disabled'
      handler = lambda: self.autoplay()
      self.auto = Button(self.app, command=handler, text='Next')
      self.auto.grid(row=3, column=0, columnspan=self.board.width, sticky="WE")
    for x,y in self.board.fields:
      tile = Canvas(self.frame, width=60, height=50, bg="navy", highlightthickness=0)
      tile.grid(row=self.board.height-1-y, column=x)
      self.tiles[x,y] = tile
    handler = lambda: self.reset()
    self.restart = Button(self.app, command=handler, text='Reset')
    self.restart.grid(row=2, column=0, columnspan=self.board.width, sticky="WE")
    self.game = self.update()

  def avail_cols(self):
    filledCols = []
    for x,y in self.p1_positions + self.p2_positions:
      if y == self.board.height - 1:
        filledCols.append(x)
    availableCols = [x for x in range(self.board.height) if x not in filledCols]
    return availableCols

  def reset(self):
    self.board = Board()
    self.p1_positions, self.p2_positions = [], []
    self.flag = True
    self.game = False
    self.inputx = []
    self.game = self.update()
    self.turnCount = 0

  def input(self,x):
    self.game = self.update()
    if self.game==False:
      self.inputx.append(x)
      if self.turnCount==0:
        self.move(self.inputx)
        self.inputx = []
      elif len(self.inputx)==2:
        self.move(self.inputx)
        self.inputx = []

  def move(self,x=None):
    if self.game==False:
      if self.p1.name=="Human":
        human = Human()
        human.move(self,x,1)
      elif self.p1.name=="Bot":
        bot = Bot()
        bot.move(self,1)
      else:
        rand_obj = RandomAgent()
        rand_obj.move(self,1)
    if self.game==False:
      if self.p2.name=="Bot":
        bot = Bot()
        bot.move(self,2)
      else:
        rand_obj = RandomAgent()
        rand_obj.move(self,2)

  def autoplay(self):
    if self.game==False:
      if self.p1.name=="Bot":
        bot = Bot()
        bot.move(self,1)
      else:
        rand_obj = RandomAgent()
        rand_obj.move(self,1)
    if self.game==False:
      if self.p2.name=="Bot":
        bot = Bot()
        bot.move(self,2)
      else:
        rand_obj = RandomAgent()
        rand_obj.move(self,2)

  def update(self):
    for (x,y) in self.board.fields:
      text = self.board.fields[x,y]
      if (text=='.'):
        self.tiles[x,y].create_oval(10, 5, 50, 45, fill="black", outline="blue", width=1)
      if (text=='X'):
        self.tiles[x,y].create_oval(10, 5, 50, 45, fill="yellow", outline="blue", width=1)
        if (x,y) not in self.p1_positions:
          self.p1_positions.append((x,y))
      if (text=='O'):
        self.tiles[x,y].create_oval(10, 5, 50, 45, fill="red", outline="blue", width=1)
        if (x,y) not in self.p2_positions:
          self.p2_positions.append((x,y))
    for x in range(self.board.width):
      if self.board.fields[x,self.board.height-1]==self.board.empty and self.human_flag:
        self.buttons[x]['state'] = 'normal'
      else:
        self.buttons[x]['state'] = 'disabled'
    if self.flag==False:
      self.flag = True
      return (self.end(self.board.check(self.p1_positions),1))
    else:
      self.flag = False
      return (self.end(self.board.check(self.p2_positions),2))


  def end(self, winning,turn):
    if winning!=[]:
      for x,y in winning:
        self.tiles[x,y].create_oval(25, 20, 35, 30, fill="black")
      for x in range(self.board.width):
        self.buttons[x]['state'] = 'disabled'
      print "\nGame Over! Player",turn,"has won!"
      return True
    return False


  def mainloop(self):
    self.app.mainloop()

if __name__ == '__main__':
  GUI().mainloop()
