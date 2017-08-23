from board import Board
from car import Car
from node import Node
import copy

cars = "boards/easy-3.txt"
carsArray = []
board_size = 6
winningPosition = (5,2)
open_list = []


def main():
  #initialize empty board
  read_cars(name=cars)

  board = construct_board(carsArray)

  #node = Node(carsArray)
  #move_car(carsArray[0], -1, board)
  #node = Node(carsArray)
  print(board)
  open_list = get_all_neighbours(board)

  for carlist in open_list:
    for car in carlist:
      print(car)
    print("\n")

  print(board)
  print(has_won(carsArray[0], board))

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

def has_won(car, board):
  if not (car.Y, car.X) == winningPosition:
    if car.O == 0:
      return (car.Y + car.S, car.X) == winningPosition
    else:
      return (car.Y, car.X + car.S) == winningPosition
  return True

def read_cars(name):
  file = open(name)
  for line in file:
    l = line.split(',')
    carsArray.append(Car(int(l[0]), int(l[1]), int(l[2]), int(l[3])))

def get_all_neighbours(board):
  neighbours = []
  for i in range(len(carsArray)):
    copy1 = copy.deepcopy(carsArray)
    if(Car.is_valid_move(copy1[i], -1, construct_board(copy1))):
      move_car(copy1[i], -1, construct_board(copy1))
      neighbours.append(copy1)
    copy2 = copy.deepcopy(carsArray)
    if(Car.is_valid_move(copy2[i], 1, construct_board(copy2))):
      move_car(copy2[i], 1, construct_board(copy2))
      neighbours.append(copy2)

  return neighbours
