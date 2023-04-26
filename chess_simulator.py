import chess
import pandas as pd
from chess_game import ChessGame
from chess_agent import *
import random
from chess_eval import *

VALID_AGENTS = ['stockfish', 'minimax','minimax_iterative', 'random']

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
            max_time2 : int,
            random_seed: int,
            white_to_move : boolean=True,
            swap_colors : boolean=True
        }
    """
    def __init__(self, config):
        
        self.agent1_name = config['agent1_name']
        self.agent2_name = config['agent2_name']
        self.depth1 = config['depth1']
        self.depth2 = config['depth2']
        self.eval1_name = config['eval1']
        self.eval2_name = config['eval2']
        self.num_games = config['num_games']
        self.start_position = None if 'start_position' not in config else config['start_position']
        self.max_time1 = None if 'max_time1' not in config else config['max_time1']
        self.max_time2 = None if 'max_time2' not in config else config['max_time2']
        self.random_seed = None if 'random_seed' not in config else config['random_seed']
        self.white_to_move = True if 'white_to_move' not in config else config['white_to_move']
        self.swap_colors = True if 'swap_colors' not in config else config['swap_colors']

        #FOR NOW SETTING EVAL TO MOVEMENT AND MOBILITY
        self.white_agent1 = self.get_agent(self.agent1_name, chess.WHITE, eval=eval_material_and_mobility_and_cc, depth=4)
        self.black_agent1 = self.get_agent(self.agent1_name, chess.BLACK, eval=eval_material_and_mobility_and_cc, depth=4) 

        self.white_agent2 = self.get_agent(self.agent2_name, chess.WHITE, eval=eval_material_and_mobility_and_cc, depth=4)
        self.black_agent2 = self.get_agent(self.agent2_name, chess.BLACK, eval=eval_material_and_mobility_and_cc, depth=4) 

    def get_agent(self, agent_name, color, eval, moveTime=None, depth=None):
        if agent_name not in VALID_AGENTS:
            return
        elif agent_name == 'minimax':
            return MinimaxAgent(color=color, evaluationFunction=eval, depth=depth, moveTime=moveTime, iterate=False)
        elif agent_name == 'minimax_iterative':
            return MinimaxAgent(color=color, evaluationFunction=eval, depth=depth, moveTime=moveTime, iterate=True)
        elif agent_name == 'random':
            return RandomAgent()
        else:
            return
        ## Add stockfish agent when ready
                
    
    def run_simulation(self):
        for i in range(self.num_games):



    def simulate_game(self, whiteAgent, blackAgent, starting_position, white_to_move):
        sim_game = ChessGame(white_to_move=white_to_move, starting_position=starting_position)
        
        sim_game.register_agent(whiteAgent, chess.WHITE)
        sim_game.register_agent(blackAgent, chess.BLACK)
        
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
        print(f"GAME TERMINATED WITH THE FOLLOWING MOVES {moves}")
        return moves
        
        
        outcomeDF = pd.DataFrame()
        outcomeDF['white'] = white
        outcomeDF['black'] = black
        outcomeDF['whiteAgent']

    def record_quality(self, board, stockfish_elo, record_agent, opponent_agent):
        board = board.copy()
        stockfish_agent = StockfishAgent(stockfish_elo)

        game_record = [] # Holds (board, stockfish_move, agent_move, agent_move_grade) tuples

        while(not game_over(board)):
            agent_move, agent_move_info = record_agent.get_next_move(board)
            stockfish_move, _ = stockfish_agent.get_next_move(board)
            agent_move_grade = stockfish_agent.grade_move(board, move)
            game_record.append((str(board), stockfish_move, agent_move, agent_move_grade))
            board.push(stockfish_move)

            m, _ = opponent_agent.get_next_move(board)
            board.push(m)

        return game_record


        






