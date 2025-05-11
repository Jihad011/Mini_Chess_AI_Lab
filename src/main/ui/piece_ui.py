from PIL import Image, ImageTk
import tkinter as tk
from src.main.utils.ui_constants import PIECE_IMAGES

class PieceUI:
    def __init__(self, cell_size: int):
        self.cell_size = cell_size
        self.image_size = cell_size * 0.85
        self.piece_images = {}
        self.load_piece_images()

    def load_piece_images(self):
        """Load and resize all piece images maintaining transparency"""
        for piece_id, image_path in PIECE_IMAGES.items():
            # Load image with PIL and ensure it's RGBA
            original = Image.open(image_path).convert('RGBA')
            
            # Create a transparent background
            background = Image.new('RGBA', original.size, (0, 0, 0, 0))
            
            # Resize the image
            image_size = int(self.image_size)
            try:
                # For newer Pillow versions
                resized = original.resize((image_size, image_size), Image.Resampling.LANCZOS)
            except AttributeError:
                # For older Pillow versions
                resized = original.resize((image_size, image_size), Image.ANTIALIAS)

            # Composite the image onto the transparent background
            final_image = Image.alpha_composite(background.resize(resized.size), resized)
            
            # Convert to PhotoImage for Tkinter
            photo_image = ImageTk.PhotoImage(final_image)
            self.piece_images[piece_id] = photo_image

    def get_piece_image(self, piece_id: int) -> ImageTk.PhotoImage:
        return self.piece_images.get(piece_id)





    
    
    