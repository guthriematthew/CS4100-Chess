import os

def game_over(board):
    return board.is_game_over(claim_draw=True)

if os.name == "posix":
    STOCKFISH_PATH = "/opt/homebrew/opt/stockfish/bin/stockfish"
else:
    STOCKFISH_PATH = None

DEFAULT_DEPTH = 3