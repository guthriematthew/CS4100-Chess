from chess_game import ChessGame
from chess_agent import *
import chess
import random
from chess_eval import *
#from stockfish import Stockfish

start_position = "3k4/8/8/5Q2/4K3/8/8/8 w - - 0 1"

midgame="r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1"

ITALIAN="r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R"

endgame="8/8/5p2/1P1K1k2/8/2r5/8/7R w - - 0 0"

mate_1_endgame = "3k4/6R1/3K4/8/8/8/8/8 w - - 0 1"
mate_2_endgame = "1k6/6R1/2K5/8/8/8/8/8 b - - 0 1 "
game = ChessGame(mate_1_endgame, white_to_move=True)
# game = ChessGame()

white = WhiteScholarAgent()
black = BlackScholarAgent()
#stockfish = Stockfish(path="/usr/local/bin/stockfish")

"""def stock_f(board, color):
    stockfish.set_fen_position(board.fen())
    eval = stockfish.get_evaluation()
    if color == chess.BLACK:
        val = -eval['value']
    else:
        val = eval['value']
    return val
"""

minimaxW = MinimaxAgent(chess.WHITE, eval_material_and_mobility, depth=4, iterate=False)
minimaxB = MinimaxAgent(chess.BLACK, eval_material_and_mobility, depth=4, iterate=False)

game.register_agent(minimaxW, True)
game.register_agent(minimaxB, False)
game.play_game()

