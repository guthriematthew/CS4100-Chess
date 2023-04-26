from chess_simulator import ChessSimulator

mate_1_endgame = "3k4/6R1/3K4/8/8/8/8/8 w - - 0 1"
mate_2_endgame = "1k6/6R1/2K5/8/8/8/8/8 b - - 0 1"
mate_3_endgame = "k7/6R1/2K5/8/8/8/8/8 w - - 0 1"

run_config = {
    'agent1_name' : 'minimax_iterative',
    'agent2_name' : 'stockfish',
    'depth1' : 4,
    'depth2' : 4,
    'eval1': 'PLACEHOLDER',
    'eval2': 'PLACEHOLDER',
    'num_games' : 4,
    'start_position' : mate_1_endgame,
    'white_to_move':True,
    'swap_colors': True
}

chess_sim1 = ChessSimulator(run_config)

g = chess_sim1.run_simulation()
print(g)