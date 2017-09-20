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


## Methods
Briefly overviews the primary subclasses and methods needed to specialize your general-purpose A*-GAC system to handle nonograms.

### Other design decisions
Mentions any other design decisions that are, in your mind, critical to getting the system to perform well.