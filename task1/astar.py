class PriorityQueue: #we use a min-heap
    def __init__(self):
        self.nodes = []

    def __cmp__(self, other):
        return cmp(self.f, other.f) #order heap by f(n) value

    def contains(self, other):
        for node in self.nodes:
            if node.position == other.position:
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
