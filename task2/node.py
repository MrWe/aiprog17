import itertools

class Node:
    def __init__(self, length, requirement):
        self.length = length
        self.requirement = requirement
        self.heuristic = 0
        self.domain = self.create_permutations(length, requirement)

    #Create all permutations of elements in requirement and add them to the domain
    def create_permutations(self, length, requirement):
        temp = ['']*(length)
        domain = []
        index = 0
        for i in range(len(requirement)):
            for k in range(requirement[i]):
                temp[index] = chr(65+i)
                index += 1

        domain.append(list(temp))
        index = 0

        for j in range(sum(requirement)-1, -1, -1):
            if(requirement[0] == length):
                continue
            char = temp[j]

            for h in range(j+1,len(temp)-index):
                temp[h-1] = ''
                temp[h] = char
                domain.append(list(temp))
                #for l in range(requirement[index]):
            index += 1

        print(domain)
        print('\n')

        #domain = list(set(itertools.permutations(domain)))

        return domain
