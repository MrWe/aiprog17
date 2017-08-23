from board import Board
from car import Car
from node import Node
from astar import a_star
from util import construct_board

cars = "boards/medium-1.txt"
carsArray = []
open_list = []


def main():
  #initialize empty board
  carsArray = read_cars(name=cars)

  initNode = Node(carsArray, 0, None)
  board = construct_board(carsArray)

  a_star(board, initNode)

def read_cars(name):
  cars = []
  file = open(name)
  for line in file:
    l = line.split(',')
    cars.append(Car(int(l[0]), int(l[1]), int(l[2]), int(l[3])))

  return cars
