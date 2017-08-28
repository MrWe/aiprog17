from util import get_all_neighbours, has_won
import lists


def a_star(board, start_node):
    open_list = lists.OpenList()
    open_list.push(start_node)
    closed_list = lists.ClosedList()

    while not open_list.is_empty():
        current_node = open_list.pop()

        if has_won(current_node):
            return current_node

        closed_list.push(current_node)

        for neighbour in get_all_neighbours(current_node):
            if closed_list.contains(neighbour):
                continue

            neighbour_g = current_node.get_g() + 1 #TODO: Add support for variable cost of one step

            if not open_list.contains(neighbour):
                open_list.push(neighbour)

            elif neighbour_g >= neighbour.get_g(): #Not an augmenting path
                continue

            #Wow we found a great new node with an augmenting path
            neighbour.parent = current_node

            neighbour.g = neighbour_g
            neighbour.f = neighbour_g + neighbour.get_h()
