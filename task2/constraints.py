import itertools
import node

def revise(row, constraint):
    for i in range(len(row)-1):
        if not constraint(row):
            return True
    return False

def reduce_domain(domain, constraints):
    new_domain = domain
    for constraint in constraints:
        for i in range(len(domain)-1,-1,-1):
            if revise(domain[i], constraint):
                new_domain.remove(domain[i])
    return new_domain

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

def validate_space_between_elements(row):
    current = None

    for item in row:
        if item == '' and current == None:
            continue
        if item == 'A' and current == None:
            current = ord('A')
            continue

        if item == chr(current):
            continue
        elif item == '':
            current += 1
        elif item == chr(current-1):
            return False
        else:
            return False
    return True

def validate_row_col(row, col, row_index, col_index):
    return row[col_index] == col[row_index]


#row = ["", "A","","","","B"]
#col = ["", "","","","A",""]
#print(validate_row_col(row, col, 4, 1))

# Ensure that it is a space between any segment A and B
c1 = makefunc(['x','y','z'], 'x+y < z') #x = start(a), y= len(a), z = start(b)
c2 = makefunc(['x','y','z'], 'z > x+y')
