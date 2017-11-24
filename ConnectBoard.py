from Tkinter import Tk, Button, Frame, Canvas
from tkFont import Font
from copy import deepcopy
import random
from enum import Enum
import time
from Main_GUI import *
from PlayerAgent import *

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
