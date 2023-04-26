import chess
import pandas as pd
from chess_game import ChessGame
from chess_agent import *
import random
from chess_eval import *

## I think the only input should actuall be two evals 
# and the config rather than two agents
class chess_simulator(object):

    """
    Input:
    agent1: the first agent
    agent2: the second agent
    config: tentative plan for how we want to pass analysis information to the simulator since it is liable to change
    -> current planned structure:
        {
            agent1_name : ['minimax', 'stockfish', 'minimax-terate'],
            agent2_name : ['minimax', 'stockfish', 'minimax-terate'],
            depth1 : int,
            depth2 : int,
            eval1 : ['material_mobility' ... ELO-for Stockfish],
            eval2 : ['material_mobility' ... ELO-for Stockfish],
            num_games : int,
            start_position : str(board fen)=none,
            is_960: boolean,
            max_time1 : int,
            max_time2 : int
        }
    """
    def __init__(self,config):
        self.agent1_name = config['agent1_name']
        self.agent2_name = config['agent2_name']
        self.depth1 = config['depth1']
        self.depth2 = config['depth2']
        self.eval1 = config['eval1']
        self.eval2 = config['eval2']
        self.num_games = config['num_games']
        self.start_position = None if 'start_position' not in config else config['start_position']
        self.max_time1 = None if 'max_time1' not in config else config['max_time1']
        self.max_time2 = None if 'max_time2' not in config else config['max_time2']
            
        # self.agent1 = agent1
        # self.agent2 = agent2

    def simulate_game(self, whiteAgent, blackAgent):
        sim_game = ChessGame()
        
        sim_game.register_agent(whiteAgent, True)
        sim_game.register_agent(blackAgent, False)
        
        gameOutcome = sim_game.play_game()
        moves = sim_game.moves
        if gameOutcome.winner:
            if gameOutcome.winner == chess.WHITE:
                white = 1
                black = 0
            else:
                white = 0
                black = 1
        else:
            white = 0.5
            black = 0.5
        
        outcomeDF = pd.DataFrame()
        outcomeDF['white'] = white
        outcomeDF['black'] = black
        outcomeDF['whiteAgent']
        






