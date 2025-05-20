from src.main.gameplay.board_state import BoardState
from src.main.gameplay.move_generator import MoveGenerator
from src.main.gameplay.move_state import MoveState
from src.main.utils.utils import is_white, is_black


class ChessGame:
    def __init__(self, engine=None, player_white_turn=True):
        self.board_state = BoardState()
        self.move_generator = MoveGenerator()
        self.engine = engine
        self.player_white_turn = player_white_turn
        # Temp variables
        self.selected_pos = None
        self.valid_moves = []


    def get_current_board(self):
        return self.board_state.board

    def get_turn(self):
        return self.board_state.is_white_turn

    def is_player_turn(self):
        return self.board_state.is_white_turn == self.player_white_turn

    def get_move_history(self):
        return self.board_state.move_history

    def get_last_move(self):
        return self.board_state.move_history[-1] if self.board_state.move_history else None

    def reset_temp(self):
        self.selected_pos = None
        self.valid_moves = []


    def initiate_move(self, pos):
        """Handle a click. Returns true if a any valid moves found, false otherwise.."""
        self.selected_pos = pos
        self.valid_moves = self.move_generator.generate_piece_moves(self.board_state,pos)
        if self.valid_moves:
            return True
        else:
            self.selected_pos = None # user can again initiate move
            self.valid_moves = []
            return False

    def apply_move(self, new_pos):
        """Attempt to make a move from selected_pos to to_pos.
           Returns true if valid move selected, false otherwise.
        """
        move = self.create_move(self.selected_pos, new_pos)
        print(move)

        self.selected_pos = None
        valid = move in self.valid_moves
        self.valid_moves = []

        if valid:
            self.board_state.make_move(move)
            return True
        return False

    # as soon as it is engine's turn
    def play_ai_move(self):
        """Call engine to play a move."""
        move = self.engine.play_move(self.board_state.copy())
        print(move)
        self.board_state.make_move(move)
        return move



    # if undo button clicked
    def undo_move(self):
        self.board_state.undo_move()


    # after move is made
    def is_game_over(self):
        return self.board_state.is_check_mate()

    def create_move(self, from_pos, to_pos):
        """
        Create a MoveState object representing a move from from_pos to to_pos
        using the current board_state.
        """
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        moved_piece = self.board_state.board[from_row][from_col]
        captured_piece = self.board_state.board[to_row][to_col]

        # Only pawns promote when reaching the last row (based on color)
        is_promoted = False
        if abs(moved_piece) == 1:
            if ((is_white(moved_piece) and to_row == 0) or
                    (is_black(moved_piece) and to_row == len(self.board_state.board) - 1)):
                is_promoted = True

        return MoveState(
            pre_pos=(from_row, from_col),
            new_pos=(to_row, to_col),
            moved_piece=moved_piece,
            captured_piece=captured_piece,
            is_promoted=is_promoted
        )


