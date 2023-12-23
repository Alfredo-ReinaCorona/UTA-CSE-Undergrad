from random import *
import csv
import numpy as np

#Set up classes to represent an active agent, potential moves, and the current state within the environment for ease of use
class Agent:
    numMoves = 0

    def __init__(self, state):
        self.state, self.latestLocation = state, state.start

    def reward(self):
        return self.state.reward(self.latestLocation)
    
    def stateInfo(self):
        return self.latestLocation

    def move(self, move):
        self.latestLocation = self.state.move(self.latestLocation, move)
        Agent.numMoves += 1

class Moves:
    direction = ['^', '<', 'v', '>']

    def __init__(self, direction_index: int):
        self.direction = direction_index % 4

    def test(self, state):
        Ty, Tx = (1, 0) if self.direction == 0 else (-1, 0) if self.direction == 2 else (0, -1) if self.direction == 1 else (0, 1)
        return state[0] + Ty, state[1] + Tx

    def left(self):
        return Moves((self.direction + 1) % 4)

    def right(self):
        return Moves((self.direction - 1) % 4)

    @staticmethod #returns all possible moves
    def moves():
        return [Moves(direction_index) for direction_index in range(4)]
    
    #magic methods
    def __eq__(self, other):# compares if moves are equal
        return isinstance(other, Moves) and self.direction == other.direction

    def __hash__(self):# gets the hash value of an move
        return hash(self.direction)

    def __str__(self):# string representation of an object
        return Moves.direction[self.direction]

class State:
    def __init__(self, environmentFile, ntr):
        self.getFile(environmentFile, ntr)

    def getFile(self, environmentFile, ntr):
        self.obstacles = []
        self.goal = {}
        self.start = None

        with open(environmentFile, 'r') as filestream:
            rows = [row for row in csv.reader(filestream)]
            self.num_rows, self.num_cols = len(rows), len(rows[0])

            for y, row in enumerate(rows):
                for x, val in enumerate(row):
                    pos = (self.num_rows - y, x + 1)
                    val = val.strip()

                    if val == 'X':
                        self.obstacles.append(pos)
                    elif val == 'I':
                        self.start = pos
                    elif val != '.':
                        self.goal[pos] = float(val)

        self.ntr = ntr

    def move(self, state, move: Moves):
        move = move.left() if random() < 0.15 else move.right() if random() > 0.9 else move

        y, x = move.test(state)
        if (y, x) in self.obstacles or not (0 < y <= self.num_rows) or not (0 < x <= self.num_cols):
            return state
        return y, x

    def reward(self, state):
        if state in self.obstacles:
            return 0

        return self.goal.get(state, self.ntr)

def Q_Learning_Update(initialState, initialReward, s, r, a, Q, N, gamma, state: State):
    if initialState in state.goal:
        Q[(initialState, None)] = initialReward

    if s is not None:
        N[(s, a)] = N.get((s, a), 0) + 1
        #For the η function, use η(N) = 20/(19+N). 
        c = 20 / (19 + N[(s, a)])

        Q[(s, a)] = (1 - c) * Q.get((s, a), 0) + c * (r + gamma * max(Q.get((initialState, move), 0) for move in Moves.moves() + [None]))

def f(u, n, ne):
    return 1 if n < ne else u

def AgentModel_Q_Learning(environment_file, ntr, gamma, number_of_moves, Ne):
    state = State(environment_file, ntr)
    Q, N = {}, {}

    while Agent.numMoves < number_of_moves:
        s, r, a = None, None, None
        agent = Agent(state)

        while Agent.numMoves < number_of_moves:
            initialState = agent.stateInfo()
            initialReward = agent.reward()
            Q_Learning_Update(initialState, initialReward, s, r, a, Q, N, gamma, state)

            if initialState in state.goal:
                break

            f_vals = {move: f(Q.get((initialState, move), 0), N.get((initialState, move), 0), Ne) for move in Moves.moves()}
            ties = [key for key, value in f_vals.items() if value == max(f_vals.values())]
            shuffle(ties)
            a = ties[0]

            agent.move(a)
            s, r = initialState, initialReward

    # Outputting the results
    utilities = np.zeros((state.num_rows, state.num_cols))
    policy = np.empty((state.num_rows, state.num_cols), dtype=str)

    for i in range(state.num_rows):
        for j in range(state.num_cols):
            pos = (i + 1, j + 1)
            if pos in state.goal:
                policy[i, j], utilities[i, j] = 'o', state.goal[pos]
            elif pos in state.obstacles:
                policy[i, j], utilities[i, j] = 'x', 0
            else:
                policy[i, j] = str(Moves(np.argmax([Q.get((pos, move), 0) for move in Moves.moves()])))
                utilities[i, j] = max(Q.get((pos, move), 0) for move in Moves.moves() + [None])

    print('utilities:')
    for row in np.flip(utilities, axis=0):
        print(' '.join(f'{val:6.3f}' for val in row))

    print('\n' + 'policy:')
    for row in np.flip(policy, axis=0):
        print(' '.join(f'{val:6s}' for val in row))

