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
        for j in range(len(d_nodes[i].domain)-1, -1, -1):
            valid_hits = [False] * len(d_nodes[0].domain[0])

            for m in range(len(d_nodes[i].domain[j])):
                for l in range(len(c_nodes[m].domain)):

                    if validate_intersect(d_nodes[i].domain[j][m], c_nodes[m].domain[l][i]):
                        #print("Intersect on row line", i, "in domain", j, "at index", m, "=", d_nodes[i].domain[j][m], "equaled c_node", k, "at domain", l, "on index", i)
                        valid_hits[m] = True

            for hit in valid_hits:
                if not hit:
                    del d_nodes[i].domain[j]
                    break

    return(d_nodes, changed_something)

def find_common_elements(node):
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

def common_elements_constraint(nodes_which_we_can_possibly_prune, nodes_which_we_check_against):
    new_nodes = nodes_which_we_can_possibly_prune
    for i in range(len(nodes_which_we_check_against)):
        common_elements = find_common_elements(nodes_which_we_check_against[i])

        for element in common_elements:
            new_nodes[element].domain = filter_on_specific_elements(element, common_elements[element], nodes_which_we_can_possibly_prune[element], i)

    hasChanged = False
    for i in range(len(new_nodes)):
        if new_nodes[i].__dict__ != nodes_which_we_can_possibly_prune[i].__dict__:
            hasChanged = True
            break

    return new_nodes, hasChanged

def validate_intersect(row_value, col_value):
    return row_value == col_value
