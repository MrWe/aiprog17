class Node:
  def __init__(self, cars, g):
    self.cars = cars
    self.parent = None
    self.h = self.get_heuristic()
    self.g = g


  def get_heuristic(self):
    sx, sy = (self.cars[0].X + (self.cars[0].S - 1) , self.cars[0].Y)
    ex, ey = (5, 2)
    return abs(ex - sx) + abs(ey - sy)
