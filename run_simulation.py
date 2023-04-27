from chess_simulator import ChessSimulator
from joblib import Parallel, delayed
import time


mate_1_endgame = "3k4/6R1/3K4/8/8/8/8/8 w - - 0 1"
mate_2_endgame = "1k6/6R1/2K5/8/8/8/8/8 b - - 0 1"
mate_3_endgame = "k7/6R1/2K5/8/8/8/8/8 w - - 0 1"

SIMULATION_EVALS = ['eval_material', 
                    'eval_material_and_mobility', 
                    'eval_material_and_mobility_and_cc',
                      'complete_eval']

run_config = {
    'agent1_name' : 'minimax',
    'agent2_name' : 'stockfish',
    'depth1' : 4,
    'depth2' : 4,
    'eval1': 'complete_eval',
    'eval2': 2000,
    'num_games' : 1,
    'start_position' : None,
    'white_to_move':False,
    'swap_colors': True,
    'output_location':'data/initial.csv'
}

# chess_sim1 = ChessSimulator(run_config)

# g = chess_sim1.run_simulation()



# num_jobs = 1
# gs = []
# start = time.time()
# Parallel(n_jobs=num_jobs, prefer="threads")(delayed(ChessSimulator.run_simulation)(run_c) for run_c in run_cs)
# print(time.time()-start)