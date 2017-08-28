import numpy as np
import random as r

class Node:
  def __init__(self, cars, g, parent):
    self.cars = cars
    self.parent = parent
    self.h = self.get_heuristic()
    self.g = g
    self.f = self.g + self.h

  def __eq__(self, other):
    for car in self.cars:
        hasEqual = False
        for other_car in other.cars:
            if car.__dict__ == other_car.__dict__:
                hasEqual = True
        if not hasEqual:
            return False

    return True



  def __str__(self):
      return 'I am a node' + str(self.h) + str(self.g)

  '''
  Car[0] is currently hardcoded to be to rectangles long
  '''
  def get_heuristic(self):
    if(self.cars[0].O == 0):
      sx, sy = (self.cars[0].X + (self.cars[0].S - 1) , self.cars[0].Y)
    else:
      sx, sy = (self.cars[0].X, self.cars[0].Y + (self.cars[0].S - 1))
    ex, ey = (5, 2)

    cars_infront_of_goal = 0

    for i in range(self.cars[0].X + self.cars[0].S, 5):
      itercars = iter(self.cars)
      next(itercars)
      for car in itercars:
        if(car.X == i or car.X + (car.S-1) == i):
          cars_infront_of_goal += 1
    return ((abs(ex - sx) + abs(ey - sy)) + cars_infront_of_goal)

  def get_g(self):
        return self.g

  def get_h(self):
        return self.h
