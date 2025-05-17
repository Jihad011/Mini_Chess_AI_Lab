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

    @staticmethod
    def create_radio_group(
        parent: tk.Tk | tk.Frame,
        options: Dict[str, Any],
        initial_value: Any,
        command: Callable[[Any], None],
        title: Optional[str] = None,
        orientation: str = "vertical",  # "vertical" or "horizontal"
        **kwargs
    ) -> Tuple[tk.Frame, tk.StringVar]:
        """Creates a group of radio buttons
        
        Args:
            parent: Parent widget
            options: Dictionary of {display_text: value}
            initial_value: Initial selected value
            command: Function to call when selection changes
            title: Optional title for the group
            orientation: "vertical" or "horizontal" layout
        
        Returns:
            Tuple of (container frame, StringVar with selected value)
        """
        # Create container frame
        container = UIComponents.create_frame(parent, **kwargs)
        
        # Add title if provided
        if title:
            title_label = tk.Label(
                container,
                text=title,
                font=("Helvetica", 12, "bold"),
                fg=UIComponents.COLORS['text'],
                bg=UIComponents.COLORS['background'],
            )
            title_label.pack(pady=(0, 5))
        
        # Find the key for the initial value in options
        initial_key = None
        for key, value in options.items():
            if value == initial_value:
                initial_key = key
                break
        
        # Create variable to track selection
        var = tk.StringVar(value=initial_key)
        
        # Create a radio button frame
        radio_frame = UIComponents.create_frame(container)
        radio_frame.pack(pady=5)
        
        # Create radio buttons
        for text, value in options.items():
            radio = tk.Radiobutton(
                radio_frame,
                text=text,
                value=text,  # Use text as value for the radio button
                variable=var,
                command=lambda: command(options[var.get()]),  # Convert back to actual value
                font=("Helvetica", 11),
                fg=UIComponents.COLORS['checkbox_fg'],
                bg=UIComponents.COLORS['background'],
                activebackground=UIComponents.COLORS['secondary'],
                activeforeground=UIComponents.COLORS['text'],
                selectcolor=UIComponents.COLORS['checkbox_bg'],
            )
            if orientation == "vertical":
                radio.pack(anchor="center", pady=3)
            else:
                radio.pack(side=tk.LEFT, padx=10)
        
        return container, var