import copy

from src.main.utils.constants import *
from .move_state import MoveState



# board_state state assumes board_state in white player perspective
# needs board_state flipping in the ui
class BoardState:
    def __init__(self, is_white_turn=True):
        self.board = copy.deepcopy(WHITE_PLAYER_PERSPECTIVE)
        self.is_white_turn = is_white_turn
        self.move_history = []
        self._hash = None  # Cache for the hash value

    def __hash__(self):
        if self._hash is not None:
            return self._hash
            
        h = 0
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                piece = self.board[row][col]
                if piece != EMPTY:
                    # Use piece type, position, and color to generate hash
                    h ^= self._zobrist_hash(piece, row, col)
    
        # Include turn in the hash
        if self.is_white_turn:
            h ^= self._zobrist_turn_hash()
        
        self._hash = h
        return h

    def _zobrist_hash(self, piece: int, row: int, col: int) -> int:
        return ZOBRIST_PIECE_SQUARE[piece + 6][row][col]  # +6 to make negative indices positive

    def _zobrist_turn_hash(self) -> int:
        return ZOBRIST_TURN
    
    

    def print_board(self):
        for row in self.board:
            print(' '.join(PIECE_SYMBOLS.get(cell, '.') for cell in row))
            
    def copy(self):
        new_state = BoardState(self.is_white_turn)
        new_state.board = [[cell for cell in row] for row in self.board]
        new_state.move_history = [move.copy() for move in self.move_history]
        return new_state
    

    def make_move(self, move: MoveState):
        pre_row, pre_col = move.pre_pos
        new_row, new_col = move.new_pos

        # Move the piece
        self.board[new_row][new_col] = move.moved_piece
        self.board[pre_row][pre_col] = EMPTY

        # Handle promotion
        if move.is_promoted:
            if self.is_white_turn:
                self.board[new_row][new_col] = WHITE_QUEEN
            else:
                self.board[new_row][new_col] = BLACK_QUEEN

        # Save the move to history
        self.move_history.append(move)

        # Switch turn and update hash
        self.is_white_turn = not self.is_white_turn
        self._hash = self._update_hash_for_move(move)

    def undo_move(self):
        if not self.move_history:
            return

        last_move = self.move_history.pop()
        pre_row, pre_col = last_move.pre_pos
        new_row, new_col = last_move.new_pos

        # Update hash before board changes
        self._hash = self._update_hash_for_undo(last_move)

        # Also handles pawn promotion (moved_piece will be pawn even for promotion)
        self.board[pre_row][pre_col] = last_move.moved_piece

        # Restore captured piece or empty
        if last_move.captured_piece:
            self.board[new_row][new_col] = last_move.captured_piece
        else:
            self.board[new_row][new_col] = EMPTY

        # Switch turn back
        self.is_white_turn = not self.is_white_turn


    # Needs to check after make_move
    def is_check_mate(self):

        last_move = self.move_history[-1] if self.move_history else None

        if not last_move:
            return False

        # If the last move captured the king, it's checkmate
        captured_piece = last_move.captured_piece
        if captured_piece == WHITE_KING or captured_piece == BLACK_KING:
            return True

        return False

    def _update_hash_for_move(self, move: MoveState) -> int:
        """Updates hash value for making a move"""
        if self._hash is None:
            return self.__hash__()
            
        h = self._hash
        pre_row, pre_col = move.pre_pos
        new_row, new_col = move.new_pos

        # Remove piece from original position
        h ^= self._zobrist_hash(move.moved_piece, pre_row, pre_col)
        
        # Handle captured piece if exists
        if move.captured_piece:
            h ^= self._zobrist_hash(move.captured_piece, new_row, new_col)
        
        # Add piece to new position (handle promotion)
        piece_to_add = move.moved_piece
        if move.is_promoted:
            piece_to_add = WHITE_QUEEN if self.is_white_turn else BLACK_QUEEN
        h ^= self._zobrist_hash(piece_to_add, new_row, new_col)
        
        # Toggle turn
        h ^= self._zobrist_turn_hash()
        
        return h

    def _update_hash_for_undo(self, move: MoveState) -> int:
        """Updates hash value for undoing a move"""
        if self._hash is None:
            return self.__hash__()
            
        h = self._hash
        pre_row, pre_col = move.pre_pos
        new_row, new_col = move.new_pos

        # Remove piece from current position (might be promoted)
        current_piece = self.board[new_row][new_col]
        h ^= self._zobrist_hash(current_piece, new_row, new_col)
        
        # Add piece back to original position
        h ^= self._zobrist_hash(move.moved_piece, pre_row, pre_col)
        
        # Add back captured piece if any
        if move.captured_piece:
            h ^= self._zobrist_hash(move.captured_piece, new_row, new_col)
            
        # Toggle turn back
        h ^= self._zobrist_turn_hash()
        
        return h