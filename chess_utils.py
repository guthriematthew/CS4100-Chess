def game_over(board):
    return board.is_checkmate() \
    or board.is_stalemate() \
    or board.is_insufficient_material()