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
  def move(self, move, board):
    if self.is_valid_move(move, board):
        if(self.O == 0):
          self.X += move
        else:
          self.Y += move
        return True
    return False

  def is_valid_move(self, move, board):
     #1. Only move one space at a time
     if not (move == 1 or move == -1):
         print('Can only move one space at a time!')
         return False
     #2. Check that move will return a position within given indices
     if self.O == 0:
         if self.X + move > 5 or self.X + move < 0:
             print('Cannot move outside given X axis')
             return False
     if self.O == 1:
         if self.Y + move > 5 or self.Y + move < 0:
             print('Cannot move outside given Y axis')
             return False

     #3. Check that move will not leave us in a position where another car is located
     if self.O == 0:
         if move == 1:
             if self.X + self.S < len(board.boardArray) and not board.boardArray[self.Y][self.X + self.S] == '-':
                 print('Car', board.boardArray[self.Y][self.X + self.S], 'is already at spot', self.Y, self.X + move)
                 return False
         else:
             if not board.boardArray[self.Y][self.X + move] == '-':
                 print('Car', board.boardArray[self.Y][self.Y + move], 'is already at spot', self.Y, self.X + move)
                 return False
     if self.O == 1:
         if move == 1:
             if not board.boardArray[self.Y + self.S][self.X] == '-':
                 print('Car', board.boardArray[self.Y + self.S][self.X], 'is already at spot', self.Y + self.S, self.X)
                 return False
         else:
             if not board.boardArray[self.Y + move][self.X] == '-':
                 print('Car', board.boardArray[self.Y + move][self.X], 'is already at spot', self.Y + move, self.X)
                 return False

     return True
