import sys
#https://www.w3schools.com/python/ was used to learn more about tuples and stack/queue implemintations withput external libraries. 
#Some code was inspired by code snippets available here

def firstIndex(item):
        return item[0]

#Gets the coordinates of the 0 tile
def zeroTileCoordinates(board):
    for x in range(3):
        for y in range(3):
            if board[x][y] == 0:
                return x, y

def goalState(board):
    goalFile = sys.argv[2]
    goalFileArray = []

    #move the goal file into an array, exluding the "END OF FILE", line
    with open(goalFile, "r") as goalFile:
            for lines in goalFile:
                #remove any whitespace
                lines = lines.strip()

                if lines != "END OF FILE":
                    #split lines into the array
                    elements = lines.split()
                    
                    #make sure the elements are intigers
                    for element in elements:
                        fileElement = int(element)  
                        goalFileArray.append(fileElement)

    #essentially return a 3x3 matrix
    return board == [[goalFileArray[0], goalFileArray[1], goalFileArray[2]], [goalFileArray[3], goalFileArray[4], goalFileArray[5]], [goalFileArray[6], goalFileArray[7], goalFileArray[8]]]

#calculate the cost of moving an arbritrary tile
#cost sould be equal to the number of the tile, i.e moving tile 8 will increase the cost by 8
def tileCost(board, newBoard):
    x, y = zeroTileCoordinates(newBoard)
    tile = board[x][y]
    
    if tile != 0:
        return tile
    else:
        return 0

#implimentation of the breadth first search algorithm
def breadthFirstSearch(startingBoard):

    #initialize the queue
    startingCost = 0
    statingDepth = 0
    startingPath = []
    queue = [(startingBoard, startingCost, statingDepth, startingPath)] 

    explored = set()
    poppedNodes = 0
    expandedNodes = 0
    totalNodesGenerated = 0
    finalFringeSize = 0
    depth = -1

    while queue:
        #pop the defined elements for processing
        board, cost, depth, steps = queue.pop(0)
        poppedNodes += 1
        #define a starting board as already explored
        explored.add(tuple(map(tuple, board)))

        if goalState(board):
            depth = depth
            return cost, poppedNodes, expandedNodes, totalNodesGenerated, depth, finalFringeSize, steps

        #get location of the 0 tile as we move it around
        i, j = zeroTileCoordinates(board)

        #Right,Left,Down,Up represent the movement of the 0 tile. In order to get the direction of the tile moved, swap the naming conventions
        #for x, y, move in [(i, j - 1, "Left"), (i, j + 1, "Right"), (i - 1, j, "Up"), (i + 1, j, "Down")]:
        for x, y, move in [(i, j - 1, "Right"), (i, j + 1, "Left"), (i - 1, j, "Down"), (i + 1, j, "Up")]:
            if 0 <= x < 3 and 0 <= y < 3:
                newBoard = [list(row) for row in board]
                #swap board values
                newBoard[i][j], newBoard[x][y] = newBoard[x][y], newBoard[i][j]
                #Map the new position of 0 to the "old" board and see what tile was there before
                tileSwapped = board[x][y]  
                totalNodesGenerated += 1
                
                #"If the new configurate after a swap is not in the explored list" 
                newState = tuple(tuple(row) for row in newBoard)
                if newState not in explored:
                    #add the new move to the "steps" fortion of the tuple
                    nextStep = steps + [f"Move {tileSwapped} {move}"] 
                    #cost+tileCost() is the new total cost
                    queue.append((newBoard, cost + tileCost(board, newBoard), depth + 1, nextStep))
                    expandedNodes += 1
                    finalFringeSize = len(queue)

    return -1, poppedNodes, expandedNodes, totalNodesGenerated, depth, finalFringeSize, []

def uniformCostSearch(startingBoard):

    startingCost = 0
    startingDepth = 0
    startingPath = []
    queue = [(startingCost, startingBoard, startingDepth, startingPath)] 

    explored = set()
    poppedNodes = 0
    expandedNodes = 0
    totalNodesGenerated = 0
    finalFringeSize = 0
    depth = -1

    while queue:
        cost, board, depth, steps = queue.pop(0)
        poppedNodes += 1
        explored.add(tuple(map(tuple, board)))

        if goalState(board):
            depth = depth
            return cost, poppedNodes, expandedNodes, totalNodesGenerated, depth, finalFringeSize, steps

        i, j = zeroTileCoordinates(board)

        #very similar to breadth first search, refer back to it for explinations on the code
        for x, y, move in [(i, j - 1, "Right"), (i, j + 1, "Left"), (i - 1, j, "Down"), (i + 1, j, "Up")]:
            if 0 <= x < 3 and 0 <= y < 3:
                newBoard = [row[:] for row in board]
                newBoard[i][j], newBoard[x][y] = newBoard[x][y], newBoard[i][j]
                tileSwapped = board[x][y] 
                totalNodesGenerated += 1

                #"If the new configurate after a swap is not in the explored list" 
                newState = tuple(tuple(row) for row in newBoard)
                if newState not in explored:
                    nextStep = steps + [f"Move {tileSwapped} {move}"]  
                    queue.append(( cost + tileCost(board, newBoard), newBoard, depth + 1, nextStep))

                    #sort by the first index(cost)
                    queue.sort(key=firstIndex)

                    expandedNodes += 1
                    finalFringeSize = len(queue)

    return -1, poppedNodes, expandedNodes, totalNodesGenerated, depth, finalFringeSize, []

#h2 heuristic taught in class
# code was inspired by https://www.geeksforgeeks.org/sum-manhattan-distances-pairs-points/
def manhattanDistance(board):
    blocks = 0
    for x in range(3):
        for y in range(3):
            tile = board[x][y]
            if tile != 0:
                goalRow, goalCol = divmod(tile - 1, 3)
                blocks += abs(x - goalRow) + abs(y - goalCol)

    return blocks

def greedySearch(startingBoard):

    # Heuristic, Board, Depth, Total Cost, Actions
    queue = [(manhattanDistance(startingBoard), startingBoard, 0, 0, [])]  
    explored = set()
    poppedNodes = 0
    expandedNodes = 0
    totalNodesGenerated = 0
    depth = -1
    finalFringeSize = 0

    while queue:
        queue.sort(key=firstIndex)

        #omit first item in the tuple
        _, board, depth, totalCost, steps = queue.pop(0)
        poppedNodes += 1
        explored.add(tuple(map(tuple, board)))

        if goalState(board):
            depth = depth
            return totalCost, poppedNodes, expandedNodes, totalNodesGenerated, depth, finalFringeSize, steps

        i, j = zeroTileCoordinates(board)

        for x, y, move in [(i, j - 1, "Right"), (i, j + 1, "Left"), (i - 1, j, "Down"), (i + 1, j, "Up")]:
            if 0 <= x < 3 and 0 <= y < 3:
                newBoard = [row[:] for row in board]
                newBoard[i][j], newBoard[x][y] = newBoard[x][y], newBoard[i][j]
                tileSwapped = board[x][y]  
                totalNodesGenerated += 1
                if tuple(map(tuple, newBoard)) not in explored:
                    nextStep = steps + [f"Move {tileSwapped} {move}"] 
                    heuristic = manhattanDistance(newBoard)
                    new_total_cost = totalCost + tileSwapped
                    queue.append((heuristic, newBoard, depth + 1, new_total_cost, nextStep))
                    expandedNodes += 1
                    finalFringeSize = len(queue)

    return -1, poppedNodes, expandedNodes, totalNodesGenerated, depth, finalFringeSize, []

def aStarSearch(startingBoard):

    totalCost=0
    def pop(queue):
        min_index = 0
        for i in range(1, len(queue)):
            if queue[i][0] < queue[min_index][0]:
                min_index = i
        return queue.pop(min_index)
    
             #step cost + heuristic cost
    queue = [(totalCost + manhattanDistance(startingBoard), 0, startingBoard, [])] 
    explored = set()
    poppedNodes = 0
    expandedNodes = 0
    totalNodesGenerated = 0
    finalFringeSize = 1
    depth = -1

    while queue:
        _, cost, board, steps = pop(queue)
        poppedNodes += 1
        explored.add(tuple(map(tuple, board)))

        if goalState(board):
            depth = len(steps)
            return cost, poppedNodes, expandedNodes, totalNodesGenerated, depth, finalFringeSize, steps

        i, j = zeroTileCoordinates(board)

        for x, y, move in [(i, j - 1, "Right"), (i, j + 1, "Left"), (i - 1, j, "Down"), (i + 1, j, "Up")]:
            if 0 <= x < 3 and 0 <= y < 3:
                newBoard = [row[:] for row in board]
                newBoard[i][j], newBoard[x][y] = newBoard[x][y], newBoard[i][j]
                tileSwapped = board[x][y] 
                totalNodesGenerated += 1
                if tuple(map(tuple, newBoard)) not in explored:
                    nextStep = steps + [f"Move {tileSwapped} {move}"] 

                    #TODO newCost not updating correctly
                    #why does it change when i use 'cost + tileSwapped' instead ??????
                    newCost = cost + 1
                    queue.append((newCost + manhattanDistance(newBoard), newCost, newBoard, nextStep))
                    
                    expandedNodes += 1
                    finalFringeSize = len(queue)

    return -1, poppedNodes, expandedNodes, totalNodesGenerated, depth, finalFringeSize, []

def depthFirstSearch(startingBoard):

    startingCost = 0
    statingDepth = 0
    startingPath = []
    stack = [(startingBoard, startingCost, statingDepth, startingPath)]

    explored = set()
    poppedNodes = 0
    expandedNodes = 0
    totalNodesGenerated = 0
    finalFringeSize = 0
    depth = -1

    while stack:
        
        board, cost, depth, steps = stack.pop()
        poppedNodes += 1
        
        #keep track of explored boards
        explored.add(tuple(map(tuple, board)))

        if goalState(board):
            depth = depth
            return cost, poppedNodes, expandedNodes, totalNodesGenerated, depth, finalFringeSize, steps

        i, j = zeroTileCoordinates(board)

        for x, y, move in [(i, j - 1, "Right"), (i, j + 1, "Left"), (i - 1, j, "Down"), (i + 1, j, "Up")]:
            if 0 <= x < 3 and 0 <= y < 3:
                newBoard = [list(row) for row in board]
                newBoard[i][j], newBoard[x][y] = newBoard[x][y], newBoard[i][j]
                tileSwapped = board[x][y]
                totalNodesGenerated += 1

                newState = tuple(tuple(row) for row in newBoard)
                if newState not in explored:
                    nextStep = steps + [f"Move {tileSwapped} {move}"]
                    stack.append((newBoard, cost + tileCost(board, newBoard), depth + 1, nextStep))
                    expandedNodes += 1
                    finalFringeSize = len(stack)

    return -1, poppedNodes, expandedNodes, totalNodesGenerated, depth, finalFringeSize, []

def depthLimitedSearch(startingBoard):

    limit=int(input("Enter Depth Limit: "))

    startingCost = 0
    statingDepth = 0
    startingPath = []
    stack = [(startingBoard, startingCost, statingDepth, startingPath)]

    explored = set()
    poppedNodes = 0
    expandedNodes = 0
    totalNodesGenerated = 0
    finalFringeSize = 0
    depth = -1

    while stack:

        board, cost, depth, steps = stack.pop()
        poppedNodes += 1

        explored.add(tuple(map(tuple, board)))

        #once iteration at the depth limit is reached, skip to the return value
        if depth > limit:
            continue  

        if goalState(board):
            depth = depth
            return cost, poppedNodes, expandedNodes, totalNodesGenerated, depth, finalFringeSize, steps

        i, j = zeroTileCoordinates(board)

        for x, y, action in [(i, j - 1, "Right"), (i, j + 1, "Left"), (i - 1, j, "Down"), (i + 1, j, "Up")]:
            if 0 <= x < 3 and 0 <= y < 3:
                newBoard = [list(row) for row in board]
                newBoard[i][j], newBoard[x][y] = newBoard[x][y], newBoard[i][j]
                tileSwapped = board[x][y]
                totalNodesGenerated += 1
                newState = tuple(tuple(row) for row in newBoard)

                if newState not in explored:
                    nextStep = steps + [f"Move {tileSwapped} {action}"]
                    stack.append((newBoard, cost + tileCost(board, newBoard), depth + 1, nextStep))
                    expandedNodes += 1
                    finalFringeSize = len(stack)

    return -1, poppedNodes, expandedNodes, totalNodesGenerated, depth, finalFringeSize, []

def iterativeDeepeningSearch(startingBoard):

    #user input for the lowest depth the algorithm is allowed to go
    max = int(input("Maximum Depth Allowed: "))

    for limit in range(max + 1):

        #superset of depth limited search algorithm
        result = depthLimitedSearch(startingBoard)

        # "-1" is the first item in the tuple, representing the sucess of the depth limites search algorithm
        # i.e "If a solution was found in this iteration, return the solution"
        if result[0] != -1:  
            return result
    
    return -1, 0, 0, 0, max, 0, []

################################
#"main" function starts here

#fringe size includes the goal node
#Make an array to hold the starting config
startFileArray = []

#command line format:
#expense_8_puzzle.py <start-file> <goal-file> <method> <dump-flag>
if len(sys.argv) != 4:
        print("Structure: python3 expense_8_puzzle.py <start-file> <goal-file> <method>")
        sys.exit(1)

startFile = sys.argv[1]
method = sys.argv[3]

#Copy the start file, exluding "END OF FILE", into an array
with open(startFile, "r") as startFile:
            for lines in startFile:
                lines = lines.strip()
                if lines != "END OF FILE":
                    #split the lines into the array
                    elements = lines.split()
                    
                    #Make sure all elements are type int
                    for element in elements:
                        fileElement = int(element)  

                        #push to list
                        startFileArray.append(fileElement)

#essentially return a 3x3 matrix representing the start state
startingBoard = [[startFileArray[0], startFileArray[1], startFileArray[2]], [startFileArray[3], startFileArray[4], startFileArray[5]], [startFileArray[6], startFileArray[7], startFileArray[8]]]

#print out needed values corresponding to each search algorithm
if method.lower() == "bfs":
        totalCost, poppedNodes, expandedNodes, totalNodesGenerated, depth, finalFringeSize, steps = breadthFirstSearch(startingBoard)
        
        if totalCost > 0:
            print("Nodes Popped:", poppedNodes)
            print("Nodes Expanded: ",expandedNodes)
            print("Nodes Generated:",totalNodesGenerated)
            print("Max Fringe Size:",finalFringeSize)
            print("Solution found at depth",depth, "with a cost of",totalCost)
            
            if steps:
                print("Steps:")
                for step in steps:
                    print(step)
        else:
            print("ERROR: State not found")

if method.lower() == "ucs":
        totalCost, poppedNodes, expandedNodes, totalNodesGenerated, depth, finalFringeSize, steps = uniformCostSearch(startingBoard)
        
        if totalCost != -1:
            print("Nodes PoppedNodes:", poppedNodes)
            print("Nodes Expanded: ",expandedNodes)
            print("Nodes Generated:",totalNodesGenerated)
            print("Max Fringe Size:",finalFringeSize)
            print("Solution found at depth",depth, "with a cost of",totalCost)
            
            if steps:
                print("Steps:")
                for step in steps:
                    print(step)
        else:
            print("ERROR: State not found")

if method.lower() == "grs":
        totalCost, poppedNodes, expandedNodes, totalNodesGenerated, depth, finalFringeSize, steps = greedySearch(startingBoard)
        
        if totalCost != -1:
            print("Nodes PoppedNodes:", poppedNodes)
            print("Nodes Expanded: ",expandedNodes)
            print("Nodes Generated:",totalNodesGenerated)
            print("Max Fringe Size:",finalFringeSize)
            print("Solution found at depth",depth, "with a cost of",totalCost)
            
            if steps:
                print("Steps:")
                for step in steps:
                    print(step)
        else:
            print("ERROR: State not found")

if method.lower() == "astar":
        totalCost, poppedNodes, expandedNodes, totalNodesGenerated, depth, finalFringeSize, steps = aStarSearch(startingBoard)
        
        if totalCost != -1:
            print("Nodes PoppedNodes:", poppedNodes)
            print("Nodes Expanded: ",expandedNodes)
            print("Nodes Generated:",totalNodesGenerated)
            print("Max Fringe Size:",finalFringeSize)
            print("Solution found at depth",depth, "with a cost of",totalCost)
            
            if steps:
                print("Steps:")
                for step in steps:
                    print(step)
        else:
            print("ERROR: State not found")

if method.lower() == "dfs":
        totalCost, poppedNodes, expandedNodes, totalNodesGenerated, depth, finalFringeSize, steps = depthFirstSearch(startingBoard)
        
        if totalCost != -1:
            print("Nodes PoppedNodes:", poppedNodes)
            print("Nodes Expanded: ",expandedNodes)
            print("Nodes Generated:",totalNodesGenerated)
            print("Max Fringe Size:",finalFringeSize)
            print("Solution found at depth",depth, "with a cost of",totalCost)
            
            if steps:
                print("Steps:")
                for step in steps:
                    print(step)
        else:
            print("ERROR: State not found")

if method.lower() == "dls":
        totalCost, poppedNodes, expandedNodes, totalNodesGenerated, depth, finalFringeSize, steps = depthLimitedSearch(startingBoard)
        
        if totalCost != -1:
            print("Nodes PoppedNodes:", poppedNodes)
            print("Nodes Expanded: ",expandedNodes)
            print("Nodes Generated:",totalNodesGenerated)
            print("Max Fringe Size:",finalFringeSize)
            print("Solution found at depth",depth, "with a cost of",totalCost)

        if steps:
                print("Steps:")
                for step in steps:
                    print(step)
            
        else:
            print("ERROR: No solution found at given depth limit")

#TODO finish
if method.lower() == "ids":
        """totalCost, poppedNodes, expandedNodes, totalNodesGenerated, depth, finalFringeSize, steps = iterativeDeepeningSearch(startingBoard)
        
        if totalCost != -1:
            print("Nodes PoppedNodes:", poppedNodes)
            print("Nodes Expanded: ",expandedNodes)
            print("Nodes Generated:",totalNodesGenerated)
            print("Max Fringe Size:",finalFringeSize)
            print("Solution found at depth",depth, "with a cost of",totalCost)

        if steps:
                print("Steps:")
                for step in steps:
                    print(step)
            
        else:
            print("ERROR: No solution found before maximum the depth was reached")"""