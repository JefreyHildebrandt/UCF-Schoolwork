# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        currentFood = currentGameState.getFood()
        currentGhostStates = currentGameState.getGhostStates()
        closest_food = 0 if currentFood[newPos[0]][newPos[1]] == True else float("inf")
        if closest_food > 0:
            for i, food_row in enumerate(newFood):
                for j, food in enumerate(food_row):
                    if food:
                        closest_food = min(closest_food, manhattanDistance(newPos, (i, j)))

        closest_ghost = float("inf")
        for ghost in currentGhostStates:
            closest_ghost = min(closest_ghost, manhattanDistance(newPos, ghost.configuration.getPosition()))

        total_spaces = currentFood.height * currentFood.width

        if closest_ghost < 2:
            closest_ghost = total_spaces
        else:
            closest_ghost = 0

        score = (total_spaces - closest_food) - closest_ghost
        # util.manhattanDistance()
        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        all_actions = dict()

        for action in gameState.getLegalActions(0):
            cur_state = gameState.generateSuccessor(0, action)
            all_actions[action] = self.minimax(cur_state, self.depth, 1)

        max_value = max(all_actions.values())  # maximum value
        max_keys = [k for k, v in all_actions.items() if v == max_value]
        return max_keys[0]

    def minimax(self, node, depth, maximizing_player):
        if depth == 0 or node.isWin() or node.isLose():
            return self.evaluationFunction(node)
        elif maximizing_player == 0:
            value = float("-inf")
            for action in node.getLegalActions(maximizing_player):
                value = max(value, self.minimax(node.generateSuccessor(maximizing_player, action), depth, maximizing_player + 1))
            return value
        else:
            value = float("inf")
            for action in node.getLegalActions(maximizing_player):
                if maximizing_player == node.getNumAgents() - 1:
                    value = min(value, self.minimax(node.generateSuccessor(maximizing_player, action), depth - 1, 0))
                else:
                    value = min(value, self.minimax(node.generateSuccessor(maximizing_player, action), depth, maximizing_player + 1))
            return value

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        all_actions = dict()
        alpha = float("-inf")
        beta = float("inf")

        for action in gameState.getLegalActions(0):
            cur_state = gameState.generateSuccessor(0, action)
            all_actions[action] = self.minimax(cur_state, self.depth, alpha, beta, 1)
            alpha = max(max(all_actions.values()), alpha)
        max_value = max(all_actions.values())  # maximum value
        max_keys = [k for k, v in all_actions.items() if v == max_value]
        return max_keys[0]

    def minimax(self, node, depth, alpha, beta, maximizing_player):
        if depth == 0 or node.isWin() or node.isLose():
            return self.evaluationFunction(node)
        elif maximizing_player == 0:
            value = float("-inf")
            for action in node.getLegalActions(maximizing_player):
                value = max(value, self.minimax(node.generateSuccessor(maximizing_player, action), depth, alpha, beta, maximizing_player + 1))
                if value > beta:
                    break
                alpha = max(alpha, value)
            return value
        else:
            value = float("inf")
            for action in node.getLegalActions(maximizing_player):
                if maximizing_player == node.getNumAgents() - 1:
                    value = min(value, self.minimax(node.generateSuccessor(maximizing_player, action), depth - 1, alpha, beta, 0))
                else:
                    value = min(value, self.minimax(node.generateSuccessor(maximizing_player, action), depth, alpha, beta, maximizing_player + 1))
                if value < alpha:
                    break
                beta = min(beta, value)
            return value

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        all_actions = dict()

        for action in gameState.getLegalActions(0):
            cur_state = gameState.generateSuccessor(0, action)
            all_actions[action] = self.expectMiniMax(cur_state, self.depth, 1)

        max_value = max(all_actions.values())  # maximum value
        max_keys = [k for k, v in all_actions.items() if v == max_value]
        return max_keys[0]

    def expectMiniMax(self, node, depth, maximizing_player):
        if depth == 0 or node.isWin() or node.isLose():
            return self.evaluationFunction(node)
        elif maximizing_player == 0:
            value = float("-inf")
            for action in node.getLegalActions(maximizing_player):
                value = max(value, self.expectMiniMax(node.generateSuccessor(maximizing_player, action), depth, maximizing_player + 1))
            return value
        else:
            value = 0
            for action in node.getLegalActions(maximizing_player):
                if maximizing_player == node.getNumAgents() - 1:
                    value += self.expectMiniMax(node.generateSuccessor(maximizing_player, action), depth - 1, 0)
                else:
                    value += self.expectMiniMax(node.generateSuccessor(maximizing_player, action), depth, maximizing_player + 1)
            return value


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: Always go to the closest food with the furthest away ghost. Always go to a capsule if nearby
    """

    "*** YOUR CODE HERE ***"
    if currentGameState.isWin():
        return float("inf")
    if currentGameState.isLose():
        return float("-inf")

    currentFood = currentGameState.getFood()
    currentGhostStates = currentGameState.getGhostStates()
    currentPos = currentGameState.getPacmanPosition()
    currentCap = currentGameState.getCapsules()
    total_spaces = currentFood.height * currentFood.width
    closest_food = 0 if currentGameState.hasFood(currentPos[0], currentPos[1]) == True else float("inf")
    if closest_food > 0:
        for i, food_row in enumerate(currentFood):
            for j, food in enumerate(food_row):
                if food:
                    closest_food = min(closest_food, manhattanDistance(currentPos, (i, j)))

    closest_ghost = float("inf")
    for ghost in currentGhostStates:
        closest_ghost = min(closest_ghost, manhattanDistance(currentPos, ghost.configuration.getPosition()))

    closest_capsule = float("inf")
    for cap in currentCap:
        closest_capsule = min(closest_capsule, manhattanDistance(currentPos, cap))

    if closest_ghost < 2:
        closest_ghost = total_spaces
    else:
        closest_ghost = 0

    food_or_capsule = min(closest_food, closest_capsule)

    # random is needed so pacman won't just sit there if two spaces are equal
    score = (total_spaces - food_or_capsule) - closest_ghost + random.choice([0, 1]) + (total_spaces*total_spaces)/(len(currentCap) + 1)

    return score + scoreEvaluationFunction(currentGameState)


# Abbreviation
better = betterEvaluationFunction

