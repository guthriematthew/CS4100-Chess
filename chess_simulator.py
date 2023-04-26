import chess
import pandas as pd
from chess_game import ChessGame
from chess_agent import *
import random
from chess_eval import *
import chess.pgn
import json

VALID_AGENTS = ['stockfish', 'minimax','minimax_iterative', 'random']
SIMULATION_EVALS = ['eval_material', 
                    'eval_material_and_mobility', 
                    'eval_material_and_mobility_and_cc',
                      'complete_eval']
EVAL_LOOKUP = {
    'eval_material' : eval_material,
    'eval_material_and_mobility': eval_material_and_mobility,
    'eval_material_and_mobility_and_cc': eval_material_and_mobility_and_cc,
    'complete_eval' : complete_eval
}

## I think the only input should actuall be two evals 
# and the config rather than two agents
class ChessSimulator(object):

    """
    Input:
    agent1: the first agent
    agent2: the second agent
    config: tentative plan for how we want to pass analysis information to the simulator since it is liable to change
    -> current planned structure:
        {
            agent1_name : ['minimax', 'stockfish', 'minimax_iterative'],
            agent2_name : ['minimax', 'stockfish', 'minimax_iterative'],
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
            output_location : str
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
        self.output_location = config['output_location']

        if self.eval1_name in SIMULATION_EVALS and self.agent1_name != 'stockfish':
            self.eval1 = EVAL_LOOKUP[self.eval1_name]
        else:
            assert type(self.eval1_name) == int
            self.eval1 = self.eval1_name

        if self.eval2_name in SIMULATION_EVALS and self.agent2_name != 'stockfish':
            self.eval2 = EVAL_LOOKUP[self.eval1_name]
        else:
            assert type(self.eval2_name) == int
            self.eval2 = self.eval2_name

        if (self.agent1_name == 'random' or self.agent2_name == 'random') and self.random_seed is not None:
            random.seed(self.random_seed)

        #FOR NOW SETTING EVAL TO MOVEMENT AND MOBILITY
        self.white_agent1 = self.get_agent(self.agent1_name, chess.WHITE, eval=self.eval1, depth=self.depth1)
        self.black_agent1 = self.get_agent(self.agent1_name, chess.BLACK, eval=self.eval1, depth=self.depth1) 

        self.white_agent2 = self.get_agent(self.agent2_name, chess.WHITE, eval=self.eval2, depth=self.depth2)
        self.black_agent2 = self.get_agent(self.agent2_name, chess.BLACK, eval=self.eval2, depth=self.depth2) 


    
    def get_agent(self, agent_name, color, eval, moveTime=None, depth=None):
        if agent_name not in VALID_AGENTS:
            return
        elif agent_name == 'minimax':
            return MinimaxAgent(color=color, evaluationFunction=eval, depth=depth, moveTime=moveTime, iterate=False)
        elif agent_name == 'minimax_iterative':
            return MinimaxAgent(color=color, evaluationFunction=eval, depth=depth, moveTime=moveTime, iterate=True)
        elif agent_name == 'random':
            return RandomAgent()
        elif agent_name == 'stockfish':
            return StockfishAgent(elo=eval, depth=depth)
        
        ## Add stockfish agent when ready
                
    
    def run_simulation(self):
        games = {}
        for i in range(self.num_games):
            if self.swap_colors and i%2 == 1:
                games_out = self.simulate_game(whiteAgent=self.white_agent2, 
                                                blackAgent=self.black_agent1,
                                                starting_position=self.start_position,
                                                white_to_move=self.white_to_move)
            else:
                games_out = self.simulate_game(whiteAgent=self.white_agent1, 
                                                blackAgent=self.black_agent2,
                                                starting_position=self.start_position,
                                                white_to_move=self.white_to_move)
            for key in games_out:
                if key not in games:
                    games[key] = [games_out[key]]
                else:
                    games[key].append(games_out[key])
        
        output = pd.DataFrame(games)
        # for key, row in output.iterrows():
        #     self.to_pgn(row.white_agent, row.black_agent, row.moves)
        output.to_csv(self.output_location)
        return games



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
        # print(f"GAME TERMINATED WITH THE FOLLOWING MOVES {moves}")
        output = {
            'white': white,
            'black': black,
            'moves': moves,
            'white_agent': str(whiteAgent),
            'black_agent': str(blackAgent)
        }
        return output
        
        

    @staticmethod
    def record_quality(board, stockfish_elo, record_agent, opponent_agent, n=None):
        board = board.copy()
        stockfish_agent = StockfishAgent(stockfish_elo)

        game_record = [] # Holds (board, stockfish_move, agent_move, agent_move_grade) tuples

        while(not game_over(board)):
            agent_move_info = record_agent.get_next_move(board)
            agent_move = agent_move_info['move']
            stockfish_move_info = stockfish_agent.get_next_move(board)
            stockfish_move = stockfish_move_info['move']

            if n is not None:
                agent_move_grade = stockfish_agent.grade_move(board, agent_move)
            else:
                agent_move_grade = stockfish_agent.grade_move(board, agent_move, n=n)
            game_record.append((str(board), stockfish_move, agent_move, agent_move_grade))
            board.push(chess.Move.from_uci(stockfish_move))
            print(f"Stockfish Move: {stockfish_move}, Agent Move: {agent_move}, Agent Move Grade: {agent_move_grade}")
            print(board)
            print("===============")

            m_info = opponent_agent.get_next_move(board)
            m = m_info['move']
            board.push(chess.Move.from_uci(m))

        return game_record
    

    def to_pgn(self, white_agent_name, black_agent_name, moves):
        game = chess.pgn.Game()
        if self.start_position:
            game.setup(self.start_position)
        game.headers['White'] = white_agent_name
        game.headers['Black'] = black_agent_name
        node = game.add_main_variation(chess.Move.from_uci(moves[0]['move']))
        for m in moves[1:]:
            node = node.add_main_variation(chess.Move.from_uci(m['move']))
            # node.comment = f"Eval : {m['evaluation']} Number of Evaluations {m['num_eval']} Time: {m['time']}"
        with open('test.pgn', 'w') as f:
            f.write(str(game))
        print(game)


    @staticmethod
    def simulate_from_file(file_path):
        my_configs = []
        with open(file_path) as f:
            my_configs = json.load(f)

        for config in my_configs:
            sim = ChessSimulator(config)
            sim.run_simulation()


if __name__ == "__main__":
    config_file_location = "./simulator_configs.json"
    ChessSimulator.simulate_from_file(config_file_location)
