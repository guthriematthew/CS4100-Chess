from chess_game import ChessGame
from chess_agent import *

game = ChessGame()
white = WhiteScholarAgent()
black = BlackScholarAgent()

game.register_agent(white, True)
game.register_agent(black, False)
game.play_game()