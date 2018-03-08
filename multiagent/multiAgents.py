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
import sys

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
        # print "New position:%s" % (newPos,)
        # IMPLEMENTION 1
        # take reciprocal of distance to food, and (if scared ghosts) distance (or reciprocal) to ghosts
        # initialize score
        # score = 0
        # # check if successor state is win state
        # if successorGameState.isWin():
        #   return sys.maxint

        # # find minimum Manhattan distance to food
        # nearestFoodDist = sys.maxint
        # for eachFood in newFood.asList():
        #   tmpDist = manhattanDistance(newPos,eachFood)
        #   if tmpDist < nearestFoodDist:
        #     nearestFoodDist = tmpDist
        # # take reciprocal
        # score += (1/nearestFoodDist)*10
        # # print "Minimum distance to food: " + str(nearestFoodDist)

        # # find change in amount of food
        # if successorGameState.getNumFood() < currentGameState.getNumFood():
        #   score += 100
        
        # # find minimum Manhattan distance to ghosts
        # nearestGhostDist = sys.maxint
        # for eachGhost in newGhostStates:
        #   tmpDist = manhattanDistance(newPos,eachGhost.getPosition())
        #   if not nearestGhostDist or tmpDist < nearestGhostDist:
        #     nearestGhostDist = tmpDist
        # # print "Minimum distance to ghost: " + str(nearestGhostDist)
        # # be careful about division by zero
        # if nearestGhostDist == 0:
        #   score -= (sys.maxint-100)
        # else:
        #   # take reciprocal
        #   score -= (1/nearestGhostDist)*10

        # # penalize STOP action
        # if action == Directions.STOP:
        #   score -= 5

        # # find minimum Manhattan distance to capsules
        # newCapsules = successorGameState.getCapsules()
        # nearestCapsuleDist = sys.maxint
        # for eachCapsule in newCapsules:
        #   tmpDist = manhattanDistance(newPos,eachCapsule)
        #   if tmpDist < nearestCapsuleDist:
        #     nearestCapsuleDist = tmpDist
        # # take reciprocal
        # score -= (1/nearestCapsuleDist)*5

        # # find change in amount of capsules
        # if len(newCapsules) < len(currentGameState.getCapsules()):
        #   score += 50

        # return score

        # Implementation 2
        # find minimum distance to ghost
        nearestGhostDist = sys.maxint
        for eachGhost in newGhostStates:
          tmpDist = manhattanDistance(newPos,eachGhost.getPosition())
          if tmpDist < nearestGhostDist:
            nearestGhostDist = tmpDist
        # find average distance to food
        foodDist = []
        for eachFood in newFood.asList():
          tmpDist = manhattanDistance(newPos,eachFood)
          foodDist.append(tmpDist)
        avgFoodDist = sum(foodDist)/len(foodDist) if foodDist else 1
        if avgFoodDist == 0:
          avgFoodDist = 1
        # find surrounding food
        nearbyFood = 0
        m = len(list(newFood))
        m = len(list(newFood[0]))
        for x in range(newPos[0]-2,newPos[0]+3):
          for y in range(newPos[1]-2,newPos[1]+3):
            if (x >= 0 and x < m) and (y >= 0 and y < m) and newFood[x][y]:
              nearbyFood += 1
        score = 4.0/nearestGhostDist + 5.0/avgFoodDist + nearbyFood + successorGameState.getScore()


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
        # util.raiseNotDefined()
        # NOTE: leaves could either be terminal or non-terminal nodes, since a depth bound is enforced
        # NOTE: terminal node = node where gameState.isWin() or gameState.isLose() is true
        # DFS Implementation
        # def DFMinimax(gameState, agentIndex, currDepth):
        #   # determine if terminal node
        #   if gameState.isWin() or gameState.isLose() or currDepth == 0:
        #     # print "Agent: " + str(agentIndex) + " Depth: " + str(currDepth) + " Value: " + str(self.evaluationFunction(gameState))
        #     return self.evaluationFunction(gameState)

        #   # apply legal actions to get successor states
        #   actions = gameState.getLegalActions(agentIndex)
        #   # determine if no more legal actions
        #   if not actions:
        #     return self.evaluationFunction(gameState)

        #   # determine if Pacman or ghost
        #   if agentIndex == 0:
        #     maxScore = -sys.maxint-1
        #     # Pacman, want maximum score among all successor states
        #     for each_action in actions:
        #       successorState = gameState.generateSuccessor(agentIndex,each_action)
        #       maxScore = max(maxScore,DFMinimax(successorState,agentIndex+1,currDepth))
        #     return maxScore
        #   else:
        #     # ghost, want minimum score among all successor states
        #     minScore = sys.maxint
        #     print "Agent index: " + str(agentIndex)
        #     if agentIndex+1 == gameState.getNumAgents():
        #       for each_action in actions:
        #         successorState = gameState.generateSuccessor(agentIndex,each_action)
        #         minScore = min(minScore,DFMinimax(successorState,0,currDepth-1))
        #     else:
        #     # ghost, want minimum score among all successor states
        #       for each_action in actions:
        #         successorState = gameState.generateSuccessor(agentIndex,each_action)
        #         minScore = min(minScore,DFMinimax(successorState,agentIndex+1,currDepth))
        #     return minScore

        # actions = gameState.getLegalActions(0)
        # optimal_action = Directions.STOP
        # maxScore = -sys.maxint-1
        # for each_action in actions:
        #   successorState = gameState.generateSuccessor(0,each_action)
        #   prevScore = maxScore
        #   maxScore = max(maxScore, DFMinimax(successorState,1,self.depth))
        #   if maxScore < prevScore:
        #     optimal_action = each_action
        # return optimal_action

        def getMax(gameState, currDepth):
          # determine if terminal node
          if gameState.isWin() or gameState.isLose() or currDepth == 0:
            return self.evaluationFunction(gameState)
          maxScore = -sys.maxint-1
          actions = gameState.getLegalActions(0)
          for each_action in actions:
            successorState = gameState.generateSuccessor(0,each_action)
            maxScore = max(maxScore, getMin(successorState,1,currDepth))
          return maxScore
        
        def getMin(gameState, agentIndex, currDepth):
          # determine if terminal node
          if gameState.isWin() or gameState.isLose() or currDepth == 0:
            return self.evaluationFunction(gameState)
          minScore = sys.maxint
          actions = gameState.getLegalActions(agentIndex)
          if agentIndex+1 == gameState.getNumAgents():
            for each_action in actions:
              successorState = gameState.generateSuccessor(agentIndex,each_action)
              minScore = min(minScore, getMax(successorState,currDepth-1))
          else:
            for each_action in actions:
              successorState = gameState.generateSuccessor(agentIndex,each_action)
              minScore = min(minScore, getMin(successorState,agentIndex+1,currDepth))
          return minScore

        actions = gameState.getLegalActions(0)
        optimal_action = Directions.STOP
        maxScore = -sys.maxint-1
        for each_action in actions:
            successorState = gameState.generateSuccessor(0,each_action)
            prevScore = maxScore
            maxScore = max(maxScore, getMin(successorState,1,self.depth))
            if maxScore > prevScore:
                optimal_action = each_action
        return optimal_action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        # util.raiseNotDefined()
        # AlphaBeta Implementation
        # def AlphaBeta(gameState, agentIndex, alpha, beta, currDepth):
        #   if gameState.isWin() or gameState.isLose() or currDepth == 0:
        #     return self.evaluationFunction(gameState)
        
        #   actions = gameState.getLegalActions(agentIndex)
        #   if not actions:
        #     return self.evaluationFunction(gameState)
          
        #   # determine if Pacman or ghost
        #   if agentIndex == 0:
        #     # Pacman
        #     for each_action in actions:
        #       if each_action == Directions.STOP:
        #         continue
        #       successorState = gameState.generateSuccessor(agentIndex,each_action)
        #       alpha = max(alpha,AlphaBeta(successorState,agentIndex+1,alpha,beta,currDepth))
        #       if beta <= alpha:
        #         break
        #     return alpha
        #   else:
        #     # ghost
        #     for each_action in actions:
        #       if each_action == Directions.STOP:
        #         continue
        #       nextAgentIndex = agentIndex+1
        #       nextDepth = currDepth
        #       if nextAgentIndex == gameState.getNumAgents():
        #         nextAgentIndex = 0
        #         nextDepth = currDepth-1
        #       successorState = gameState.generateSuccessor(agentIndex,each_action)
        #       beta = min(beta,AlphaBeta(successorState,nextAgentIndex,alpha,beta,nextDepth))
        #       if beta <= alpha:
        #         break
        #     return beta

        def getMax(gameState, currDepth, alpha, beta):
          # determine if terminal node
          if gameState.isWin() or gameState.isLose() or currDepth == 0:
            # print "Depth:" + str(currDepth)
            return self.evaluationFunction(gameState)
          maxScore = -(float("inf"))
          actions = gameState.getLegalActions(0)
          for each_action in actions:
            successorState = gameState.generateSuccessor(0,each_action)
            maxScore = max(maxScore, getMin(successorState,1,currDepth,alpha,beta))
            if beta <= maxScore:
              return maxScore
            alpha = max(maxScore,alpha)
          return maxScore
        
        def getMin(gameState, agentIndex, currDepth, alpha, beta):
          # determine if terminal node
          if gameState.isWin() or gameState.isLose() or currDepth == 0:
            # print "Depth:" + str(currDepth)
            return self.evaluationFunction(gameState)
          minScore = float("inf")
          actions = gameState.getLegalActions(agentIndex)
          if agentIndex+1 == gameState.getNumAgents():
            for each_action in actions:
              successorState = gameState.generateSuccessor(agentIndex,each_action)
              minScore = min(minScore, getMax(successorState,currDepth-1,alpha,beta))
              if minScore <= alpha:
                # print "Pruned"
                return minScore
              beta = min(minScore,beta)
          else:
            for each_action in actions:
              successorState = gameState.generateSuccessor(agentIndex,each_action)
              minScore = min(minScore, getMin(successorState,agentIndex+1,currDepth,alpha,beta))
              if minScore <= alpha:
                # print "Pruned"
                return minScore
              beta = min(minScore,beta)
          return minScore

        actions = gameState.getLegalActions(0)
        alpha = -(float("inf"))
        beta = float("inf")
        maxScore = -(float("inf"))
        optimal_action = Directions.STOP
        for each_action in actions:
          successorState = gameState.generateSuccessor(0,each_action)
          prevScore = maxScore
          maxScore = max(maxScore,getMin(successorState,1,self.depth,alpha,beta))
          if beta <= maxScore:
            # print("Pruned")
            return each_action
          alpha = max(maxScore,alpha)
          if maxScore > prevScore:
            optimal_action = each_action
        return optimal_action


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
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

