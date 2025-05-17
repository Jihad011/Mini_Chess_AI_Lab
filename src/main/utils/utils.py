from .constants import *

def is_white(piece: int) -> bool:
    return piece > 0

def is_black(piece: int) -> bool:
    return piece < 0

def is_opponent(piece: int, target: int) -> bool:
    if target == EMPTY:
        return False
    return (is_white(piece) and is_black(target)) or (is_black(piece) and is_white(target))

def is_same_side(piece1: int, piece2: int) -> bool:
    if piece1 == EMPTY or piece2 == EMPTY:
        return False
    return (is_white(piece1) and is_white(piece2)) or (is_black(piece1) and is_black(piece2))

def is_own_piece(piece: int, is_white_turn: bool) -> bool:
    if piece == EMPTY:
        return False
    return (is_white(piece) and is_white_turn) or (is_black(piece) and not is_white_turn)


def is_within_board(row: int, col: int, board) -> bool:
    return 0 <= row < len(board) and 0 <= col < len(board[0])

def get_piece_position(board, piece):
    """Returns (row, col) of first found piece or None if not found."""
    return next(((i, j) for i, row in enumerate(board)
               for j, p in enumerate(row) if p == piece), None)


def is_ai_turn(is_play_with_ai: bool, player_white_turn: bool) -> bool:
    return is_play_with_ai and not player_white_turn

