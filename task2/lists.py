import heapq

class List:
    def __init__(self):
        self.nodes = []

    def contains(self, other):

        return other in self.nodes

    def is_empty(self):
        return len(self.nodes) == 0

class OpenList(List): #we use a min-heap
    def __init__(self):
        super().__init__()

    def push(self, node):
        heapq.heappush(self.nodes,(node.f, node))

    def pop(self):
        return heapq.heappop(self.nodes)[1]

class ClosedList(List):
    def __init__(self):
        super().__init__()

    def push(self, node):
        self.nodes.append(node)

    def is_empty(self):
        return len(self.nodes) == 0
