import itertools
import node

def revise(row, constraint):
    for i in range(len(row)-1):
        for j in range(i+1, len(row)):
            if constraint(row[i], row[j]):
                return True
    return False

def reduce_domain():
    for constraint in constraints:
        for i in range(len(domain)-1,-1,-1):
            if revise(domain[i], constraint):
                domain.remove(domain[i])


def makefunc(names , expression , envir=globals()):
    args = ','.join(names) # eg [’x’,’y’,’z’] => ’x,y,z’
    return eval("(lambda " + args + ": " + expression + ")" , envir)

def intersect_row_col(row, col, index):
    if(row[index] == col[index]):
        pass
    return False

def validate_alphabetical_order(row):
    biggest = chr(0)
    for item in row:
        if item == "":
            continue
        elif item >= biggest:
            biggest = item
        else:
            return False
    return True


# Ensure that it is a space between any segment A and B
c1 = makefunc(['x','y','z'], 'x+y < z') #x = start(a), y= len(a), z = start(b)
c2 = makefunc(['x','y','z'], 'z > x+y')

# Make sure that all elements are in the correct order
c_alpha = makefunc(['row'], "validate_alphabetical_order(row)")

row = ('A', 'B', 'B', '', 'B', '')

print(c_alpha(row))
