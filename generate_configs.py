import json
from chess_simulator import VALID_AGENTS
from chess_eval import SIMULATION_EVALS
import chess
"""
Input:
agent1: the first agent
agent2: the second agent
config: tentative plan for how we want to pass analysis information to the simulator since it is liable to change
-> current planned structure:
    {
        agent1_name : ['minimax', 'stockfish', 'minimax-iterate'],
        agent2_name : ['minimax', 'stockfish', 'minimax-iterate'],
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

OUTPUT_FILE = "./simulator_configs.json"

IS_960 = True
NOT_960 = not IS_960

WHITE_TO_MOVE = True
BLACK_TO_MOVE = not WHITE_TO_MOVE

depth1_depths = list(range(3, 4))
depth2_depths = list(range(3, 4))

start_positions = [
    (chess.STARTING_BOARD_FEN, NOT_960, WHITE_TO_MOVE)
    ]

max_time1 = None
max_time2 = None
swap_colors = True
white_to_move = True
num_games = 2
random_seed = 69

def name(agent_name, depth, eval):
    return f"./data/vs_random/{agent_name}_{depth}_{eval}"

def create_config(agent1, agent2, depth1, depth2, eval1, eval2, start_position, is_960, white_to_move):
    config =     {
        'agent1_name' : agent1,
        'agent2_name' : agent2,
        'depth1' : depth1,
        'depth2' : depth2,
        'eval1' : eval1,
        'eval2' : eval2,
        'num_games' : num_games,
        'start_position' : start_position,
        'is_960': is_960,
        'max_time1' : max_time1,
        'max_time2' : max_time2,
        'random_seed': random_seed,
        'white_to_move' : white_to_move,
        'swap_colors' : swap_colors,
        'output_location': name(agent1, depth1, eval1)
    }
    return config

configs = []

for agent1 in VALID_AGENTS:
    for agent2 in ['random']:
        if agent1 == agent2 or agent1 == 'stockfish' or agent2 == 'stockfish' or agent1 == 'random':
            # Assuming we don't want the same agents to play against each other 
            continue
        for depth1 in depth1_depths:
            for depth2 in depth2_depths:
                for eval1 in SIMULATION_EVALS:
                    for eval2 in ["eval_material"]:
                        for start_position, is_960, white_to_move in start_positions:
                            config = create_config(agent1, agent2, depth1, depth2, eval1, eval2, start_position, is_960, white_to_move)
                            configs.append(config)

with open(OUTPUT_FILE, 'w') as f:
    json.dump(configs, f, indent=4)