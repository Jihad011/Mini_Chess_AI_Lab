import tkinter as tk
from src.main.gameplay.move_state import MoveState
from src.main.utils.constants import EMPTY
from src.main.utils.ui_constants import *
from src.main.ui.piece_ui import PieceUI

class ChessBoardUI:
    def __init__(self, parent, on_click, board, rows: int = 6, cols: int = 5, cell_size: int = 65, color: int = GRAY):
        self.parent = parent
        self.on_click = on_click
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.board_color = GREEN_BOARD
        # Temp variables
        self.cells = {}
        self.pieces = {}
        self.highlighted_cells = []
        self.last_clicked_cell = None
        # Initialize PieceUI
        self.piece_ui = PieceUI(cell_size)
        self.create_board()
        self.add_pieces(board)
        self.add_hover_effect()

    def create_board(self):
        """Create the visual chess board_state"""
        for row in range(self.rows):
            for col in range(self.cols):

                color = self.board_color["LIGHT"] if (row + col) % 2 == 0 else self.board_color["DARK"]
                cell = tk.Canvas(self.parent,
                                 width=self.cell_size,
                                 height=self.cell_size,
                                 bg=color,
                                 highlightthickness=0)
                cell.grid(row=row, column=col)
                self.cells[(row, col)] = cell

                # Bind click events
                cell.bind('<Button-1>', lambda e, r=row, c=col: self.on_cell_click(r, c))


    def add_pieces(self, board):
        """Add pieces to the board_state"""
        for row in range(self.rows):
            for col in range(self.cols):
                piece = board[row][col]
                if piece != EMPTY:
                    self.draw_piece(row, col, piece)


    def on_cell_click(self, row: int, col: int):
        """Propagate to main ui"""
        self.on_click(row, col)
        self.last_clicked_cell = (row, col)

    def draw_piece(self, row: int, col: int, piece: int):
        """Draw a piece on the board_state"""
        if (row, col) in self.pieces:
            self.clear_piece(row, col)

        # Get the canvas for this cell
        canvas = self.cells[(row, col)]

        # Set the canvas background FIRST
        canvas.configure(bg=self.get_cell_color(row, col))

        # Get the piece image from PieceUI
        piece_image = self.piece_ui.get_piece_image(piece)
        if piece_image:
            # Calculate center position
            x = self.cell_size // 2
            y = self.cell_size // 2

            # Create image on canvas and store its ID
            piece_id = canvas.create_image(x, y, image=piece_image, anchor='center')
            self.pieces[(row, col)] = (piece_id, piece_image)  # Store both ID and image reference

            # Ensure the canvas is updated properly
            canvas.update_idletasks()


    def clear_prev_piece(self):
        """Remove the pre pos piece from the board_state"""
        if not self.last_clicked_cell:
            return
        row, col = self.last_clicked_cell
        self.clear_piece(row, col)



    # after move ( pre pos )
    def clear_piece(self, row: int, col: int):
        """Remove a piece from the board_state"""
        if (row, col) in self.pieces:
            canvas = self.cells[(row, col)]
            canvas.delete(self.pieces[(row, col)][0])
            del self.pieces[(row, col)]


    def highlight_cell(self, moves: list[MoveState], color: str = 'yellow'):
        """Highlight a cell to show possible moves"""
        for move in moves:
            row, col = move.new_pos
            self.cells[(row, col)].config(bg=color)
            self.highlighted_cells.append((row, col))

    def remove_highlight(self):
        """Remove all highlights"""
        for position, cell in self.cells.items():
            row, col = position
            color = self.get_cell_color(row, col)
            cell.config(bg=color)
        self.highlighted_cells = []

    def get_cell_color(self, row: int, col: int) -> str:
        """Get the original color for a cell based on its position"""
        return self.board_color["LIGHT"] if (row + col) % 2 == 0 else self.board_color["DARK"]

    def add_hover_effect(self):
        """Add hover effect to all cells"""
        for position, cell in self.cells.items():
            row, col = position
            original_color = self.get_cell_color(row, col)
            # Bind events with correct variable capturing
            cell.bind('<Enter>', 
                     lambda event, canvas=cell, color=original_color: 
                     self.on_hover_enter(canvas, color))
            cell.bind('<Leave>', 
                     lambda event, canvas=cell, r=row, c=col: 
                     self.on_hover_leave(canvas, r, c))

    def on_hover_enter(self, cell: tk.Canvas, original_color: str):
        """Handle mouse enter event"""
        # Skip hovering if the cell is highlighted
        if cell in [self.cells[pos] for pos in self.highlighted_cells]:
            return
        
        # Convert hex to RGB, lighten it, and convert back to hex
        rgb = tuple(int(original_color[i:i+2], 16) for i in (1, 3, 5))
        lightened_rgb = tuple(min(255, int(x + 20)) for x in rgb)  # Lighten by adding 20
        lightened_color = f'#{lightened_rgb[0]:02x}{lightened_rgb[1]:02x}{lightened_rgb[2]:02x}'
        cell.configure(bg=lightened_color)

    def on_hover_leave(self, cell: tk.Canvas, row: int, col: int):
        """Handle mouse leave event"""
        # Skip hovering if the cell is highlighted
        if (row, col) in self.highlighted_cells:
            return
        
        original_color = self.get_cell_color(row, col)
        cell.configure(bg=original_color)

    def reset_colors(self):
        """Reset all cells to their original colors"""
        for position, cell in self.cells.items():
            row, col = position
            color = self.get_cell_color(row, col)
            cell.config(bg=color)