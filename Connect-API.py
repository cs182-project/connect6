from Tkinter import Tk, Button, Frame, Canvas
from tkFont import Font
from copy import deepcopy
import random

class Board:
  def __init__(self,other=None):
    self.player = 'X'
    self.opponent = 'O'
    self.empty = '.'
    self.width = 7
    self.height = 7
    self.connect = 6
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
    self.p1_positions, self.p2_positions = [], []
    
    #initiate turnCount for every time player moves. Doesn't count opponent's moves. Used in def move
    self.turnCount = 0
    
    for x in range(self.board.width):
      handler = lambda x=x: self.move(x)
      button = Button(self.app, command=handler, font=Font(family="Helvetica", size=14), text=x+1)
      button.grid(row=0, column=x, sticky="WE")
      self.buttons[x] = button
    self.frame.grid(row=1, column=0, columnspan=self.board.width)
    
    for x,y in self.board.fields:
      tile = Canvas(self.frame, width=60, height=50, bg="navy", highlightthickness=0)
      tile.grid(row=self.board.height-1-y, column=x)
      self.tiles[x,y] = tile
    handler = lambda: self.reset()
    self.restart = Button(self.app, command=handler, text='reset')
    self.restart.grid(row=2, column=0, columnspan=self.board.width, sticky="WE")
    self.game = self.update()

  def reset(self):
    self.board = Board()
    self.p1_positions, self.p2_positions = [], []
    self.flag = True
    self.game = False
    self.game = self.update()
    #reset turn counter
    self.turnCount = 0

  def move(self,x):
      
    #if turn count is odd, then player plays a stone and computer plays two stones
    if not (self.turnCount % 2 == 0):
        if self.game == False:
          self.app.config(cursor="watch")
          self.board = self.board.move(x,1)
          self.game = self.update()
          
        if self.game == False:          
          #check for filled columns that the computer cannot place a stone in
          filledCols = []
          for x,y in self.p1_positions + self.p2_positions:              
              if y == self.board.height - 1:
                  filledCols.append(x)
          availableCols = [x for x in range(self.board.height) if x not in filledCols]         
          #computer places a stone randomly in an available column
          move = random.choice(availableCols)
          self.board = self.board.move(move,2)
          self.game = self.update()
          
        if self.game == False:              
          #check for filled columns that the computer cannot place a stone in
          for x,y in self.p1_positions + self.p2_positions:
              if y == self.board.height - 1:
                  if x not in filledCols:
                      filledCols.append(x)
          availableCols = [x for x in range(self.board.height) if x not in filledCols]  
          #computer places a stone randomly in an available column
          move = random.choice(availableCols)
          self.board = self.board.move(move,2)
          self.game = self.update()
          #increment turn count
          self.turnCount = self.turnCount + 1
          
    #if turn count is even, then player plays one stone
    else:  
        if self.game == False:
          self.app.config(cursor="watch")
          self.board = self.board.move(x,1)
          self.game = self.update()   
          #increment turn count
          self.turnCount = self.turnCount + 1
    self.app.config(cursor="")

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
      if self.board.fields[x,self.board.height-1]==self.board.empty:
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
