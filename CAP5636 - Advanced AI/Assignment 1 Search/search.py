# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    # from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

class State:
    def __init__(self, coord, direction, cost):
        self.coord = coord
        self.direction = direction
        self.cost = cost

    def get_tuple(self):
        return [self.coord, self.direction, self.cost]


coordinate = 0
direction = 1
cost = 2

def treeSearch(problem, strategy, get_cur_coord = lambda state: state):
    # initializing the strategy structure with tuple of [(x, y), Direction, Cost]
    paths = strategy()
    strat = strategy()
    strat.push(problem.getStartState())
    visited = []
    path = []
    while not strat.isEmpty():
        cur_coord = strat.pop()
        if cur_coord not in visited:
            visited.append(cur_coord)
            if problem.isGoalState(cur_coord):
                return path
            for coord in problem.getSuccessors(cur_coord):
                # if isinstance(coord[0][0], tuple):
                #     coord = coord[0]
                strat.push(coord[coordinate])
                paths.push(path + [coord[direction]])
        if paths.isEmpty():
            return []
        path = paths.pop()
    return []



def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    return treeSearch(problem, util.Stack)

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    return treeSearch(problem, util.Queue)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    paths = util.PriorityQueue()
    strat = util.PriorityQueue()
    strat.push(problem.getStartState(), 0)
    visited = set()
    path = []
    while not strat.isEmpty():
        cur_coord = strat.pop()
        if cur_coord not in visited:
            visited.add(cur_coord)
            if problem.isGoalState(cur_coord):
                return path
            for coord, dir, cost in problem.getSuccessors(cur_coord):
                n_cost = problem.getCostOfActions(path + [dir])
                strat.push(coord, n_cost)
                paths.push(path + [dir], n_cost)
        if paths.isEmpty():
            return []
        path = paths.pop()
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

# def is_custom_state(state):
#     return len(state) > 1 and isinstance(state[1], set)
#
# def convert_state_for_map(state):
#     if is_custom_state(state):
#         return state[0]
#     return state
#
# def add_coords_to_map(state, problem, total_path):
#     if is_custom_state(state):
#         problem.add_coords_to_map(state, problem, total_path)
#     return state

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    # python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
    "*** YOUR CODE HERE ***"

    fringe = util.PriorityQueue()
    fringe.push(problem.getStartState(), 0)
    came_from = util.PriorityQueue()
    visited = []
    total_path = []

    curr_state = fringe.pop()
    while not problem.isGoalState(curr_state):
        if curr_state not in visited:
            visited.append(curr_state)
            for coord, direction, cost in problem.getSuccessors(curr_state):
                if coord not in visited:
                    temp_path = total_path + [direction]
                    cost_so_far = problem.getCostOfActions(temp_path) + heuristic(coord, problem)
                    fringe.push(coord, cost_so_far)
                    came_from.push(temp_path, cost_so_far)
        total_path = came_from.pop()
        curr_state = fringe.pop()

    return total_path

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
