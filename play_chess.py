from chess_game import ChessGame
from chess_agent import *
import chess

game = ChessGame()
white = WhiteScholarAgent()
black = BlackScholarAgent()

def f(board):
    return -1

minimax = MinimaxAgent(chess.BLACK, f)

game.register_agent(white, True)
game.register_agent(minimax, False)
game.play_game()