import csp
import time
import sys

#Write only filename to choose board
if len(sys.argv) > 1:
    in_file = "boards/" + sys.argv[1] + ".txt"
else:
    in_file = "boards/hut.txt"


def main():
  #initialize empty board
  rows, columns = read_board(in_file)
  hitlers_final_solution = csp.CSP(rows, columns)
  return rows, columns

def read_board(name):
  string_board = ""
  file = open(name)
  for line in file:
    string_board += line
  l = string_board.split('\n')
  rows = l[1:int(l[0].split(" ")[1])+1]
  columns = l[int(l[0].split(" ")[1])+1:]
  #list(reversed(rows)) Do we need this?
  return rows, columns

main()
