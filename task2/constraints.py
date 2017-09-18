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

def reduce_domains(domains, constraints):
    #print("DOMAINS:", domains)
    new_domains = []
    for domain in domains:
        for constraint in constraints:
            new_domain = reduce_domain(domain, constraints)
            #print("NEW DOMAIN", new_domain)
            new_domains.append(new_domain)
    #print("NEW DOMAINS:", new_domains)
    return new_domains

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
    for i in range(1,len(row)):
        if row[i] == '':
            continue
        elif row[i] != '':
            if row[i-1] == '' or row[i-1] == row[i]:
                continue
            else:
                return False
    return True

def validate_row_col(row, col, row_index, col_index):
    return row.domain[0][col_index] == col.domain[0][row_index]


#row = ["", "A","","","","B"]
#col = ["", "","","","A",""]
#print(validate_row_col(row, col, 4, 1))

# Ensure that it is a space between any segment A and B
c1 = makefunc(['x','y','z'], 'x+y < z') #x = start(a), y= len(a), z = start(b)
c2 = makefunc(['x','y','z'], 'z > x+y')
