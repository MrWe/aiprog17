import itertools

def generate_permutations(row, len_row):
    domain = ['']*(len_row-1)
    index = 0
    for i in range(len(row)):
        for k in range(row[i]):
            domain[index] = chr(65+i)
            index += 1
    domain = list(set(itertools.permutations(domain)))
    isDeleted = False
    for i in range(len(domain)-1,-1,-1):
        for k in range(len(domain[i])-1):
            for j in range(k+1, len(domain[i])):
                if(domain[i][k] == '' or domain[i][j] == ''):
                    continue
                if c5(domain[i][k], domain[i][j]):
                    domain.remove(domain[i])
                    isDeleted = True
                    break
            if(isDeleted):
                isDeleted = False
                break

    domain = list(set(domain))

    for n in domain:
        print(n)

    #options = list(filter(lambda ))


def revise():
    pass


def makefunc(names , expression , envir=globals()):
    args = ','.join(names) # eg [’x’,’y’,’z’] => ’x,y,z’
    return eval("(lambda " + args + ": " + expression + ")" , envir)

def intersect_row_col(row, col, index):
    if(row[index] == col[index]):
        pass
    return False

c1 = makefunc(['x','y','z'], 'x+y < z') #x = start(a), y= len(a), z = start(b)
c2 = makefunc(['x','y','z'], 'z > x+y')

c3 = makefunc(['x'], 'x >= 0')
c4 = makefunc(['x', 'y'], 'x < y') #y = len(board)-1

c5 = makefunc(['x', 'y'], 'x > y')

