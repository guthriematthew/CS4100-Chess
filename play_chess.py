from chess_game import ChessGame
from chess_agent import *
import chess
import random
from chess_eval import *
#from stockfish import Stockfish

start_position = "3k4/8/8/5Q2/4K3/8/8/8 w - - 0 1"

midgame="r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1"

game = ChessGame()

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

minimaxW = MinimaxAgent(chess.WHITE, eval_material, depth=4, moveTime=5)
minimaxB = MinimaxAgent(chess.BLACK, eval_material, depth=4, moveTime=5)

game.register_agent(minimaxW, True)
game.register_agent(minimaxB, False)
game.play_game()

