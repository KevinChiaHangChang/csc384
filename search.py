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
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

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
    #print "Start:", problem.getStartState()
    #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    #print "Start's successors:", problem.getSuccessors(problem.getStartState())

    #Based on pseudocode
    #Initialize action list
    no_action = []
    goal_action = []
    #Get start state    
    start = problem.getStartState()
    start_path = []
    start_path.append(start)
    #Initialize frontier
    frontier = util.Stack()
    #Frontier entries wil be in the form of (path, action list, cost)
    frontier.push((start_path,no_action,0))

    while not frontier.isEmpty():
        #Remove (path, action list, cost) from frontier
        path, action, cost = frontier.pop()
        if problem.isGoalState(path[-1]):
            return action
        #Always expand
        #Get successors    
        successors = problem.getSuccessors(path[-1])
        #print "Successors:",successors
        for each_node, each_action, each_cost in successors:
            #Path checking
            if each_node not in path:
                new_path = list(path)
                new_path.append(each_node)
                new_action = list(action)
                new_action.append(each_action)
                frontier.push((new_path,new_action,cost+each_cost))
    return goal_action

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    print "Start:", problem.getStartState()
    #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    #print "Start's successors:", problem.getSuccessors(problem.getStartState())

    #Based on pseudocode
    #Initialize action list
    no_action = []
    goal_action = []
    #Get start state    
    start = problem.getStartState()
    start_path = []
    start_path.append(start)
    #Initialize frontier
    frontier = util.Queue()
    #Initialize closed list
    closed = {}
    #Frontier entries wil be in the form of (path, action list, cost)
    frontier.push((start_path,no_action,0))

    while not frontier.isEmpty():
        #Remove (path, action list, cost) from frontier
        path, action, cost = frontier.pop()
        if problem.isGoalState(path[-1]):
            return action
        #Decide whether or not to expand
        if path[-1] in closed:
            continue
        closed[path[-1]] = cost
        #Get successors    
        successors = problem.getSuccessors(path[-1])
        print "Successors:",successors
        for each_node, each_action, each_cost in successors:
            #Cycle checking
            if each_node not in closed:
                new_path = list(path)
                new_path.append(each_node)
                new_action = list(action)
                new_action.append(each_action)
                frontier.push((new_path,new_action,cost+each_cost))
    return goal_action

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    #print "Start:", problem.getStartState()
    #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    #print "Start's successors:", problem.getSuccessors(problem.getStartState())

    #Based on pseudocode
    #Initialize action list
    no_action = []
    goal_action = []
    #Get start state    
    start = problem.getStartState()
    start_path = []
    start_path.append(start)
    #Initialize frontier
    frontier = util.PriorityQueue()
    #Initialize closed dict
    closed = {}
    #Frontier entries wil be in the form of (path, action list, cost)
    frontier.push((start_path,no_action,0),0)

    while not frontier.isEmpty():
        #Remove (path, action list, cost) from frontier
        path, action, cost = frontier.pop()
        if problem.isGoalState(path[-1]):
            return action
        #Decide whether or not to expand
        if path[-1] in closed:
            continue
        closed[path[-1]] = cost
        #Get successors    
        successors = problem.getSuccessors(path[-1])
        #print "Successors:",successors
        for each_node, each_action, each_cost in successors:
            new_cost = cost + each_cost
            #Cycle checking
            if each_node not in closed or new_cost < closed[each_node]:
                new_path = list(path)
                new_path.append(each_node)
                new_action = list(action)
                new_action.append(each_action)
                frontier.push((new_path,new_action,new_cost),new_cost)
    return goal_action

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    #print "Start:", problem.getStartState()
    #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    #print "Start's successors:", problem.getSuccessors(problem.getStartState())

    #Based on pseudocode
    #Initialize action list
    no_action = []
    goal_action = []
    #Get start state    
    start = problem.getStartState()
    start_path = []
    start_path.append(start)
    #Initialize frontier
    frontier = util.PriorityQueue()
    #Initialize closed dict
    closed = {}
    #Frontier entries wil be in the form of (path, action list, cost)
    frontier.push((start_path,no_action,0),0+heuristic(start,problem))

    while not frontier.isEmpty():
        #Remove (path, action list, cost) from frontier
        path, action, cost = frontier.pop()
        #print "New value: " + str(cost)
        if problem.isGoalState(path[-1]):
            return action
        #Decide whether or not to expand
        if path[-1] in closed and cost >= closed[path[-1]]:
            continue
        closed[path[-1]] = cost
        #Get successors    
        successors = problem.getSuccessors(path[-1])
        # print "Successors:",successors
        for each_node, each_action, each_cost in successors:
            new_cost = cost+each_cost
            #Cycle checking
            if each_node not in closed or new_cost < closed[each_node]:
                new_path = list(path)
                new_path.append(each_node)
                new_action = list(action)
                new_action.append(each_action)
                frontier.push((new_path,new_action,new_cost),new_cost+heuristic(each_node,problem))
    return goal_action


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
