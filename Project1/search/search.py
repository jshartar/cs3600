# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def GSA(problem, visit):
    visited = []
    node = problem.getStartState()
    path = []
    visit.push((node, path))
    while (not problem.isGoalState(node)) and (not visit.isEmpty()):
        item = visit.pop()
        node = item[0]
        path = item[1]
        if problem.isGoalState(node):
            return path
        visited.append(node)
        for x in problem.getSuccessors(node):
            if x[0] not in visited:
                p = path[:]
                p.append(x[1][:])
                visit.push((x[0], p))
    if problem.isGoalState(node):
        return path
    else:
        return None


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    from util import Stack
    visit = Stack()
    return GSA(problem, visit)

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    from util import Queue

    visit = Queue()
    visited = []
    node = problem.getStartState()
    path = []
    visit.push((node, path))
    while (not problem.isGoalState(node)) and (not visit.isEmpty()):
        item = visit.pop()
        node = item[0]
        path = item[1]
        if problem.isGoalState(node):
            return path
        visited.append(node)
        for x in problem.getSuccessors(node):
            if x[0] not in visited:
                p = path[:]
                p.append(x[1][:])
                visit.push((x[0], p))
                visited.append(x[0])
    if problem.isGoalState(node):
        return path
    else:
        return None


    util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    from game import Directions
    visit = util.PriorityQueue()
    visited = []
    path = []
    last = {}
    list = []
    cost = {}
    start = ((problem.getStartState(), Directions.EAST, 0), 0)
    visited.append(start[0][0])
    list.append(start[0][0])
    cost[start[0][0]] = 0
    succ = problem.getSuccessors(problem.getStartState())
    succ.sort()
    for x in succ:
        last[x[0]] = start
        cost[x[0]] = cost[start[0][0]] + x[2]
        visit.push((x, cost[x[0]]), cost[x[0]])
        list.append(x[0])
        visited.append(x)
    curr = visit.pop()
    while not problem.isGoalState(curr[0][0]) and visit:
        visited.append(curr[0][0])
        cost[curr[0][0]] = curr[0][2] + cost[last[curr[0][0]][0][0]]
        successors = problem.getSuccessors(curr[0][0])
        successors.sort()
        for x in successors:
            itemCost = x[2] + cost[curr[0][0]]
            if (x[0] not in visited) and (x[0] not in list):
                last[x[0]] = curr
                cost[x[0]] = itemCost
                visit.push((x, cost[x[0]]), cost[x[0]])
                list.append(x[0])
            elif x[0] in list and itemCost < cost[x[0]]:
                last[x[0]] = curr
                cost[x[0]] = itemCost
                visit.push((x, cost[x[0]]), cost[x[0]])
                list.append(x[0])
        curr = visit.pop()
    while curr != start:
        path.append(curr[0][1])
        curr = last[curr[0][0]]
    path.reverse()
    return path

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    path = []
    cost = 0
    visit = util.PriorityQueue()
    visit.push((start, path, cost), 0)
    visited = list()
    while visit:
        curr = visit.pop()
        node = curr[0]
        path = curr[1]
        cost = curr[2]
        if node not in visited:
            visited.append(node)
            if problem.isGoalState(node):
                return path
            for state, action, c in problem.getSuccessors(node):
                if state not in visited:
                    p = path[:]
                    p.append(action)
                    visit.push((state, p, cost + c), cost + c + heuristic(state, problem))
    return path

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
