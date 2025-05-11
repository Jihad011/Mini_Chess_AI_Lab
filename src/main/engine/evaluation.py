from src.main.gameplay.board_state import BoardState
from src.main.utils.utils import *

# Position bonus maps for 5x6 board_state (white perspective)
PAWN_POSITION_BONUS = [
    [80, 80, 80, 80, 80],    # Almost promoted
    [50, 50, 50, 50, 50],    # Near promotion
    [30, 30, 40, 30, 30],    # Advanced
    [20, 20, 30, 20, 20],    # Past middle
    [10, 10, 20, 10, 10],    # Moving out
    [0,  0,  0,  0,  0]      # Starting position
]

KNIGHT_POSITION_BONUS = [
    [-20, -10,  0, -10, -20],
    [-10,  0,  10,  0, -10],
    [0,   10,  20, 10,  0],
    [0,   10,  20, 10,  0],
    [-10,  0,  10,  0, -10],
    [-20, -10,  0, -10, -20]
]

BISHOP_POSITION_BONUS = [
    [-10, -5,  0, -5, -10],
    [-5,  0,  10,  0, -5],
    [0,   10, 15, 10,  0],
    [0,   10, 15, 10,  0],
    [-5,  0,  10,  0, -5],
    [-10, -5,  0, -5, -10]
]

ROOK_POSITION_BONUS = [
    [0,  0,  5,  0,  0],
    [5,  5,  5,  5,  5],
    [0,  0,  0,  0,  0],
    [0,  0,  0,  0,  0],
    [5,  5,  5,  5,  5],
    [0,  0,  5,  0,  0]
]

QUEEN_POSITION_BONUS = [
    [-10, -5,  0, -5, -10],
    [-5,  0,  5,  0, -5],
    [0,   5,  10, 5,  0],
    [0,   5,  10, 5,  0],
    [-5,  0,  5,  0, -5],
    [-10, -5,  0, -5, -10]
]

KING_POSITION_BONUS = [
    [-60, -60, -60, -60, -60],
    [-60, -60, -60, -60, -60],
    [-40, -40, -40, -40, -40],
    [-20, -20, -20, -20, -20],
    [-10, -10, -10, -10, -10],
    [20,   30,  0,  30,  20]  # Back rank is safest
]

POSITION_BONUS = {
    abs(WHITE_PAWN): PAWN_POSITION_BONUS,
    abs(WHITE_KNIGHT): KNIGHT_POSITION_BONUS,
    abs(WHITE_BISHOP): BISHOP_POSITION_BONUS,
    abs(WHITE_ROOK): ROOK_POSITION_BONUS,
    abs(WHITE_QUEEN): QUEEN_POSITION_BONUS,
    abs(WHITE_KING): KING_POSITION_BONUS
}


def evaluate_board(board_state: BoardState, engine_white_turn: bool) -> int:
    """Evaluates the board from the ENGINE'S perspective.
    Returns:
        Positive score if engine has advantage,
        Negative score if opponent has advantage,
        Zero if equal position
    """
    board_row = len(board_state.board)
    board_col = len(board_state.board[0])
    score = 0
    board = board_state.board

    for row in range(board_row):
        for col in range(board_col):
            piece = board[row][col]
            if piece == EMPTY:
                continue

            abs_piece = abs(piece)
            value = PIECE_VALUES.get(abs_piece, 0)

            # Always use white's perspective for bonus maps
            pos_row = row if is_white(piece) else board_row - 1 - row
            bonus = POSITION_BONUS.get(abs_piece, [[0]*board_col]*board_row)[pos_row][col]

            if is_white(piece) == engine_white_turn:
                score += value + bonus
            else:
                score -= value + bonus

    return score



# needs to be tested
def mobility_bonus(board_state: BoardState) -> int:
    """Calculates mobility score from current player's perspective."""
    from src.main.gameplay.move_generator import MoveGenerator
    
    move_gen = MoveGenerator()
    current_moves = len(move_gen.generate_all_moves(board_state))
    
    # Save current turn
    current_turn = board_state.is_white_turn
    
    # Switch turn to calculate opponent's mobility
    board_state.is_white_turn = not current_turn
    opponent_moves = len(move_gen.generate_all_moves(board_state))
    
    # Restore original turn
    board_state.is_white_turn = current_turn
    
    return (current_moves - opponent_moves) * 10