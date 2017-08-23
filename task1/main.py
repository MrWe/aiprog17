from board import Board
from car import Car
from node import Node
from astar import a_star
import util

cars = "boards/expert-2.txt"
carsArray = []

def main():
  #initialize empty board
  carsArray = read_cars(name=cars)

  initNode = Node(carsArray, 0, None)
  board = util.construct_board(carsArray)
  path = a_star(board, initNode)
  return path

def read_cars(name):
  cars = []
  file = open(name)
  for line in file:
    l = line.split(',')
    cars.append(Car(int(l[0]), int(l[1]), int(l[2]), int(l[3])))

  return cars
