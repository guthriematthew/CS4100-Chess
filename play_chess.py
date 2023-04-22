from chess_game import ChessGame
from chess_agent import *
import chess

game = ChessGame()
white = WhiteScholarAgent()
black = BlackScholarAgent()

def f(board, color):
    return -1
minimaxW = MinimaxAgent(chess.WHITE, f)
minimaxB = MinimaxAgent(chess.BLACK, f)

game.register_agent(minimaxW, True)
game.register_agent(minimaxB, False)
game.play_game()