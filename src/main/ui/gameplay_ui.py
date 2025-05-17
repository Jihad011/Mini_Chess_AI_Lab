from src.main.engine.engine import Engine
from src.main.gameplay.chess_game import ChessGame
from src.main.ui.chess_board import ChessBoardUI
from src.main.ui.ui_components import UIComponents
from src.main.utils.ui_constants import GREEN_BOARD
from src.main.utils.utils import is_ai_turn
import tkinter as tk


class GamePlayUI:
    def __init__(self, root, player_white_turn, is_play_with_ai, depth, return_to_menu_callback=None, board_color=GREEN_BOARD):
        self.root = root
        self.player_white_turn = player_white_turn
        self.is_play_with_ai = is_play_with_ai
        self.board_color = board_color
        self.isGameOver = False
        self.game_over_msg = None
        self.status_label = None
        print(self.player_white_turn, self.is_play_with_ai)
        self.return_to_menu_callback = return_to_menu_callback
        self.engine = Engine(depth, not self.player_white_turn)
        self.chess_game = ChessGame(self.engine, self.player_white_turn)
        self.ui = UIComponents()

        # Create main container frame
        self.main_frame = self.ui.create_frame(self.root)
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Create a frame for the chess board
        self.board_frame = self.ui.create_frame(self.main_frame)
        self.board_frame.grid(row=0, column=0, padx=(0, 20))

        # Create chess board ui
        self.chess_board_ui = ChessBoardUI(
            self.board_frame,
            self.on_click_board,
            self.chess_game.get_current_board(),
            cell_size=65,
            board_color=self.board_color
        )

        # Create control frame (on the right)
        self.control_frame = self.ui.create_frame(self.main_frame)
        self.control_frame.grid(row=0, column=1, sticky='n')
        
        # Add the controls
        self.add_controls()

        # Engine move first
        if is_ai_turn(self.is_play_with_ai, self.player_white_turn):
            self.root.after(1000, self.on_engine_move)



    def restart_game(self):

        self.restart_game_over()
        self.engine = Engine(self.engine.depth, not self.player_white_turn)
        self.chess_game = ChessGame(self.engine, self.player_white_turn)
        # Clear old chess board UI widgets
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        # Create chess board ui
        self.chess_board_ui = ChessBoardUI(
            self.board_frame,
            self.on_click_board,
            self.chess_game.get_current_board(),
            cell_size=65,
            board_color=self.board_color
        )

        # Engine move first
        if is_ai_turn(self.is_play_with_ai, self.player_white_turn):
            self.root.after(1000, self.on_engine_move)

        
    def add_controls(self):
        # Title for controls section
        control_title = self.ui.create_title_label(
            self.control_frame,
            "Game Controls",
            font_size=18,
            pady=10
        )
        control_title.pack(pady=(0, 20))

        # Restart button with secondary color
        restart_btn = self.ui.create_button(
            self.control_frame,
            "Restart Game",
            self.restart_game,
            width=15,
            bg=UIComponents.COLORS['secondary'],
            activebackground=UIComponents.COLORS['primary']
        )
        restart_btn.pack(pady=10)

        # Undo button with primary color
        undo_btn = self.ui.create_button(
            self.control_frame,
            "Undo Move",
            self.undo_move,
            width=15,
            bg=UIComponents.COLORS['primary'],
            activebackground=UIComponents.COLORS['secondary']
        )
        undo_btn.pack(pady=10)

        # Main menu button with a different style
        menu_btn = self.ui.create_button(
            self.control_frame,
            "Main Menu",
            self.return_to_menu,
            width=15,
            bg=UIComponents.COLORS['accent'],
            activebackground=UIComponents.COLORS['button_hover']
        )
        menu_btn.pack(pady=10)
        
        # Game status label
        self.status_label = tk.Label(
            self.control_frame,
            text="",
            font=("Helvetica", 12, "bold"),
            fg=UIComponents.COLORS['text'],
            bg=UIComponents.COLORS['background'],
            wraplength=150,  # Wrap text if it's too long
            justify=tk.CENTER
        )
        self.status_label.pack(pady=(20, 0))



    def undo_move(self):
        # Implement undo move logic
        print("Undoing move...")

    def return_to_menu(self):
        if self.return_to_menu_callback:
            # Reset game state
            self.chess_game = None
            self.engine = None
            self.chess_board_ui = None
            self.restart_game_over()
            for widget in self.root.winfo_children():
                widget.destroy()

            self.return_to_menu_callback()




    def on_click_board(self, row, col):

        if self.chess_game.is_game_over():
            print("Game Over")
            return


        if self.is_play_with_ai and self.chess_game.is_player_turn():
            self.on_player_move(row, col)
        if not self.is_play_with_ai:
            self.on_player_move(row, col)





    def on_player_move(self, row, col):

        # First click
        if not self.chess_game.selected_pos:
            if self.chess_game.initiate_move((row, col)):
                self.chess_board_ui.highlight_cell(self.chess_game.valid_moves)

        # Second click
        else:
            self.chess_board_ui.remove_highlight()
            if self.chess_game.apply_move((row, col)):
                print('Move applied')
                print(self.chess_game.board_state.print_board())
                self.chess_board_ui.clear_prev_piece()
                self.chess_board_ui.draw_piece(row, col, self.chess_game.board_state.board[row][col])
                if self.chess_game.is_game_over():
                    turn = self.chess_game.get_turn()
                    self.init_game_over(turn)
                    print("Game Over - ", "black" if turn else "white", " wins")
                    return

                if self.is_play_with_ai:
                    self.on_engine_move()



    def on_engine_move(self):

        if self.chess_game is None:
            return

        move = self.chess_game.play_ai_move()
        self.chess_board_ui.clear_piece(move.pre_pos[0], move.pre_pos[1])
        self.chess_board_ui.draw_piece(move.new_pos[0], move.new_pos[1], self.chess_game.board_state.board[move.new_pos[0]][move.new_pos[1]])
        print(self.chess_game.board_state.print_board())
        if self.chess_game.is_game_over():
            turn = self.chess_game.get_turn()
            self.init_game_over(turn)
            print("Game Over - ", "black" if turn else "white", " wins")
            return


    def init_game_over(self, turn):
        self.isGameOver = True
        winner = "Black" if turn else "White"
        self.game_over_msg = f"Game Over - {winner} wins!"
        
        # Update the status label with game over message
        if hasattr(self, 'status_label'):
            self.status_label.config(
                text=self.game_over_msg,
                fg=UIComponents.COLORS['danger']
            )
        
    def restart_game_over(self):
        self.isGameOver = False
        self.game_over_msg = None
        
        # Clear the status label
        if hasattr(self, 'status_label'):
            self.status_label.config(
                text="",
                fg=UIComponents.COLORS['text']
            )