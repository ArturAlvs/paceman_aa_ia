# pacmanAgents.py
# ---------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from pacman import Directions
from game import Agent
from searchAgents import PositionSearchProblem
import random
import game
import util
import search



class MyPacman( Agent ):

  def __init__( self):

    self.searchFunction = lambda prob: search.aStarSearch(prob)
    # self.searchType = PositionSearchProblem
    self.searchType = lambda state, goal, posIni: PositionSearchProblem(state, goal=goal, startStatao=posIni )

    self.movimentos = []

    self.food = None

  def generateMoves(self, state):
    posicao_Pacman = state.getPacmanPosition()

    # pegando as comidas
    comida_grid = state.getFood()
    # to list
    comida_list = list(comida_grid.asList())
    dist, comida_do_pacman = random.choice([(util.manhattanDistance(posicao_Pacman, food), food) for food in comida_list])  # Obtem a comida_do_pacman mais proxima do Pacman utilizando a distancia de manhattan.



    if self.food == None or posicao_Pacman == self.food :
      for fantasma_pos in state.getGhostPositions():
        if self.food != fantasma_pos:
          self.food = comida_do_pacman

    
    prob = self.searchType(state, self.food, posicao_Pacman)

    self.movimentos = self.searchFunction(prob)

    # print("self.movimentos")
    # print(self.movimentos)



  def getAction( self, state ):
    
    self.generateMoves(state)

    # Se nao tiver mais acao, fica parado
    try:
      acao = self.movimentos.pop(0)
    except Exception as e:
      acao = Directions.STOP

    return acao

class LeftTurnAgent(game.Agent):
  "An agent that turns left at every opportunity"
  
  def getAction(self, state):
    legal = state.getLegalPacmanActions()
    current = state.getPacmanState().configuration.direction
    if current == Directions.STOP: current = Directions.NORTH
    left = Directions.LEFT[current]
    if left in legal: return left
    if current in legal: return current
    if Directions.RIGHT[current] in legal: return Directions.RIGHT[current]
    if Directions.LEFT[left] in legal: return Directions.LEFT[left]
    return Directions.STOP

class GreedyAgent(Agent):
  def __init__(self, evalFn="scoreEvaluation"):
    self.evaluationFunction = util.lookup(evalFn, globals())
    assert self.evaluationFunction != None
   #Olhar de novo     
  def getAction(self, state):
    # Generate candidate actions
    legal = state.getLegalPacmanActions()
    if Directions.STOP in legal: legal.remove(Directions.STOP)
      
    successors = [(state.generateSuccessor(0, action), action) for action in legal] 
    scored = [(self.evaluationFunction(state), action) for state, action in successors]
    bestScore = max(scored)[0]
    bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
    return random.choice(bestActions)
  
def scoreEvaluation(state):
  return state.getScore()  