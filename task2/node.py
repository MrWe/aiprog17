import itertools


class Node:
    def __init__(self, length, requirement):
        self.length = length
        self.requirement = requirement
        self.heuristic = 0
        self.domain = self.generate_domain(length, requirement)
        self.duplicates = 0

    # Create all legal permutations of elements in requirement and add them to the domain
    # Implicit requirements: Pieces stick together and are separated by one or more spaces
    def generate_domain(self, length, requirement):
        # generate minimum placement
        domain = []
        min_placement = []
        for s in requirement:
            for i in range(s):
                min_placement.append(1)
            min_placement.append(0)
        min_placement.pop(len(min_placement) - 1)

        insert_indices = [i + 1 for i, x in enumerate(min_placement) if x == 0]
        insert_indices.extend([0, len(min_placement)])
        combinations = itertools.combinations_with_replacement(insert_indices, length - len(min_placement))
        for c in combinations:
            result = min_placement[:]
            insert_positions = list(c)
            insert_positions.sort()
            offset = 0
            for index in insert_positions:
                result.insert(index + offset, 0)
                offset += 1
            domain.append(result)
        return domain


    def move_elements(self, original):
        return [original[-1]] + original[:-1]



    def init_domain(self, length, requirement, index=0):

        temp = [' ']*(length-self.duplicates)

        for i in range(len(requirement)):
            group = []
            for k in range(requirement[i]):
                group.append(chr(65+i))
            temp[index] = list(group)
            index += 1

        return temp
