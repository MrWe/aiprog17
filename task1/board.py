class Board:
    def __init__(self, boardArray, g, h, parent):
        self.boardArray = boardArray
        self.g = g
        self.h = h
        self.parent = parent

    def __str__(self):
      #Note: Not self-produced as we did not consider it very relevant for the task at hand
      s = [[str(e) for e in row] for row in self.boardArray]
      lens = [max(map(len, col)) for col in zip(*s)]
      fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
      table = [fmt.format(*row) for row in s]
      return ('\n'.join(table))
