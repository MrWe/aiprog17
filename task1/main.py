from car import Car

cars = "boards/easy-3.txt"
carsArray = []
board_size = 6

def main():
  board = []
  for i in range(board_size):
      board.append(["-"] * board_size)

  read_cars(name=cars)
  board = construct_board(board)
  pretty_print_board(board)
  move_car(carsArray[0], -1)
  board = construct_board(board)

  pretty_print_board(board)

def construct_board(board):
  board = []
  for i in range(board_size):
      board.append(["-"] * board_size)

  for i in range(len(carsArray)):
    car = carsArray[i]
    board[car.Y][car.X] = i #Obsobs, flipped coords to accomodate cartesian plane

    if(car.O == 1):
      for j in range(car.S):
        board[car.Y+j][car.X] = i
    if(car.O == 0):
      for j in range(car.S):
        board[car.Y][car.X+j] = i
  return board

def move_car(car, move):
  if(is_valid_move(car, move)):
    car.move(move)


def is_valid_move(car, move):
  return True

def read_cars(name):
  file = open(name)
  for line in file:
    l = line.split(',')
    carsArray.append(Car(int(l[0]), int(l[1]), int(l[2]), int(l[3])))

def pretty_print_board(board):
  s = [[str(e) for e in row] for row in board]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
  table = [fmt.format(*row) for row in s]
  print ('\n'.join(table))
main()
