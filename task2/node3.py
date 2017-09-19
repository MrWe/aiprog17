import itertools
import numpy as np

class Node:
    def __init__(self, length, requirement):
        self.length = length
        self.requirement = requirement
        self.heuristic = 0
        self.domain = self.create_permutations(length, requirement)

    #Create all permutations of elements in requirement and add them to the domain
    def create_permutations(self, length, requirement):

        num_duplicates = 0
        for i in requirement:
            num_duplicates += i-1


        temp = self.init_domain(length, requirement, num_duplicates)
        print(temp)
        domain = list(temp)
        return domain



    def init_domain(self, length, requirement, duplicates, index=0):
        temp = [' ']*(length-duplicates)

        for i in range(len(requirement)):
            group = []
            for k in range(requirement[i]):
                group.append(chr(65+i))
            temp[index] = list(group)
            index += 1

        return temp