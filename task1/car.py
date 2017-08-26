class Car:
  def __init__(self, O, X, Y, S):
    self.O = O
    self.X = X
    self.Y = Y
    self.S = S

  def __str__(self):
    return("Y:" + str(self.Y) + " " "X:" + str(self.X))

  def __cmp__(self, other):
    return self.__dict__ == other.__dict__

    '''
    params: move
    a move is a number indicating number of spaces a car should move in its given orientation
    '''
  def move(self, move, parent):
    if self.is_valid_move(move, parent):
        if(self.O == 0):
          self.X += move
        else:
          self.Y += move
        return True
    return False

  def is_valid_move(self, move, parent):
    #1. Only move one space at a time
    if not (move == 1 or move == -1):
        print('Can only move one space at a time!')
        return False
    #2. Check that move will return a position within given indices
    if self.O == 0:
        if self.X + move + self.S - 1 > 5 or self.X + move < 0:
            #print('Cannot move outside given X axis')
            return False
    if self.O == 1:
        if self.Y + move + self.S - 1 > 5 or self.Y + move < 0:
            #print('Cannot move outside given Y axis')
            return False

    #3. Check that move will not leave us in a position where another car is located
    '''
    if self.O == 0:
      if move == 1:
        for car in parent:
          if not (car == self):
            if self.X + move == car.X: #and (self.Y == car.Y or self.Y == (car.Y + car.S-1)*car.O):
              return False
      elif move == - 1:
        for car in parent:
          if not (car == self):
            if self.X - 1 == car.X + car.S - 1:# and (self.Y == car.Y or self.Y == (car.Y + car.S-1)*car.O):
              return False
    if move == 1:
      for car in parent:
        if not (car == self):
          if self.Y + self.S - 1  == car.Y:# and (self.X == car.X or self.X == (car.X + car.S - 1)*car.O):
            return False
    elif move == - 1:
      for car in parent:
        if not (car == self):
          if self.Y - 1 == car.Y + car.S - 1:# and (self.X == car.X or self.X == (car.X + car.S - 1)*car.O):
            return False
    '''

    if self.O == 0:
      if move == 1:
        for car in parent:
          if not (car is self):
            if self.X + self.S == car.X and car.Y <= self.Y <= car.Y + ((car.S-1)*car.O):
              return False
      elif move == - 1:
        for car in parent:
          if not (car is self):
            if self.X - 1 == car.X + ((car.S-1) * (1 if car.O == 0 else 0 )) and car.Y <= self.Y <= car.Y + ((car.S-1)*car.O):
              return False
    if move == 1:
      for car in parent:
        if not (car is self):
          if self.Y + self.S == car.Y and car.X <= self.X <= car.X + ((car.S-1) * (1 if car.O == 0 else 0 )):
            return False
    if move == - 1:
      for car in parent:
        if not (car is self):
          if self.Y - 1 == car.Y + (car.S-1)*car.O and car.X <= self.X <= car.X + ((car.S-1) * (1 if car.O == 0 else 0 )):
            return False

    return True




    '''
     if self.O == 0:
         if move == 1:
             if not board.boardArray[self.Y][self.X + self.S] == '-':
                 #print('Car', board.boardArray[self.Y][self.X + self.S], 'is already at spot', self.Y, self.X + move)
                 return False
         else:
             if not board.boardArray[self.Y][self.X + move] == '-':
                 #print('Car', board.boardArray[self.Y][self.X + move], 'is already at spot', self.Y, self.X + move)
                 return False
     if self.O == 1:
         if move == 1:
             if not board.boardArray[self.Y + self.S][self.X] == '-':
                 #print('Car', board.boardArray[self.Y + self.S][self.X], 'is already at spot', self.Y + self.S, self.X)
                 return False
         else:
             if not board.boardArray[self.Y + move][self.X] == '-':
                 #print('Car', board.boardArray[self.Y + move][self.X], 'is already at spot', self.Y + move, self.X)
                 return False
    '''
     #return True
