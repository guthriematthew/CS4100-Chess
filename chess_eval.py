import chess
import math
import bisect
import random
from chess_utils import game_over
from collections import Counter

PIECE_VALUE = {
    chess.PAWN: 100,
    chess.KNIGHT: 300,
    chess.BISHOP: 300,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 5000000000000
}

PIECE_SYMBOLS = [None, "p", "n", "b", "r", "q", "k"]

PAWN_PIECESQUARE = [0,  0,  0,  0,  0,  0,  0,  0,
                          5, 10, 10,-20,-20, 10, 10,  5,
                          5, -5,-10,  0,  0,-10, -5,  5,
                          0,  0,  0, 20, 20,  0,  0,  0,
                          5,  5, 10, 25, 25, 10,  5,  5,
                          10, 10, 20, 30, 30, 20, 10, 10,
                          50, 50, 50, 50, 50, 50, 50, 50,
                          0,  0,  0,  0,  0,  0,  0,  0]

KNIGHT_PIECESQUARE = [-50,-40,-30,-30,-30,-30,-40,-50,
                            -40,-20,  0,  5,  5,  0,-20,-40,
                            -30,  5, 10, 15, 15, 10,  5,-30,
                            -30,  0, 15, 20, 20, 15,  0,-30,
                            -30,  5, 15, 20, 20, 15,  5,-30,
                            -30,  0, 10, 15, 15, 10,  0,-30,
                            -40,-20,  0,  0,  0,  0,-20,-40,
                            -50,-40,-30,-30,-30,-30,-40,-50]

BISHOP_PIECESQUARE = [-20,-10,-10,-10,-10,-10,-10,-20,
                            -10,  5,  0,  0,  0,  0,  5,-10,
                            -10, 10, 10, 10, 10, 10, 10,-10,
                            -10,  0, 10, 10, 10, 10,  0,-10,
                            -10,  5,  5, 10, 10,  5,  5,-10,
                            -10,  0,  5, 10, 10,  5,  0,-10,
                            -10,  0,  0,  0,  0,  0,  0,-10,
                            -20,-10,-10,-10,-10,-10,-10,-20]

#                   a   b   c   d   e   f   g   h
ROOK_PIECESQUARE = [0,  0,  0,  5,  5,  0,  0,  0,  #1
                    -5,  0,  0,  0,  0,  0,  0, -5, #2
                    -5,  0,  0,  0,  0,  0,  0, -5, #3
                    -5,  0,  0,  0,  0,  0,  0, -5, #4 
                    -5,  0,  0,  0,  0,  0,  0, -5, #5
                    -5,  0,  0,  0,  0,  0,  0, -5, #6
                     5, 10, 10, 10, 10, 10, 10,  5, #7
                     0,  0,  0,  0,  0,  0,  0,  0] #8

QUEEN_PIECESQUARE = [-20,-10,-10, -5, -5,-10,-10,-20,
                           -10,  0,  5,  0,  0,  0,  0,-10,
                           -10,  5,  5,  5,  5,  5,  0,-10,
                            0,  0,  5,  5,  5,  5,  0, -5,
                            -5,  0,  5,  5,  5,  5,  0, -5,
                            -10,  0,  5,  5,  5,  5,  0,-10,
                            -10,  0,  0,  0,  0,  0,  0,-10,
                            -20,-10,-10, -5, -5,-10,-10,-20]

KING_PIECESQUARE_EG = [-50,-30,-30,-30,-30,-30,-30,-50,
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
    
    return ordered_moves

def eval_random(board, color):
    return random.randint(-100, 100)

# can use the psts to multiply piece value by the corresponding table's value for the square its moving to
# may need to mirror the psts and keep track of who's moving because values are not symmetrical
def calc_pst(board, legal_moves):
    pst_values = []
    for move in legal_moves:
        piece_type = board.piece_type_at(move.from_square)
        piece_sym = piece_type.symbol().lower()
        if piece_sym == "p":
            pst_values.append(PAWN_PIECESQUARE.get(move.to_square))
        elif piece_sym == "n":
            pst_values.append(KNIGHT_PIECESQUARE.get(move.to_square))
        elif piece_sym == "b":
            pst_values.append(BISHOP_PIECESQUARE.get(move.to_square))
        elif piece_sym == "q":
            pst_values.append(QUEEN_PIECESQUARE.get(move.to_square))
        elif piece_sym == "k":
            pst_values.append(KING_PIECESQUARE_EG.get(move.to_square))
        else:
            pst_values.append(0)
    return pst_values

# for every piece calculate the number of possible moves
def total_mobility(board, color, as_value=False):
    board = board.copy()
    board.turn = color
    legal_moves = list(board.legal_moves)
    move_from_square = {}
    for move in legal_moves:
        from_sq = move.from_square
        number_moves_currently = move_from_square.get(from_sq, 0) + 1
        move_from_square.update({from_sq: number_moves_currently})
    if not as_value:
        return move_from_square
    else:
        return sum([move_from_square[x] for x in move_from_square])

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


def center_control(board):
    center_squares = [chess.E4, chess.E5, chess.D4, chess.D5]
    white_center_control = sum(map(lambda x: len(board.attackers(chess.WHITE, x)), center_squares))
    black_center_control = sum(map(lambda x: len(board.attackers(chess.BLACK, x)), center_squares))
    return white_center_control, black_center_control


def eval_material(board, color):
    white_material, black_material = total_material(board, as_value=True)
    color_bias = 1 if color == chess.WHITE else -1
    if board.is_repetition(3):
        return -float('inf')
    return color_bias * (white_material - black_material)

def game_over_evaluation(board, color):
    outcome = board.outcome(claim_draw=True)
    if outcome.termination is not None and \
        outcome.termination == chess.Termination.CHECKMATE \
        and outcome.winner == color:
        return PIECE_VALUE[chess.KING]
    else:
        return -1 * PIECE_VALUE[chess.KING]

def endgame_evaluation(board, color):
    our_king = board.king(color)
    their_king = board.king(not color)

    evaluation = 0
    
    # push our king to center
    evaluation += KING_PIECESQUARE_EG[our_king]

    # push opponent king to edge
    evaluation += -1*KING_PIECESQUARE_EG[their_king]

    # decrease distance between kings
    evaluation -= abs(our_king - their_king)

    return evaluation

def eval_material_and_mobility(board, color):
    evaluation = 0
    evaluation += evaluate_material(board, color)
    evaluation += evaluate_mobility(board, color)

    return evaluation
'''
    board = board.copy()

    if game_over(board):
        return game_over_evaluation(board, color)

    white_material, black_material = total_material(board)
    white_mobility = total_mobility(board, chess.WHITE, as_value=True)
    black_mobility = total_mobility(board, chess.BLACK, as_value=True)

    white_material = Counter([chess.Piece.from_symbol(x) for x in white_material])
    black_material = Counter([chess.Piece.from_symbol(x) for x in black_material])

    my_material, their_material = (white_material, black_material) if color else (black_material, white_material)
    my_mobility, their_mobility = (white_mobility, black_mobility) if color else (black_mobility, white_mobility)

    evaluation = 0

    # Endgame Case
    is_endgame = 0 if my_material[chess.QUEEN] or their_material[chess.QUEEN] else 1
    endgame_bias = 1/(white_material.total() + black_material.total()) * endgame_evaluation(board, color)
    endgame_bias *= is_endgame

    # Evaluate Material
    evaluation += 100*(my_material[chess.QUEEN] - their_material[chess.QUEEN])
    evaluation += 9*(my_material[chess.ROOK] - their_material[chess.ROOK])
    evaluation += 5*(my_material[chess.BISHOP] - their_material[chess.BISHOP])
    evaluation += 3*(my_material[chess.KNIGHT] - their_material[chess.KNIGHT])
    evaluation += 1*(my_material[chess.PAWN] - their_material[chess.PAWN])

    # Evaluate Center Control
    white_center_control, black_center_control = center_control(board=board)
    evaluation += 5 * white_center_control if color == chess.WHITE else 10 * black_center_control

    # Evaluate Mobility
    evaluation += 0.1*(my_mobility - their_mobility)*is_endgame

    return endgame_bias + evaluation

    return endgame_bias * evaluation
    '''

def evaluate_mobility(board, color):
    board = board.copy()

    if game_over(board):
        game_over_evaluation(board, color)
    
    white_mobility = total_mobility(board, chess.WHITE, as_value=True)
    black_mobility = total_mobility(board, chess.BLACK, as_value=True)

    my_mobility, their_mobility = (white_mobility, black_mobility) if color else (black_mobility, white_mobility)

    evaluation = 0
    evaluation += 0.1*(my_mobility - their_mobility)

    return evaluation

def evaluate_material(board, color):
    board = board.copy()

    if game_over(board):
        game_over_evaluation(board, color)

    white_material, black_material = total_material(board)

    white_material = Counter([chess.Piece.from_symbol(x) for x in white_material])
    black_material = Counter([chess.Piece.from_symbol(x) for x in black_material])

    my_material, their_material = (white_material, black_material) if color else (black_material, white_material)
    evaluation = 0

    # Evaluate Material
    evaluation += 100*(my_material[chess.QUEEN] - my_material[chess.QUEEN])
    evaluation += 9*(my_material[chess.ROOK] - my_material[chess.ROOK])
    evaluation += 5*(my_material[chess.BISHOP] - my_material[chess.BISHOP])
    evaluation += 3*(my_material[chess.KNIGHT] - my_material[chess.KNIGHT])
    evaluation += 1*(my_material[chess.PAWN] - my_material[chess.PAWN])
    return evaluation



    





        