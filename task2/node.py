import itertools


class Node:
    def __init__(self, length, requirement):
        self.length = length
        self.requirement = requirement
        self.heuristic = 0
        self.domain = self.create_permutations(length, requirement)

    #Create all permutations of elements in requirement and add them to the domain
    def create_permutations(self, length, requirement):

        start_pos = 0
        temp = list(self.init_domain(length, requirement, start_pos))
        domain = []
        domain.append(list(temp))



        for i in range(length - sum(requirement)-1):
            index = 0

            for j in range(sum(requirement)-1+i, -1, -1):
                if(requirement[0] == length):
                    continue
                requirement_index = 0
                for h in range(j+1,len(temp)-index):


                    char = temp[h-1]
                    temp[h-1] = ''
                    temp[h] = char

                    domain.append(list(temp))
                    requirement_index += 1
                index += 1
            start_pos += 1
            #temp = list(self.init_domain(length, requirement, start_pos))
            temp = list([temp[-1]] + temp[:-1])
            domain.append(list(temp))
        del domain[-1]

        for n in domain:
            print(n)
        print("\n")

        #domain = list(set(itertools.permutations(domain)))

        return domain



    def init_domain(self, length, requirement, index):
        temp = ['']*(length)

        for i in range(len(requirement)):
            for k in range(requirement[i]):
                temp[index] = chr(65+i)
                index += 1
        return temp
