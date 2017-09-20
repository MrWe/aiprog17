import state_node
import copy
import constraints

def get_all_neighbours(state):
    neighbours = []
    blacklist = []
    for i in range(len(state.row_nodes)):
        if len(state.row_nodes[i].domain) > 1:
            for j in range(len(state.row_nodes[i].domain)):

                modified_row_nodes = copy.deepcopy(state.row_nodes)
                modified_col_nodes = copy.deepcopy(state.col_nodes)

                modified_row_nodes[i].domain = [state.row_nodes[i].domain[j]]

                modified_state_node = state_node.StateNode(modified_row_nodes, modified_col_nodes, state_node, state.g + 1)

                try:
                    modified_state_node.row_nodes, modified_state_node.col_nodes = this_todo(modified_state_node.row_nodes, modified_state_node.col_nodes)
                    neighbours.append(modified_state_node)
                except IndexError:
                    print("Pruned down to zero :(")

    return neighbours


def this_todo(row_nodes, col_nodes):

    row_nodes, col_nodes, colHasChanged, rowHasChanged = constraints.revise(row_nodes, col_nodes)

    return row_nodes, col_nodes

def todo(row_nodes, col_nodes):
    todo_revise = []
    todo_revise.insert(0, constraints.revise)

    while todo_revise:
      function = todo_revise.pop()

      row_nodes, col_nodes, colHasChanged, rowHasChanged = constraints.revise(row_nodes, col_nodes)

      if len(row_nodes) == 0 and len(col_nodes) == 0:
          return row_nodes, col_nodes

      if colHasChanged or rowHasChanged:
          todo_revise.insert(0, function)
    return row_nodes, col_nodes



def has_won(state_node):
    for node in state_node.row_nodes:
        if len(node.domain) != 1:
            return False
    for node in state_node.col_nodes:
        if len(node.domain) != 1:
            return False
    return True