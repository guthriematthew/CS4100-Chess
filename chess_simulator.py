import chess
import pandas as pd
from chess_game import ChessGame
from chess_agent import *
import random
from chess_eval import *

## I think the only input should actuall be two evals and the config
class chess_simulator(object):

    """
    Input:
    agent1: the first agent
    agent2: the second agent
    config: tentative plan for how we want to pass analysis information to the simulator since it is liable to change
    -> current planned structure:
        {
            outputLocation: /eval/game/etc.,
            agent1Name: minimax, random whatever,
            agent2Name: minimax, random whatever,
            boardPosition: optional starting board position, could change this to a list
            numberOfGames: how many games to simulate

        }
    """
    def __init__(self, agent1, agent2, config):
        self.agent1 = agent1
        self.agent2 = agent2

    def simulate_game(self, whiteAgent, blackAgent):
        sim_game = ChessGame()



