class Node:
  def __init__(self, cars, g, parent):
    self.cars = cars
    self.parent = parent
    self.h = self.get_heuristic()
    self.g = g


  '''
  Car[0] is currently hardcoded to be to rectangles long
  '''
  def get_heuristic(self):
    if(self.cars[0].S == 0):
      sx, sy = (self.cars[0].X + (self.cars[0].S - 1) , self.cars[0].Y)
    else:
      sx, sy = (self.cars[0].X, self.cars[0].Y + (self.cars[0].S - 1))
    ex, ey = (5, 2)
    return abs(ex - sx) + abs(ey - sy)
