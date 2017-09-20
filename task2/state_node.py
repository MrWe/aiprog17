class StateNode:
    def __init__(self, row_nodes, col_nodes, parent, g):
        self.row_nodes = row_nodes
        self.col_nodes = col_nodes
        self.heuristic = float("inf")
        self.parent = parent
        self.g = g
        self.f = self.heuristic + self.g
        self.set_h()
        self.hash = self.generate_hash()

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.hash == other.hash


    def generate_hash(self):
        hashString = ""
        for n in self.row_nodes:
            hashString += str(n.__dict__)
        for p in self.col_nodes:
            hashString += str(p.__dict__)
        return hashString

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