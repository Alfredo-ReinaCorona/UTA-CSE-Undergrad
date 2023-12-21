Alfredo Reina Corona ; 1001935392

Code was developed using Python 3.10.6 on linux mint

The "sys" library was imported in order to use command line arguments. No other library was used

The command line format of the code is:
expense_8_puzzle.py <start-file> <goal-file> <method>

For Example:
python3 expense_8_puzzle.py start.txt goal.txt astar

In the "<method>" section the input for the search algorithms are as follows:
bfs - Breadth First Search
ucs - Uniform Cost Search
grs - Greedy Search
astar - A* Search
dfs- Depth First Search
dls - Deapth Limited Search

The code is structured in a successive manner. All the functions are defined before the "main" function. Each searching algorithms has its own dedicated function. There are a few "tool" functions that where specifically made to help maintain clarity in the internal structure of the search functions(The manhattan Heuristic function being an example). 

As you can see, the dump flag was not sucessfully implimented so it was omitted from the code.

While mentioned in the code, I will list the resources I used here:
- https://www.w3schools.com/python/ was used to learn more about tuples and stack/queues, and python in general, as this is my first class that I've used python. Some code was inspired by code snippets available here

- h2 heuristic taught in class. code was inspired by  https:www.geeksforgeeks.org/sum-manhattan-distances-pairs-points/
(This is referring to the manhattan distance heuristic function I implimented)
