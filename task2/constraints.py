import itertools
import node

def revise(row_nodes, col_nodes, function):
      col_nodes, colHasChanged = function(col_nodes, row_nodes)
      row_nodes, rowHasChanged = function(row_nodes, col_nodes)

      return row_nodes, col_nodes, colHasChanged, rowHasChanged

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
                    changed_something = True
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
    changed_something = False

    for domain in domain_that_can_possibly_be_reduced.domain:
        if domain[row_index] == value and domain not in new_domain:
            new_domain.append(domain)
        else:
            changed_something = True

    return new_domain, changed_something

def common_elements_constraint(nodes_which_we_can_possibly_prune, nodes_which_we_check_against):
    new_nodes = list(nodes_which_we_can_possibly_prune)
    hasChanged = False

    for i in range(len(nodes_which_we_check_against)):
        common_elements = find_common_elements(nodes_which_we_check_against[i])

        for element in common_elements:
            new_nodes[element].domain, domainHasChanged = filter_on_specific_elements(element, common_elements[element], nodes_which_we_can_possibly_prune[element], i)
            if domainHasChanged:
                hasChanged = True

    return new_nodes, hasChanged

def validate_intersect(row_value, col_value):
    return row_value == col_value
