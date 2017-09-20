# CSP Solver using A*
By Agnete Djupvik and Erik Wiker

## How to run
Requires installation of [Python 3.x](https://www.python.org/download/releases/3.0/) and [Tkinter](http://www.tkdocs.com/tutorial/install.html)
```
> python3 gui.py
```

Optional: Specify desired board. Defaults to Hut.

```
> python3 gui.py reindeer
```

## Representations
#### Variables
In this problem, we chose to represent a variable as one row or column and its representation, given in a boolean form.
A variable with a domain of length 1 can, as an example, look like this: ```101101 ``` given a length ```6``` and a constraint ```1 2 1 ```. Here, ```1``` represents a colored slot and ```0```a blank slot.


#### Domains
A domain represents all possible values of a row or column given a constraint (in this report referred to as _possibilities_).
In the classical thinking of CSP, one is to generate _all possible_ combinations of elements and removing them using constraints. However, given the combinatory nature of the domain space, the domain for a row of length _n_ could produce a domain of size close to _n<sup>n</sup>_.
This explains why we wanted to do some of the preprocessing in the domain generation itself instead of removing unwanted possibilities later. See more on the constraints implemented directly upon domain generation in the next subsection.

#### Constraints
The simplest constraints are implemented directly into the method for generating the initial state. This way, we reduce the workload of generating states which we know we will immediately prune away.
The constraints implemented while generating the initial state:
1. Keeping segments of length > 1 together
2. Keeping segments separated by one or more spaces

The two other constraints applied were the following:
1. **Common denominator elimination**. If a common element can be found for every possibility in the domain for a row (such as a specific space having to be colored no matter which of the possibilities we chose), this common element is applied as a constraint to intersecting column and vice versa.
2. **Intersecting elimination**. For a given element in a row, there has to exist a possibility in the domain of the intersecting column which satisfies the element in (that possibility of) the row, and vice versa.

The two constraints were applied in the order presented above (although in a loop for as long as they produced change in domains). This is because the intersecting elimination can be quite forgiving when domains are plentiful and varied. However, it proves much more effective for eliminating the last possibilities when domains are heavily diminished.

## Heuristics
Explains the heuristics used for this problem. Note that heuristics appear in at least two places in A*-GSP: a) in A*’s traditional h function, and b) in the choice of a variable on which to base the next assumption. Both (and others, if relevant) should be mentioned in the report.
Two different heuristics are used in the solving of an A*-CSP, and they can be found in a _node_ and a _state node_, respectively (these two nodes are described in more detail in Methods).
1. **Node heuristic**. Used in the general GAC. A node referring to a single row or column has the heuristic ```len(self.domain) - 1```. The desired effect here is to indicate that rows with a domain of length ```1``` has concluded in the search for a domain and we will no longer do any work on it.
2. **Node state heuristic**. Introduced along with A*. As each node state includes representations of all row and column nodes, the node state uses the _summed heuristic of all nodes' heuristics_. As we make assumptions in nodes in the state, the results discovered in the node are then reflected in this node state heuristic.

## Methods
1. **node.py**. Nodes in this program refer to a single row or column, with each nodes domain being all possible values for that row/column, both valid and invalid.
2. **state_node.py**. When A* is needed to complete a board, the program generates a state given the set of pruned column-nodes and row-nodes. Each state contains one or many representations of an entire board, both valid and invalid.
3. **constraints.py**. The constraints file contain the revise*-method. All calls to constraints from this method are made to problem-specific methods which will not work for other problems.

### Other design decisions
Not many other design decisions were made which significantly changed the architecture of the problem. However, it may be worth to mention that the input structure was changed. In the given task, the rows are counted from the _bottom up_. In order to make the row indexing communicate more nicely with Python indexing, the counting of rows were flipped so that it was iterating from the _top down_. The rationale for this decision mainly consisted of making the problem representation more intuitive and consistent with the programming language that was used.