StateTableTools
===============

Tools to support transforming tabular representations of state machines into other formats

Background
----------

State machines may be represented in a variety of ways.  May engineers are
familiar with textual descriptions of a graphical state-chart of some form.
This paper [1] gives a useful overview of how state machines may be
represented in a tabular format.
When representing state machines in a tabular format it's often still
useful to have a graphical representation to aid comprehension

Example
-------

The following table (based on the example used in the paper [1]):

                      | open_door | close_door       | lock           | unlock           | push_in
    Opened            |           | Closed, Unlocked |                |                  |
    Closed, Unlocked  | Opened    |                  | Closed, Locked |                  | Broken
    Closed, Locked    |           |                  |                | Closed, Unlocked | Broken
    Broken            |           |                  |                |                  |

StateTableTools can take that and build an alternative representation which
[GraphViz](http://www.graphviz.org/) can turn into something like this:

![Example state chart](https://raw.github.com/bright-tools/StateTableTools/master/test/example_2.png)

Usage
-----

Coming soon ...

References
----------

[1] http://www.crosstalkonline.org/storage/issue-archives/2008/200803/200803-Herrmannsdrfer.pdf
