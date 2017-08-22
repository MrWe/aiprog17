from car import Car
from board import Board

cars = "boards/easy-3.txt"
carsArray = []
board_size = 6

def main():
  #initialize empty board
  board = []
  for i in range(board_size):
      board.append(["-"] * board_size)

  read_cars(name=cars)
  board = construct_board(board)


  print board
  move_car(carsArray[0], -1, board)
  board = construct_board(board)

  print board

def construct_board(board):
  board = Board([], float('Inf'), float('Inf'), None)
  for i in range(board_size):
      board.boardArray.append(["-"] * board_size)

  for i in range(len(carsArray)):
    car = carsArray[i]
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

def read_cars(name):
  file = open(name)
  for line in file:
    l = line.split(',')
    carsArray.append(Car(int(l[0]), int(l[1]), int(l[2]), int(l[3])))

main()
