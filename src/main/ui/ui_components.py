import tkinter as tk
from typing import Callable, Any, Optional, Dict, Tuple

class UIComponents:
    # Color scheme
    COLORS = {
        'primary': '#2C3E50',  # Dark blue-gray
        'secondary': '#34495E',  # Lighter blue-gray
        'accent': '#3498DB',  # Bright blue
        'text': '#ECF0F1',  # Light gray
        'background': '#1A1A1A',  # Dark background
        'button_hover': '#2980B9',  # Darker blue for hover
        'checkbox_bg': '#2C3E50',  # Dark blue-gray for checkbox
        'checkbox_fg': '#ECF0F1',  # Light gray for checkbox text
        'danger': '#E74C3C',  # Red for exit button
        'danger_hover': '#C0392B',  # Darker red for hover
    }

    @staticmethod
    def create_title_label(
        parent: tk.Tk | tk.Frame, 
        text: str, 
        font_size: int = 24,  # Increased font size
        font_family: str = "Helvetica",  # Modern font
        **kwargs
    ) -> tk.Label:
        """Creates a modern-looking title label"""
        label = tk.Label(
            parent,
            text=text,
            font=(font_family, font_size, "bold"),  # Added bold
            fg=UIComponents.COLORS['text'],
            bg=UIComponents.COLORS['background'],
            **kwargs
        )
        return label

    @staticmethod
    def create_checkbox(
        parent: tk.Tk | tk.Frame,
        text: str,
        initial_value: bool,
        command: Callable[[], None],
        **kwargs
    ) -> Tuple[tk.Checkbutton, tk.BooleanVar]:
        """Creates a modern-looking checkbox"""
        var = tk.BooleanVar(value=initial_value)
        checkbox = tk.Checkbutton(
            parent,
            text=text,
            variable=var,
            command=command,
            font=("Helvetica", 12),
            fg=UIComponents.COLORS['checkbox_fg'],
            bg=UIComponents.COLORS['background'],
            activebackground=UIComponents.COLORS['secondary'],
            activeforeground=UIComponents.COLORS['text'],
            selectcolor=UIComponents.COLORS['checkbox_bg'],
            **kwargs
        )
        return checkbox, var

    @staticmethod
    def create_button(
        parent: tk.Tk | tk.Frame,
        text: str,
        command: Callable[[], None],
        width: Optional[int] = None,
        height: Optional[int] = None,
        bg: Optional[str] = COLORS['accent'],
        fg: Optional[str] = COLORS['text'],
        activebackground: Optional[str] = COLORS['button_hover'],
        activeforeground: Optional[str] = COLORS['text'],
        **kwargs
    ) -> tk.Button:
        """Creates a modern-looking button"""
        button = tk.Button(
            parent,
            text=text,
            command=command,
            width=width,
            height=height,
            font=("Helvetica", 12, "bold"),
            bg=bg,
            fg=fg,
            activebackground=activebackground,
            activeforeground=activeforeground,
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            **kwargs
        )
        
        # Hover effect
        def on_enter(e):
            button['background'] = activebackground

        
        def on_leave(e):
            button['background'] = bg
            
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        return button

    @staticmethod
    def create_frame(
        parent: tk.Tk | tk.Frame,
        **kwargs
    ) -> tk.Frame:
        """Creates a styled frame"""
        frame = tk.Frame(
            parent,
            bg=UIComponents.COLORS['background'],
            **kwargs
        )
        return frame