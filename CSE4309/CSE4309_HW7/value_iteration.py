import pandas as pd

def returnUtility(file, ntr):
    df = pd.read_csv(file, header=None)
    Table = [[(0, False, 0, False) for _ in range(len(df.columns)+2)]]

    for i in range(len(df)):
        row = [(0, False, 0, False)]
        for j in range(len(df.columns)):
            value = df.iloc[i][j]
            if value == 'X':
                row.append((0, False, 0, False))
            elif value == '.':
                row.append((0, True, ntr, False))
            else:
                row.append((0, True, float(value), True))
        row.append((0, False, 0, False))
        Table.append(row)

    Table.append(Table[0])
    return Table


def moves(U, i, j):

    #Max utility when going up
    maxUp = 0.8 * U[i-1][j][0] if U[i-1][j][1] else 0.8 * U[i][j][0]
    maxUp += 0.1 * U[i][j-1][0] if U[i][j-1][1] else 0.1 * U[i][j][0]
    maxUp += 0.1 * U[i][j+1][0] if U[i][j+1][1] else 0.1 * U[i][j][0]

    #Max utility when going down
    maxDown = 0.8 * U[i+1][j][0] if U[i+1][j][1] else 0.8 * U[i][j][0]
    maxDown += 0.1 * U[i][j-1][0] if U[i][j-1][1] else 0.1 * U[i][j][0]
    maxDown += 0.1 * U[i][j+1][0] if U[i][j+1][1] else 0.1 * U[i][j][0]

    #Max utility when going left
    maxLeft = 0.8 * U[i][j-1][0] if U[i][j-1][1] else 0.8 * U[i][j][0]
    maxLeft += 0.1 * U[i-1][j][0] if U[i-1][j][1] else 0.1 * U[i][j][0]
    maxLeft += 0.1 * U[i+1][j][0] if U[i+1][j][1] else 0.1 * U[i][j][0]

    #Max utility when going right
    maxRight = 0.8 * U[i][j+1][0] if U[i][j+1][1] else 0.8 * U[i][j][0]
    maxRight += 0.1 * U[i-1][j][0] if U[i-1][j][1] else 0.1 * U[i][j][0]
    maxRight += 0.1 * U[i+1][j][0] if U[i+1][j][1] else 0.1 * U[i][j][0]

    return maxUp, maxDown, maxLeft, maxRight

# From the slides
def valueIterationFunction(data_file, ntr, gamma, K):
    U_copy = returnUtility(data_file, ntr)
    policy = [['' for _ in range(len(U_copy[0]))] for _ in range(len(U_copy))]

    for _ in range(K):
        U = [[tuple(cell) for cell in row] for row in U_copy]

        #Where i and j get initialized for the moves
        for i in range(1, len(U_copy) - 1):
            for j in range(1, len(U_copy[i]) - 1):
                if U_copy[i][j][3] or not U_copy[i][j][1]:
                    U_copy[i][j] = (U_copy[i][j][2], U_copy[i][j][1], U_copy[i][j][2], U_copy[i][j][3])
                else:
                    maxUp, maxDown, maxLeft, maxRight = moves(U,i,j)
                    maxAction = max(moves(U, i, j))
                    U_copy[i][j] = (U_copy[i][j][2] + gamma * maxAction, U_copy[i][j][1], U_copy[i][j][2], U_copy[i][j][3])

                    # Determine policy
                    actions = [maxUp, maxDown, maxLeft, maxRight]
                    directions = ['^', 'v', '<', '>']
                    policy[i][j] = directions[actions.index(maxAction)]

    return U_copy, policy

# Function call for the main python file
def value_iteration(data_file, ntr, gamma, K):
    
    U, policy = valueIterationFunction(data_file, ntr, gamma, K)

    # Print the utilities
    for i in range(1, len(U)-1, 1):
        print('{:6.3f}'.format(U[i][1][0]), end="")
        for j in range(2, len(U[i])-1, 1):
            print(',{:6.3f}'.format(U[i][j][0]), end="")
        print()
    print()

    # Print the policies
    for i in range(1, len(policy) - 1):
        for j in range(1, len(policy[i]) - 1):
            if U[i][j][0] == 1:
                print('o', end="")
            elif U[i][j][0] == -1:
                print('o', end="")
            elif U[i][j][0] == 0:
                print('X', end="")
            else:
                print('{}'.format(policy[i][j]), end="")
            if j < len(policy[i]) - 2:
                print(',', end="")
        print()
