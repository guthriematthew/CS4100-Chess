from chess_game import ChessGame
from chess_agent import *
import chess
from stockfish import Stockfish

start_position = "3k4/8/8/5Q2/4K3/8/8/8 w - - 0 1"

game = ChessGame(starting_position=start_position)
white = WhiteScholarAgent()
black = BlackScholarAgent()
stockfish = Stockfish(path="/usr/local/bin/stockfish")

def f(board, color):
    
    return -1

def stock_f(board, color):
    stockfish.set_fen_position(board.fen())
    eval = stockfish.get_evaluation()
    if color == chess.BLACK:
        val = -eval['value']
    else:
        val = eval['value']
    return val


minimaxW = MinimaxAgent(chess.WHITE, stock_f, depth=2)
minimaxB = MinimaxAgent(chess.BLACK, stock_f, depth=2)

game.register_agent(minimaxW, True)
game.register_agent(minimaxB, False)
game.play_game()

