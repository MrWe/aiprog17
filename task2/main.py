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

  row_nodes = []
  col_nodes = []

  for row in rows:
      row_nodes.append(node.Node(len(columns), row))
  for column in columns:
      col_nodes.append(node.Node(len(rows), column))

  # Constraints regarding seperate rows or cols
  for row_node in row_nodes:
      row_node.domain = constraints.reduce_domain(row_node.domain, [constraints.validate_alphabetical_order, constraints.validate_space_between_elements])
  for col_node in col_nodes:
      col_node.domain = constraints.reduce_domain(col_node.domain, [constraints.validate_alphabetical_order, constraints.validate_space_between_elements])

  # Constraints regarding combinations of rows
  for i in range(len(row_nodes)):

      for j in range(len(row_nodes[i].domain)):
          print(row_nodes[i].domain[j])

          for k in range(len(col_nodes)):

              row_must_be_deleted = True
              for l in range(len(col_nodes[k].domain)):


                  if constraints.validate_row_col(row_nodes[i].domain[j], col_nodes[k].domain[l], j, l):
                      row_must_be_deleted = False
                      break
      if row_must_be_deleted:
          row_nodes[i].domain.remove(row_nodes[i].domain[j]])

        #[row_nodes[i].domain, col_nodes[j].domain] = constraints.reduce_domains([row_nodes[i].domain, col_nodes[j].domain], [constraints.validate_row_col(row_nodes[i], col_nodes[j], i, j)])

  for row_node in row_nodes:
      print("ROW NODE DOMAIN:", row_node.domain)
  for col_node in col_nodes:
      print("COL NODE DOMAIN:", col_node.domain)

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
