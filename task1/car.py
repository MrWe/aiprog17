class Car:
  def __init__(self, O, X, Y, S):
    self.O = O
    self.X = X
    self.Y = Y
    self.S = S

    '''
    params: move
    a move is a number indicating number of spaces a car should move in its given orientation
    '''
  def move(self, move):
    if move == 1 or move == -1:
        if(self.O == 0):
          self.X += move
        else:
          self.Y += move
    else:
        raise ValueError('Can only move one space at a time!')
