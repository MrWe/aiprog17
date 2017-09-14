import itertools

class Node:
    def __init__(self, length, requirement):
        self.length = length
        self.requirement = requirement
        self.heuristic = 0
        self.domain = self.create_permutations(length, requirement)

    #Create all permutations of elements in requirement and add them to the domain
    def create_permutations(self, length, requirement):
        domain = ['']*(length)
        index = 0
        for i in range(len(requirement)):
            for k in range(requirement[i]):
                domain[index] = chr(65+i)
                index += 1
        domain = list(set(itertools.permutations(domain)))

        return domain
