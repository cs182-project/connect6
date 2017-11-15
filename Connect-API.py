from Tkinter import Tk, Button, Frame, Canvas
from tkFont import Font
from copy import deepcopy
import random
from enum import Enum
import time

class Board:
  def __init__(self,other=None):
    self.player = 'X'
    self.opponent = 'O'
    self.empty = '.'
    self.width = 10
    self.height = 10
    self.connect = 4
    self.fields = {}
    for y in range(self.height):
      for x in range(self.width):
        self.fields[x,y] = self.empty
    if other:
      self.__dict__ = deepcopy(other.__dict__)

  def move(self,x,turn):
    board = Board(self)
    for y in range(board.height):
      if board.fields[x,y] == board.empty:
        if turn == 1:
          board.fields[x,y] = board.player
          break
        else:
          board.fields[x,y] = board.opponent
          break
    return board

  def check(self, moves):
    if len(moves)<self.connect:
      return []
    #Left Diagonal
    for i in moves:
      winning = []
      x,y = i
      winning.append(i)
      for z in range(1,self.connect):
        next = (x+z,y+z)
        if next in moves:
          winning.append(next)
        else:
          break
      if len(winning) == self.connect:
        return winning

    #Right Diagonal
    for i in moves:
      winning = []
      x,y = i
      winning.append(i)
      for z in range(1,self.connect):
        next = (x+z,y-z)
        if next in moves:
          winning.append(next)
        else:
          break
      if len(winning) == self.connect:
        return winning

    #Vertical
    for i in moves:
      winning = []
      x,y = i
      winning.append(i)
      for z in range(1,self.connect):
        next = (x,y+z)
        if next in moves:
          winning.append(next)
        else:
          break
      if len(winning) == self.connect:
        return winning

    #Horizontal
    for i in moves:
      winning = []
      x,y = i
      winning.append(i)
      for z in range(1,self.connect):
        next = (x+z,y)
        if next in moves:
          winning.append(next)
        else:
          break
      if len(winning) == self.connect:
        return winning
    return []


class PlayerType(Enum):
    Human = 1
    Bot = 2
    Random = 3

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
    self.auto_delay = 2
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

  def reset(self):
    self.board = Board()
    self.p1_positions, self.p2_positions = [], []
    self.flag = True
    self.game = False
    self.inputx = []
    self.game = self.update()
    self.turnCount = 0

  def avail_cols(self):
    filledCols = []
    for x,y in self.p1_positions + self.p2_positions:
      if y == self.board.height - 1:
        filledCols.append(x)
    availableCols = [x for x in range(self.board.height) if x not in filledCols]
    return availableCols

  def random_move(self,turn):
    if (self.turnCount == 0):
      move = random.choice(self.avail_cols())
      self.board = self.board.move(move,turn)
      self.game = self.update()
    else:
      for i in range(2):
        if self.game==False:
          move = random.choice(self.avail_cols())
          self.board = self.board.move(move,turn)
          self.game = self.update()
    self.turnCount = self.turnCount + 1

  def agent_move(self, turn):
    pass
    #if (self.turnCount == 0):
    #  move = get_agent_move()
    #  self.board = self.board.move(move,turn)
    #  self.game = self.update()
    #else:
    #  for i in range(2):
    #    if self.game==False:
    #      move = get_agent_move()
    #      self.board = self.board.move(move,turn)
    #      self.game = self.update()
    ###DO NOT REMOVE THIS LINE BELOW
    #self.turnCount = self.turnCount + 1

  def human_move(self,x,turn):
    for i in x:
      if self.game==False:
        self.board = self.board.move(i,turn)
        self.game = self.update()
    self.turnCount = self.turnCount + 1

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
        self.human_move(x,1)
      elif self.p1.name=="Bot":
        self.agent_move(1)
      else:
        self.random_move(1)
    if self.game==False:
      if self.p2.name=="Bot":
        self.agent_move(2)
      else:
        self.random_move(2)

  def autoplay(self):
    if self.game==False:
      if self.p1.name=="Bot":
        self.agent_move(1)
      else:
        self.random_move(1)
    if self.game==False:
      if self.p2.name=="Bot":
        self.agent_move(2)
      else:
        self.random_move(2)

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
