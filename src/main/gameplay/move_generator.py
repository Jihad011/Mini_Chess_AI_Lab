from src.main.utils.constants import *
from .board_state import BoardState
from .move_state import MoveState
from ..utils.utils import is_opponent, is_own_piece, is_within_board


class MoveGenerator:
    def __init__(self):
        pass

    def generate_all_moves(self, board_state: BoardState):
        rows, cols = len(board_state.board), len(board_state.board[0])

        # List comprehension to gather all valid moves
        return [
            move
            for row in range(rows)
            for col in range(cols)
            if is_own_piece(board_state.board[row][col], board_state.is_white_turn)
            for move in self.generate_piece_moves(board_state, (row, col))
        ]




    def generate_piece_moves(self, board_state: BoardState, pos):

        piece = board_state.board[pos[0]][pos[1]]
        if not is_own_piece(piece, board_state.is_white_turn):
            return []


        if piece == WHITE_PAWN or piece == BLACK_PAWN:
            return self.get_pawn_moves(board_state, pos)
        elif piece == WHITE_ROOK or piece == BLACK_ROOK:
            return self.get_rook_moves(board_state, pos)
        elif piece == WHITE_KNIGHT or piece == BLACK_KNIGHT:
            return self.get_opt_knight_moves(board_state, pos)
        elif piece == WHITE_BISHOP or piece == BLACK_BISHOP:
            return self.get_bishop_moves(board_state, pos)
        elif piece == WHITE_QUEEN or piece == BLACK_QUEEN:
            return self.get_queen_moves(board_state, pos)
        elif piece == WHITE_KING or piece == BLACK_KING:
            return self.get_opt_king_moves(board_state, pos)
        elif piece == EMPTY:
            return []
        else:
            raise ValueError("Invalid piece type")


    # default perspective is white
    # white pawn will move up(-1) and black moves down(+1)
    def get_pawn_moves(self, board_state: BoardState, pos):
        row, col = pos
        piece = board_state.board[row][col]
        turn = board_state.is_white_turn
        moves = []

        # Determine movement direction based on turn
        direction = -1 if turn else 1

        # Forward move (if target square is empty)
        new_row = row + direction
        if 0 <= new_row < len(board_state.board):
            if board_state.board[new_row][col] == EMPTY:
                is_promoted = (new_row == 0 and turn) or (new_row == len(board_state.board) - 1 and not turn)
                moves.append(MoveState((row, col), (new_row, col), piece, None, is_promoted))

        # Diagonal captures (must have opponent piece)
        for dc in [-1, 1]:
            new_col = col + dc
            if is_within_board(new_row, new_col, board_state.board):
                target = board_state.board[new_row][new_col]
                if is_opponent(piece, target):
                    is_promoted = (new_row == 0 and turn) or (new_row == len(board_state.board) - 1 and not turn)
                    moves.append(MoveState((row, col), (new_row, new_col), piece, target, is_promoted))

        return moves


    def get_opt_knight_moves(self, board_state: BoardState, pos):
        row, col = pos
        piece = board_state.board[row][col]
        moves = []

        # Retrieve precomputed knight moves
        for new_row, new_col in KNIGHT_MOVES_FROM.get((row, col), []):
            target = board_state.board[new_row][new_col]

            if target == EMPTY or is_opponent(piece, target):
                move_state = MoveState((row, col), (new_row, new_col), piece, target if target != EMPTY else None)
                moves.append(move_state)

        return moves



    def get_bishop_moves(self, board_state: BoardState, pos):
        diagonal_dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        return self.get_sliding_moves(board_state, pos, diagonal_dirs)


    def get_rook_moves(self, board_state: BoardState, pos):
        straight_dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return self.get_sliding_moves(board_state, pos, straight_dirs)


    def get_queen_moves(self, board_state: BoardState, pos):
        straight_and_diagonal_dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1),(-1, 0), (1, 0), (0, -1), (0, 1)]
        return self.get_sliding_moves(board_state, pos, straight_and_diagonal_dirs)



    def get_sliding_moves(self, board_state: BoardState, pos, directions):
        row, col = pos
        piece = board_state.board[row][col]
        moves = []

        for dr, dc in directions:
            new_row, new_col = row, col
            while True:
                new_row += dr
                new_col += dc

                if not is_within_board(new_row, new_col, board_state.board):
                    break

                target = board_state.board[new_row][new_col]

                if target == EMPTY:
                    move_state = MoveState((row, col), (new_row, new_col), piece, None)
                    moves.append(move_state)
                elif is_opponent(piece, target):
                    move_state = MoveState((row, col), (new_row, new_col), piece, target)
                    moves.append(move_state)
                    break
                else:
                    break

        return moves




    def get_opt_king_moves(self, board_state: BoardState, pos):
        row, col = pos
        piece = board_state.board[row][col]
        moves = []

        # Retrieve precomputed king moves
        for new_row, new_col in KING_MOVES_FROM.get((row, col), []):
            target = board_state.board[new_row][new_col]

            if target == EMPTY or is_opponent(piece, target):
                move_state = MoveState((row, col), (new_row, new_col), piece, target if target != EMPTY else None)
                moves.append(move_state)

        return moves
