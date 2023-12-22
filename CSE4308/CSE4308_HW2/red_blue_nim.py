# Alfredo Reina Corona
# 1001935392

import sys

#return the favorability of the state when called(ok)
def evalFunction(redMarbles, blueMarbles, depth):
    
    value = 0
    
    #when there is a pile of 1, take it
    if redMarbles == 1 or blueMarbles == 1:
        #assign a high value in order to represent a favorable situation
        return 50 + depth  

    #increase the difference as much as possible between both piles in order to get the most points possibel
    value = redMarbles - blueMarbles

    return value


def minmaxAlphaBeta(alpha, beta, depth, maxValue, redMarbles, blueMarbles, version):
     
    #call the eval function when a depth of 0 is given or the game ends
    #misere used the oppitise eval
    #TODO: not implemented right
    if depth == 0 or (redMarbles == 0 and blueMarbles == 0):
        if version == 'misere':
            return -evalFunction(redMarbles, blueMarbles, depth)
        else:
            return evalFunction(redMarbles, blueMarbles, depth)


    #wether you get the max or min depends on the order taken during the game
    #recursively run through the tree, and prune(don't consier) less optimal branches
    #alpha ; get the maximum of the nodes in the layer below
    if maxValue:
        maxVal = float('-inf')
        for move in range(1, max(redMarbles, blueMarbles) + 1):
            if redMarbles >= move:
                maxVal = max(maxVal, minmaxAlphaBeta(alpha, beta, depth, False, redMarbles - move, blueMarbles, version))
                alpha = max(alpha, maxVal)
                
                if beta <= alpha:
                    break
                
            if blueMarbles >= move:
                maxVal = max(maxVal, minmaxAlphaBeta(alpha, beta, depth, False, redMarbles, blueMarbles - move, version))
                alpha = max(alpha, maxVal)
                
                if beta <= alpha:
                    break
                    
        return maxVal

    #beta ; get the minimum of the layer below
    else:
        minVal = float('inf')
        for move in range(1, max(redMarbles, blueMarbles) + 1):
            if redMarbles >= move:
                minVal = min(minVal, minmaxAlphaBeta(alpha, beta, depth, True, redMarbles - move, blueMarbles, version))
                beta = min(beta, minVal)
                
                if beta <= alpha:
                    break
                
            if blueMarbles >= move:
                minVal = min(minVal, minmaxAlphaBeta(alpha, beta, depth, True, redMarbles, blueMarbles - move, version))
                beta = min(beta, minVal)
                
                if beta <= alpha:
                    break

        return minVal

#TODO: only works whn depth is defined?? Dosent take the last marble???
def computerTurn(redMarbles, blueMarbles, version, depth):
    alpha = float('-inf')
    beta = float('inf')
    redEval = float('-inf')
    blueEval = float('-inf')
    optimalRedMove = None
    optimalBlueMove = None

    #get the favorability of each state when the computer takes either a red or blue marble
    if redMarbles > 0:
        eval_result = minmaxAlphaBeta(alpha, beta, depth, False, redMarbles - 1, blueMarbles, version)
        if eval_result > redEval:
            redEval = eval_result
            optimalRedMove = (redMarbles - 1, blueMarbles)

    if blueMarbles > 0:
        eval_result = minmaxAlphaBeta(alpha, beta, depth, False, redMarbles, blueMarbles - 1, version)
        if eval_result > blueEval:
            blueEval = eval_result
            optimalBlueMove = (redMarbles, blueMarbles - 1)

    #the best move should be reflected by the eval function
    #of the 2 possible moves take the one that has the most favorability
    if blueEval <= redEval:
        return optimalRedMove
    else:
        return optimalBlueMove

#where the game is played(ok)
def red_blue_nim(redMarbles, blueMarbles, version, currentPlayer, depth):
    
    while redMarbles > 0 and blueMarbles > 0:
        print(f"Red Marbles: {redMarbles}, Blue Marbles: {blueMarbles}")
        
        #Computer's Turn 
        if currentPlayer == 'computer':
            computerMove = computerTurn(redMarbles, blueMarbles, version, depth)
            redMarbles, blueMarbles = computerMove
            print(f"Computer removes 1 marble (Red: {computerMove[0]}, Blue: {computerMove[1]})")
            
        #Human's Turn
        else:
            humanMove = input("Remove marble from Red(r) or Blue(b) pile: ").lower()
            if humanMove == 'r':
                redMarbles -= 1
            elif humanMove == 'b':
                blueMarbles -= 1
            else:
                print("Invalid move. Please enter 'r' or 'b'.")
                continue

        print()
       
       #at the end of the turn, switch the players
        if currentPlayer == 'human':
            currentPlayer = 'computer'
        else:
            currentPlayer = 'human'

    #"Game Over" conditions differ depending on version
    if redMarbles == 0 or blueMarbles == 0 :
        
        score = 3 * blueMarbles + 2 * redMarbles
    
        if version == "standard":
            if currentPlayer == 'human':
                winner = 'Computer'
            else:
                winner = 'Human'
                
            print(f"{winner} wins with a score of: {score}")
        
        else:
            if currentPlayer == 'human':
                winner = 'Human'
            else:
                winner = 'Computer'
                
            print(f"{winner} wins with a score of: {score}")




#driver code
if len(sys.argv) < 3:
    print("Format: red_blue_nim.py <num-red> <num-blue> <version> <first-player> <depth>")

redMarbles = int(sys.argv[1])
blueMarbles = int(sys.argv[2])

if len(sys.argv) > 3:
    version = sys.argv[3].lower()
else:
    version = 'standard'

if  len(sys.argv) > 4:
    firstPlayer = sys.argv[4].lower()
else:
    firstPlayer = 'computer'
    
if len(sys.argv) > 5:
    depth = int(sys.argv[5]) 
else:
    #max depth is N-1 so to simulate that there is no depth set it as the maximum size
    #only doing this becasue I've structured by code in a way that it wont run unless depth>0
    depth = redMarbles + blueMarbles -1

red_blue_nim(redMarbles, blueMarbles, version, firstPlayer, depth)
