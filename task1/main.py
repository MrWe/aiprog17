from car import Car
from node import Node
from astar import a_star
import util
import time
import sys

#Write only filename to choose board
if len(sys.argv) > 1:
    cars = "boards/" + sys.argv[1] + ".txt"
else:
    cars = "boards/expert-2.txt"

def main():
  #initialize empty board
  carsArray = read_cars(name=cars)
  board = util.construct_board(carsArray)
  initNode = Node(carsArray, 0, None)
  t0 = time.time()
  path = a_star(initNode)
  t1 = time.time()
  print(t1-t0)
  return path if path else initNode

def read_cars(name):
  cars = []
  file = open(name)
  for line in file:
    l = line.split(',')
    cars.append(Car(int(l[0]), int(l[1]), int(l[2]), int(l[3])))
  return cars
