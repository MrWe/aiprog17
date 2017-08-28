from util import get_all_neighbours, has_won, construct_board, set_path
import heapq
closed_list = []
closed_set = set()

class PriorityQueue: #we use a min-heap
    def __init__(self):
        self.nodes = []
        self.set = set()

    def contains(self, other):
        return other.hash in self.set

    def is_empty(self):
        return len(self.nodes) == 0

    def push(self, node):
        heapq.heappush(self.nodes,(node.f, node))
        self.set.add(node.hash)
        #self.nodes.sort(key=lambda x: x.f, reverse = True)

    def pop(self):
        #self.nodes.sort(key=lambda x: x.f, reverse = True)
        return heapq.heappop(self.nodes)[1]

def a_star(board, start_node):
    open_set = PriorityQueue()

    open_set.push(start_node)

    while not open_set.is_empty():
        current_node = open_set.pop()

        if has_won(current_node):
            print("Yay, we found the goal!")
            return current_node

        closed_list.append(current_node)
        closed_set.add(current_node.hash)

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
    return other.hash in closed_set

def path(current_node):
    set_path(current_node)
    while (current_node.parent):
        #print(construct_board(current_node.parent.cars), '\n')
        current_node = current_node.parent
