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
        