import chess
import math
import bisect
import random

PIECE_VALUE = {
    chess.PAWN: 100,
    chess.KNIGHT: 300,
    chess.BISHOP: 300,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: math.inf
}

PIECE_SYMBOLS = [None, "p", "n", "b", "r", "q", "k"]

PAWN_PIECESQUARE_BLACK = [ 0,  0,  0,  0,  0,  0,  0,  0,
                    50, 50, 50, 50, 50, 50, 50, 50,
                    10, 10, 20, 30, 30, 20, 10, 10,
                    5,  5, 10, 25, 25, 10,  5,  5,
                    0,  0,  0, 20, 20,  0,  0,  0,
                    5, -5,-10,  0,  0,-10, -5,  5,
                    5, 10, 10,-20,-20, 10, 10,  5,
                    0,  0,  0,  0,  0,  0,  0,  0]

PAWN_PIECESQUARE_WHITE = [0,  0,  0,  0,  0,  0,  0,  0,
                          5, 10, 10,-20,-20, 10, 10,  5,
                          5, -5,-10,  0,  0,-10, -5,  5,
                          0,  0,  0, 20, 20,  0,  0,  0,
                          5,  5, 10, 25, 25, 10,  5,  5,
                          10, 10, 20, 30, 30, 20, 10, 10,
                          50, 50, 50, 50, 50, 50, 50, 50,
                          0,  0,  0,  0,  0,  0,  0,  0]
                          

KNIGHT_PIECESQUARE_BLACK = [-50,-40,-30,-30,-30,-30,-40,-50,
                      -40,-20,  0,  0,  0,  0,-20,-40,
                      -30,  0, 10, 15, 15, 10,  0,-30,
                      -30,  5, 15, 20, 20, 15,  5,-30,
                      -30,  0, 15, 20, 20, 15,  0,-30,
                      -30,  5, 10, 15, 15, 10,  5,-30,
                      -40,-20,  0,  5,  5,  0,-20,-40,
                      -50,-40,-30,-30,-30,-30,-40,-50]

KNIGHT_PIECESQUARE_WHITE = [-50,-40,-30,-30,-30,-30,-40,-50,
                            -40,-20,  0,  5,  5,  0,-20,-40,
                            -30,  5, 10, 15, 15, 10,  5,-30,
                            -30,  0, 15, 20, 20, 15,  0,-30,
                            -30,  5, 15, 20, 20, 15,  5,-30,
                            -30,  0, 10, 15, 15, 10,  0,-30,
                            -40,-20,  0,  0,  0,  0,-20,-40,
                            -50,-40,-30,-30,-30,-30,-40,-50]

BISHOP_PIECESQUARE_BLACK = [-20,-10,-10,-10,-10,-10,-10,-20,
                      -10,  0,  0,  0,  0,  0,  0,-10,
                      -10,  0,  5, 10, 10,  5,  0,-10,
                      -10,  5,  5, 10, 10,  5,  5,-10,
                      -10,  0, 10, 10, 10, 10,  0,-10,
                      -10, 10, 10, 10, 10, 10, 10,-10,
                      -10,  5,  0,  0,  0,  0,  5,-10,
                      -20,-10,-10,-10,-10,-10,-10,-20]

BISHOP_PIECESQUARE_WHITE = [-20,-10,-10,-10,-10,-10,-10,-20,
                            -10,  5,  0,  0,  0,  0,  5,-10,
                            -10, 10, 10, 10, 10, 10, 10,-10,
                            -10,  0, 10, 10, 10, 10,  0,-10,
                            -10,  5,  5, 10, 10,  5,  5,-10,
                            -10,  0,  5, 10, 10,  5,  0,-10,
                            -10,  0,  0,  0,  0,  0,  0,-10,
                            -20,-10,-10,-10,-10,-10,-10,-20]

#                   a   b   c    d   e   f   g   h
ROOK_PIECESQUARE_BLACK = [ 0,  0,  0,  0,  0,  0,  0,  0,     #8
                     5, 10, 10, 10, 10, 10, 10,  5,     #7
                    -5,  0,  0,  0,  0,  0,  0, -5,     #6
                    -5,  0,  0,  0,  0,  0,  0, -5,     #5
                    -5,  0,  0,  0,  0,  0,  0, -5,     #4
                    -5,  0,  0,  0,  0,  0,  0, -5,     #3
                    -5,  0,  0,  0,  0,  0,  0, -5,     #2
                     0,  0,  0,  5,  5,  0,  0,  0]     #1

#                         a   b   c   d   e   f   g   h
ROOK_PIECESQUARE_WHITE = [0,  0,  0,  5,  5,  0,  0,  0,  #1
                          -5,  0,  0,  0,  0,  0,  0, -5, #2
                          -5,  0,  0,  0,  0,  0,  0, -5, #3
                          -5,  0,  0,  0,  0,  0,  0, -5, #4 
                          -5,  0,  0,  0,  0,  0,  0, -5, #5
                          -5,  0,  0,  0,  0,  0,  0, -5, #6
                           5, 10, 10, 10, 10, 10, 10,  5, #7
                           0,  0,  0,  0,  0,  0,  0,  0] #8

QUEEN_PIECESQUARE_BLACK = [-20,-10,-10, -5, -5,-10,-10,-20,
                     -10,  0,  0,  0,  0,  0,  0,-10,
                     -10,  0,  5,  5,  5,  5,  0,-10,
                     -5,  0,  5,  5,  5,  5,  0, -5,
                      0,  0,  5,  5,  5,  5,  0, -5,
                    -10,  5,  5,  5,  5,  5,  0,-10,
                    -10,  0,  5,  0,  0,  0,  0,-10,
                    -20,-10,-10, -5, -5,-10,-10,-20]

QUEEN_PIECESQUARE_WHITE = [-20,-10,-10, -5, -5,-10,-10,-20,
                           -10,  0,  5,  0,  0,  0,  0,-10,
                           -10,  5,  5,  5,  5,  5,  0,-10,
                            0,  0,  5,  5,  5,  5,  0, -5,
                            -5,  0,  5,  5,  5,  5,  0, -5,
                            -10,  0,  5,  5,  5,  5,  0,-10,
                            -10,  0,  0,  0,  0,  0,  0,-10,
                            -20,-10,-10, -5, -5,-10,-10,-20]

KING_PIECESQUARE_EG_BLACK = [-50,-40,-30,-20,-20,-30,-40,-50,
                       -30,-20,-10,  0,  0,-10,-20,-30,
                       -30,-10, 20, 30, 30, 20,-10,-30,
                       -30,-10, 30, 40, 40, 30,-10,-30,
                       -30,-10, 30, 40, 40, 30,-10,-30,
                       -30,-10, 20, 30, 30, 20,-10,-30,
                       -30,-30,  0,  0,  0,  0,-30,-30,
                       -50,-30,-30,-30,-30,-30,-30,-50]

KING_PIECESQUARE_EG_WHITE = [-50,-30,-30,-30,-30,-30,-30,-50,
                             -30,-30,  0,  0,  0,  0,-30,-30,
                             -30,-10, 20, 30, 30, 20,-10,-30,
                             -30,-10, 30, 40, 40, 30,-10,-30,
                             -30,-10, 30, 40, 40, 30,-10,-30,
                             -30,-10, 20, 30, 30, 20,-10,-30,
                             -30,-20,-10,  0,  0,-10,-20,-30,
                             -50,-40,-30,-20,-20,-30,-40,-50]

def order_moves(board, legal_moves):
    ordered_moves = []
    for move in legal_moves:
        move_score = 0
        moving_piece_value = PIECE_VALUE[board.piece_type_at(move.from_square)]

        # prioritize capturing high value pieces, and ignore en passant
        if board.is_capture(move) and not board.is_en_passant(move):
            target_piece_value = PIECE_VALUE[board.piece_type_at(move.to_square)]
            move_score += target_piece_value - moving_piece_value

        # prioritize promoting pawn
        if move.promotion is not None:
            move_score += PIECE_VALUE[move.promotion] - moving_piece_value

        bisect.insort(ordered_moves, (move, move_score), key=lambda x: x[1])
    
    return [x for x, y in ordered_moves]

def eval_random(board, color):
    return random.randint(-100, 100)

# can use the psts to multiply piece value by the corresponding table's value for the square its moving to
# may need to mirror the psts and keep track of who's moving because values are not symmetrical
def calc_pst(board, legal_moves):
    pst_values = []
    for move in legal_moves:
        piece_type = board.piece_type_at(move.from_square)
        piece_sym = piece_type.symbol()
        if piece_sym == "p":
            pst_values.append(PAWN_PIECESQUARE_BLACK.get(move.to_square))
        elif piece_sym == "P":
            pst_values.append(PAWN_PIECESQUARE_WHITE.get(move.to_square))
        elif piece_sym == "n":
            pst_values.append(KNIGHT_PIECESQUARE_BLACK.get(move.to_square))
        elif piece_sym == "N":
            pst_values.append(KNIGHT_PIECESQUARE_WHITE.get(move.to_square))
        elif piece_sym == "b":
            pst_values.append(BISHOP_PIECESQUARE_BLACK.get(move.to_square))
        elif piece_sym == "B":
            pst_values.append(BISHOP_PIECESQUARE_WHITE.get(move.to_square))
        elif piece_sym == "q":
            pst_values.append(QUEEN_PIECESQUARE_BLACK.get(move.to_square))
        elif piece_sym == "Q":
            pst_values.append(QUEEN_PIECESQUARE_WHITE.get(move.to_square))
        elif piece_sym == "k":
            pst_values.append(KING_PIECESQUARE_EG_BLACK.get(move.to_square))
        elif piece_sym == "K":
            pst_values.append(KING_PIECESQUARE_EG_WHITE.get(move.to_square))
        else:
            pst_values.append(0)
    return pst_values

# for every piece calculate the number of possible moves
def total_mobility(board, legal_moves):
    move_from_square = {}
    for move in legal_moves:
        from_sq = move.from_square
        number_moves_currently = move_from_square.get(from_sq, 0) + 1
        move_from_square.update(from_sq, number_moves_currently)
    return move_from_square

#knowing a move, find the mobility for that piece    
def mobility_per_piece(move, mobility_dict):
    return mobility_dict.get(move.from_square, 0)

def total_material(board, as_value=False):
    board_str = str(board)
    white_material = []
    black_material = []
    for char in board_str:
        if char == " " or char == ".":
            continue
        
        if char.isupper():
            white_material.append(char)

        elif char.islower():
            black_material.append(char)

    if not as_value:
        return white_material, black_material
    else:
        white_total = sum([PIECE_VALUE[PIECE_SYMBOLS.index(x.lower())] for x in white_material])
        black_total = sum([PIECE_VALUE[PIECE_SYMBOLS.index(x)] for x in black_material])
        return white_total, black_total

def eval_material(board, color):
    white_material, black_material = total_material(board, as_value=True)
    color_bias = 1 if color == chess.WHITE else -1
    return color_bias * (white_material - black_material)


        