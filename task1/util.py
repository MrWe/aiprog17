from board import Board
from car import Car
from node import Node
import copy
import time

board_size = 6
winningPosition = (5,2)
finished_path = []

def has_won(node):
  if not (node.cars[0].Y, node.cars[0].X) == winningPosition:
    if node.cars[0].O == 0:
      return (node.cars[0].X + node.cars[0].S -1, node.cars[0].Y) == winningPosition
    else:
      return (node.cars[0].X, node.cars[0].Y + node.cars[0].S - 1 ) == winningPosition
  return True

def set_path(path):
  finished_path = path

def get_all_neighbours(parent):
  neighbours = []
  for i in range(len(parent.cars)):
    copy1 = []
    copy2 = []
    for car in parent.cars:
      O, X, Y, S = car.O, car.X, car.Y, car.S
      copy1.append(Car(O, X, Y, S))
      copy2.append(Car(O, X, Y, S))
    board = construct_board(copy1)

    if(Car.is_valid_move(copy1[i], -1, board)):
      move_car(copy1[i], -1, board)
      neighbours.append(Node(copy1, parent.g+1, parent))

    if(Car.is_valid_move(copy2[i], 1, board)):
      move_car(copy2[i], 1, board)
      neighbours.append(Node(copy2, parent.g+1, parent))
  return neighbours

def construct_board(cars):
  board = []
  for i in range(board_size):
      board.append(["-"] * board_size)

  board = Board([], float('Inf'), float('Inf'), None)
  for i in range(board_size):
      board.boardArray.append(["-"] * board_size)

  for i in range(len(cars)):
    car = cars[i]
    board.boardArray[car.Y][car.X] = i #Obsobs, flipped coords to accomodate cartesian plane

    if(car.O == 1):
      for j in range(car.S):
        board.boardArray[car.Y+j][car.X] = i
    if(car.O == 0):
      for j in range(car.S):
        board.boardArray[car.Y][car.X+j] = i
  return board

def move_car(car, move, board):
  car.move(move, board)
