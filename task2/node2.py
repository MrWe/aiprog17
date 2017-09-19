import itertools


class Node:
    def __init__(self, length, requirement):
        self.length = length
        self.requirement = requirement
        self.heuristic = 0
        self.domain = self.create_permutations(length, requirement)
        self.duplicates = 0

    #Create all permutations of elements in requirement and add them to the domain
    def create_permutations(self, length, requirement):

        num_duplicates = 0
        for i in requirement:
            num_duplicates += i-1
        self.duplicates = num_duplicates
        start_pos = 0
        temp = self.init_domain(length, requirement, start_pos)

        domain = []
        domain.append(list(itertools.chain(*temp)))
        original = list(temp)

        for n in range(length-sum(requirement)):
            index = 0
            temp = list(original)
            for element in range(sum(requirement)-num_duplicates, -1, -1):
                if(temp[element] == ' '):
                    continue
                for i in range(element+1, len(temp)-index):
                    char = temp[i-1]
                    temp[i-1] = ' '
                    temp[i] = char
                    domain.append(list(itertools.chain(*temp)))
                index += 1
            start_pos += 1
            original = list(self.move_elements(list(original)))
            temp = list(original)
            domain.append(list(itertools.chain(*temp)))

        for n in domain:
            print(n)
        print("\n")

        #return domain


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
