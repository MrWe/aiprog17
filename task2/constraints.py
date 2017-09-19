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

def intersect_constraint(nodes_which_we_can_possibly_delete, nodes_which_we_check_against):
    row_must_be_deleted = None
    changed_something = False
    d_nodes = nodes_which_we_can_possibly_delete
    c_nodes = nodes_which_we_check_against

    for i in range(len(d_nodes)):
        for j in range(len(d_nodes[i].domain)):
            for k in range(len(c_nodes)):

                row_must_be_deleted = True
                for l in range(len(c_nodes[k].domain)):

                    if validate_intersect(d_nodes[i].domain[j], c_nodes[k].domain[l], i, k):
                        row_must_be_deleted = False
                        break

        if row_must_be_deleted:
            print("Removed a row")
            changed_something = True
            d_nodes[i].domain.remove(d_nodes[i].domain[j])

    return(d_nodes, changed_something)

def common_element(node):
    common_elements = {}

    for i in range(len(node.domain[0])):
        first_element = node.domain[0][0]

        for row in node.domain:
            if not row[i] == first_element:
                first_element = None
        if first_element != None:
            common_elements[i] = first_element

    return common_elements

def filter_on_specific_elements(element, value, domain_that_can_possibly_be_reduced, row_index):
    new_domain = []

    for domain in domain_that_can_possibly_be_reduced.domain:
        if domain[row_index] == value and domain not in new_domain:
            new_domain.append(domain)

    return new_domain

def super_constrainty(nodes_which_we_can_possibly_prune, nodes_which_we_check_against):
    new_nodes = nodes_which_we_can_possibly_prune
    for i in range(len(nodes_which_we_check_against)):
        common_elements = common_element(nodes_which_we_check_against[i])

        for element in common_elements:
            new_nodes[element].domain = filter_on_specific_elements(element, common_elements[element], nodes_which_we_can_possibly_prune[element], i)

    hasChanged = False
    for i in range(len(new_nodes)):
        if new_nodes[i].__dict__ != nodes_which_we_can_possibly_prune[i].__dict__:
            hasChanged = True
            break

    return new_nodes, hasChanged

def validate_intersect(row, col, row_index, col_index):
    #print("Row", row_index)
    #print("Col", col_index)
    #print(row[col_index] == col[row_index])
    #print("\n")
    return row[col_index] == col[row_index]

