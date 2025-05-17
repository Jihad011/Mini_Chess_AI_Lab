from src.main.gameplay.board_state import BoardState
from src.main.utils.utils import *
from src.main.utils.constants import *
from src.main.utils.engine_constants import *
from typing import NamedTuple


class BoardFeatures(NamedTuple):
    material_difference: int
    piece_counts: dict[int, int]  # piece type -> count on board
    positional_score: int
    current_piece_count: int



def extract_board_features(board_state: BoardState, engine_white_turn: bool) -> BoardFeatures:
    board_row = len(board_state.board)
    board_col = len(board_state.board[0])
    material_difference = 0
    positional_score = 0
    current_piece_count = 0
    piece_counts = {pt: 0 for pt in PIECE_VALUES.keys()}

    for row in range(board_row):
        for col in range(board_col):
            piece = board_state.board[row][col]
            if piece == EMPTY:
                continue
            current_piece_count += 1

            abs_piece = abs(piece)
            piece_counts[abs_piece] += 1

            value = PIECE_VALUES.get(abs_piece, 0)
            pos_row = row if is_white(piece) else board_row - 1 - row
            bonus = POSITION_BONUS.get(abs_piece, [[0]*board_col]*board_row)[pos_row][col]

            if is_white(piece) == engine_white_turn:
                material_difference += value
                positional_score += bonus
            else:
                material_difference -= value
                positional_score -= bonus

    return BoardFeatures(
        material_difference=material_difference,
        piece_counts=piece_counts,
        positional_score=positional_score,
        current_piece_count=current_piece_count,
    )


def evaluate_board(board_state: BoardState, engine_white_turn: bool) -> int:
    """Evaluates the board from the ENGINE'S perspective.
    Returns:
        Positive score if engine has advantage,
        Negative score if opponent has advantage,
        Zero if equal position
    """
    features = extract_board_features(board_state, engine_white_turn)
    if is_insufficient_material(features):
        return 0

    score = features.material_difference + features.positional_score
    if features.material_difference >= 300:
        score += TRADE_BONUS * (TOTAL_PIECE_COUNT - features.current_piece_count)


    return score



def is_insufficient_material(feature: BoardFeatures) -> bool:

    if feature.current_piece_count == 2:
        return True  # King vs King
    if feature.current_piece_count == 3 and feature.piece_counts.get(WHITE_KNIGHT, 0) == 1:
        return True  # King vs Knight

    return False