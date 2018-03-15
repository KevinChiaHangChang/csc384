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
        # IMPLEMENTATION 1
        # get information about current state
        currPos = currentGameState.getPacmanPosition()
        currFood = currentGameState.getFood()

        score = 0.0

        # check if next state brings Pacman closer to ghosts
        # find current state minimum distance to ghosts
        currGhostDist = float('inf')
        for eachGhost in currentGameState.getGhostStates():
          tmpDist = manhattanDistance(currPos,eachGhost.getPosition())
          currGhostDist = min(currGhostDist,tmpDist)
        # find next state minimum distance to ghosts
        newGhostDist = float('inf')
        for eachGhost in newGhostStates:
          tmpDist = manhattanDistance(newPos,eachGhost.getPosition())
          newGhostDist = min(newGhostDist,tmpDist)
        # if newGhostDist > currGhostDist:
        #   score += 2.0/newGhostDist
        print "Current ghost distance: " + str(currGhostDist) + " New ghost distance: " + str(newGhostDist)
        if newGhostDist == 0.0:
          score -= 10.0
        elif newGhostDist < currGhostDist:
          score -= 2.0/newGhostDist
        elif newGhostDist > currGhostDist:
          score += 0.5/currGhostDist
        print "Score: " + str(score)
        
        # check if next state brings Pacman closer to food
        if len(newFood.asList()) < len(currFood.asList()):
          score += 5.0
        # print "Score: " + str(score)
        # find current state minimum distance to food
        currFoodDist = float('inf')
        for eachFood in currFood.asList():
          tmpDist = manhattanDistance(currPos,eachFood)
          currFoodDist = min(currFoodDist,tmpDist)
        # find next state minimum distance to food
        newFoodDist = float('inf')
        for eachFood in newFood.asList():
          tmpDist = manhattanDistance(newPos,eachFood)
          newFoodDist = min(newFoodDist,tmpDist)
        if newFoodDist < currFoodDist:
          score += 3.0/currFoodDist
        # print "Score: " + str(score)
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
        # NOTE: leaves could either be terminal or non-terminal nodes, since a depth bound is enforced
        # NOTE: terminal node = node where gameState.isWin() or gameState.isLose() is true

        def getMax(gameState, currDepth):
          # determine if terminal node
          if gameState.isWin() or gameState.isLose() or currDepth == 0:
            return self.evaluationFunction(gameState)
          maxScore = -(float('inf'))
          actions = gameState.getLegalActions(0)
          # get max score out of all successor states generated by legal actions
          for each_action in actions:
            successorState = gameState.generateSuccessor(0,each_action)
            maxScore = max(maxScore, getMin(successorState,1,currDepth))
          return maxScore
        
        def getMin(gameState, agentIndex, currDepth):
          # determine if terminal node
          if gameState.isWin() or gameState.isLose() or currDepth == 0:
            return self.evaluationFunction(gameState)
          minScore = float('inf')
          actions = gameState.getLegalActions(agentIndex)
          # if reach last agent index, need to decrement depth by 1
          if agentIndex+1 == gameState.getNumAgents():
            # get min score out of all successor states generated by legal actions
            for each_action in actions:
              successorState = gameState.generateSuccessor(agentIndex,each_action)
              minScore = min(minScore, getMax(successorState,currDepth-1))
          else:
            for each_action in actions:
              # get min score out of all successor states generated by legal actions
              successorState = gameState.generateSuccessor(agentIndex,each_action)
              minScore = min(minScore, getMin(successorState,agentIndex+1,currDepth))
          return minScore

        actions = gameState.getLegalActions(0)
        optimal_action = Directions.STOP
        maxScore = -(float('inf'))
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

        def getMax(gameState, currDepth, alpha, beta):
          # determine if terminal node
          if gameState.isWin() or gameState.isLose() or currDepth == 0:
            return self.evaluationFunction(gameState)
          maxScore = -(float("inf"))
          actions = gameState.getLegalActions(0)
          for each_action in actions:
            successorState = gameState.generateSuccessor(0,each_action)
            maxScore = max(maxScore, getMin(successorState,1,currDepth,alpha,beta))
            # update alpha if necessary
            alpha = max(maxScore,alpha)
            # pruning occurs
            if beta <= alpha:
              return maxScore
          return maxScore
        
        def getMin(gameState, agentIndex, currDepth, alpha, beta):
          # determine if terminal node
          if gameState.isWin() or gameState.isLose() or currDepth == 0:
            return self.evaluationFunction(gameState)
          minScore = float("inf")
          actions = gameState.getLegalActions(agentIndex)
          if agentIndex+1 == gameState.getNumAgents():
            for each_action in actions:
              successorState = gameState.generateSuccessor(agentIndex,each_action)
              minScore = min(minScore, getMax(successorState,currDepth-1,alpha,beta))
              # update beta if necessary
              beta = min(minScore,beta)
              # pruning occurs
              if beta <= alpha:
                return minScore
          else:
            for each_action in actions:
              successorState = gameState.generateSuccessor(agentIndex,each_action)
              minScore = min(minScore, getMin(successorState,agentIndex+1,currDepth,alpha,beta))
              # update beta if necessary
              beta = min(minScore,beta)
              # pruning occurs
              if beta <= alpha:
                return minScore
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
          # update alpha if necessary
          alpha = max(maxScore,alpha)
          # pruning occurs
          if beta <= alpha:
            return each_action
          # no pruning, need to check if current score is higher than previous score
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

