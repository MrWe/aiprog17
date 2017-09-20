class StateNode:
    def __init__(self, row_nodes, col_nodes, parent, g):
        self.row_nodes = row_nodes
        self.col_nodes = col_nodes
        self.heuristic = float("inf")
        self.parent = parent
        self.g = g
        self.f = self.heuristic + self.g

        for row_node in row_nodes:
            #print(row_node.domain)
            pass
        #print("\n")

        self.set_h()

    def __lt__(self, other):
        return self.f < other.f

    def set_h(self):
        h = 0
        for node in self.row_nodes:
            h += node.heuristic
        for node in self.col_nodes:
            h += node.heuristic
        self.heuristic = h

    def get_g(self):
        return self.g

    def get_h(self):
        return self.heuristic