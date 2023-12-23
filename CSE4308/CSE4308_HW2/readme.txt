Alfredo Reina Corona
1001935392

Language Used:
Python 3.10.12

Code Structure:
The code is divided into 4 different functions and some driver code at the end
- red_blue_nim ; this function plays the game. It alternates between the computer and player declares the winner which depends on the versio being played

- computerTurn ; inside "red_blue_nim" when it is the computer's turn it calls this function. It return which of the 2 piles the computer will choose

- minmaxAlphaBeta ; this function is called within "computerTurn". It performs minmax search with alpha-beta pruning.

- evalFunction ; this function is called within "minmax_ab" and runs if the depth flag is set. It returns the favorability of the the state which then influences the computer's choices

- Driver Code ; does not belong to a function. Aquires the flag values from the command line


How to Run:
- Format: red_blue_nim.py <num-red> <num-blue> <version> <first-player> <depth>
- Command line Example ; python3 red_blue_nim.py 5 3 misere computer 10
- Note, the last 3 flags(version, firstPlayer, depth) are not required
- I have attempted to implement depth limited search


Sources:
- https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/

