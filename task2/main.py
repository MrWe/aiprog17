import csp
import time
import sys
import constraints
import node

#Write only filename to choose board
if len(sys.argv) > 1:
    in_file = "boards/" + sys.argv[1] + ".txt"
else:
    in_file = "boards/hut.txt"



def main():
  #initialize empty board
  rows, columns = read_board(in_file)
  rows = list(reversed(rows))
  #print(rows)

  row_nodes = []
  col_nodes = []

  for row in rows:
    row_nodes.append(node.Node(len(columns), row))

  for column in columns:
      col_nodes.append(node.Node(len(rows), column))


  # Constraints regarding combinations of rows
  #print(constraints.constrainty(row_nodes, col_nodes))
  #print(constraints.constrainty(col_nodes, row_nodes))
  for i in range(len(col_nodes)):
      common_element = constraints.common_element(col_nodes[i])

      for element in common_element:
          row_nodes[element].domain = constraints.filter_on_specific_elements(element, common_element[element], row_nodes[element], i)

def read_board(name):
  string_board = ""
  file = open(name)
  for line in file:
    string_board += line
  l = string_board.split('\n')
  rows = l[1:int(l[0].split(" ")[1])+1]
  rows = [row.split(" ") for row in rows]
  for j in range(len(rows)):
      for i in range(len(rows[j])):
          rows[j][i] = int(rows[j][i])
  columns = l[int(l[0].split(" ")[1])+1:]
  columns = [col.split(" ") for col in columns]
  for j in range(len(columns)):
    for i in range(len(columns[j])):
      columns[j][i] = int(columns[j][i])
  #list(reversed(rows)) Do we need this?
  return rows, columns

main()
