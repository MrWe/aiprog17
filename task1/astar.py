from util import get_all_neighbours, has_won, construct_board, set_path

closed_set = []

class PriorityQueue: #we use a min-heap
    def __init__(self):
        self.nodes = []

    def __cmp__(self, other):
        return cmp(self.f, other.f) #order heap by f(n) value

    def contains(self, other):
        for node in self.nodes:
            if node == other:
                return True
        return False

    def is_empty(self):
        return len(self.nodes) == 0

    def push(self, node):
        self.nodes.append(node)
        self.nodes.sort(key=lambda x: x.f, reverse = True)

    def pop(self):
        self.nodes.sort(key=lambda x: x.f, reverse = True)
        node = self.nodes.pop()
        return node

def a_star(board, start_node):
    open_set = PriorityQueue()

    open_set.push(start_node)

    while not open_set.is_empty():
        current_node = open_set.pop()

        if has_won(current_node):
            print("Yay, we found the goal!")
            return current_node
            return path(current_node)

        closed_set.append(current_node)

        for neighbour in get_all_neighbours(current_node):
            if contains(neighbour):
                continue

            neighbour_g = current_node.get_g() + 1 #TODO: Add support for variable cost of one step

            if not open_set.contains(neighbour):
                open_set.push(neighbour)

            elif neighbour_g >= neighbour.get_g(): #Not an augmenting path
                continue

            #Wow we found a great new node with an augmenting path
            neighbour.parent = current_node

            neighbour.g = neighbour_g
            neighbour.f = neighbour_g + neighbour.get_h()

def contains(other):
    for node in closed_set:
        if node == other:
            return True
    return False

def path(current_node):
    set_path(current_node)
    while (current_node.parent):
        #print(construct_board(current_node.parent.cars), '\n')
        current_node = current_node.parent
