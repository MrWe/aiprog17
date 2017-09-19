import csp
import time
import sys
import constraints
import node
import time

#Write only filename to choose board
if len(sys.argv) > 1:
    in_file = "boards/" + sys.argv[1] + ".txt"
else:
    in_file = "boards/hut.txt"

def main():
  #initialize empty board
  rows, columns = read_board(in_file)
  rows = list(reversed(rows))

  t0 = time.time()
  row_nodes = []
  col_nodes = []

  for row in rows:
    row_nodes.append(node.Node(len(columns), row))

  for column in columns:
      col_nodes.append(node.Node(len(rows), column))

  todo_revise = []
  todo_revise.insert(0, constraints.common_elements_constraint)
  todo_revise.insert(0, constraints.intersect_constraint)

  while todo_revise:
    function = todo_revise.pop()
    row_nodes, col_nodes, colHasChanged, rowHasChanged = constraints.revise(row_nodes, col_nodes, function)

    if colHasChanged or rowHasChanged:
        todo_revise.insert(0, function)

  if not is_finished(row_nodes, col_nodes):
      print("No finish :(")

  display_ascii_image(row_nodes)
  t1 = time.time()
  print(t1-t0)
  return row_nodes

def is_finished(row_nodes, col_nodes):
    for node in row_nodes:
        if len(node.domain) != 1:
            return False
    for node in col_nodes:
        if len(node.domain) != 1:
            return False
    return True

def display_ascii_image(row_nodes):
  print("ROW NODES")
  for row in row_nodes:
      print(row.domain)

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