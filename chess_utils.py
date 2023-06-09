import os

def game_over(board):
    return board.is_game_over(claim_draw=True)

if os.name == "posix":
    print(f'\n\nLOGIN{os.getlogin()}\n\n')
    if os.getlogin() == 'liorzippel':
        STOCKFISH_PATH = "/usr/local/bin/stockfish"
    elif os.getlogin() == 'gunther':
        STOCKFISH_PATH = "/opt/homebrew/opt/stockfish/bin/stockfish"
    else:
        STOCKFISH_PATH = None 
else:
    STOCKFISH_PATH = None



DEFAULT_DEPTH = 3