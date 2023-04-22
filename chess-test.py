import chess

# Getting all legal moves: https://stackoverflow.com/questions/62076938/how-to-get-a-list-of-all-the-legal-moves-in-the-python-chess-module

#Heuristic: minimax: white_material - black_material

STARTING_BOARD = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

board = chess.Board("6k1/5p2/6p1/8/7p/8/6PP/6K1 b - - 0 0")

print(board)