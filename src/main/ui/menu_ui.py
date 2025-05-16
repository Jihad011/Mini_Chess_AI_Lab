import tkinter as tk
from tkinter import PhotoImage
from src.main.ui.gameplay_ui import GamePlayUI
from src.main.ui.ui_components import UIComponents
from src.main.utils.ui_constants import APP_ICON_PATH


class MenuUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MiniChess")
        self.root.geometry("600x450")
        self.root.resizable(False, False)
        self.root.iconphoto(False, PhotoImage(file=APP_ICON_PATH))
        self.root.configure(bg=UIComponents.COLORS['background'])
        
        # UI Components handler
        self.ui = UIComponents()

        # Settings variables
        self.player_white_turn = False
        self.is_play_with_ai = False
        self.depth = 6

        self.menu_widgets = []
        self.build_menu()

        self.root.mainloop()

    def build_menu(self):
        # Clear previous widgets if any
        for w in self.menu_widgets:
            w.destroy()
        self.menu_widgets.clear()

        # Create main frame
        main_frame = self.ui.create_frame(self.root)
        main_frame.pack(expand=True, fill='both', padx=40, pady=40)
        self.menu_widgets.append(main_frame)

        # Create title label
        label = self.ui.create_title_label(
            main_frame, 
            "Mini Chess",
            pady=20
        )
        label.pack(pady=(0, 30))
        self.menu_widgets.append(label)

        # Settings frame
        settings_frame = self.ui.create_frame(main_frame)
        settings_frame.pack(fill='x', padx=20, pady=(0, 30))
        self.menu_widgets.append(settings_frame)

        # Checkbox for player color
        def update_player_white_turn(val: bool):
            self.player_white_turn = val

        color_cb, color_var = self.ui.create_checkbox(
            settings_frame,
            "Play as White",
            self.player_white_turn,
            command=lambda: update_player_white_turn(color_var.get())
        )

        color_cb.pack(pady=5)
        self.menu_widgets.append(color_cb)

        # Checkbox for play with AI
        def update_ai_enabled(val: bool):
            self.is_play_with_ai = val

        ai_cb, ai_var = self.ui.create_checkbox(
            settings_frame,
            "Play with AI",
            self.is_play_with_ai,
            command=lambda: update_ai_enabled(ai_var.get())
        )
        ai_cb.pack(pady=5)
        self.menu_widgets.append(ai_cb)

        # Create button frame for multiple buttons
        button_frame = self.ui.create_frame(main_frame)
        button_frame.pack(pady=20)
        self.menu_widgets.append(button_frame)

        # Start game button
        start_btn = self.ui.create_button(
            button_frame,
            "Start Game",
            self.start_game,
            width=15
        )
        start_btn.pack(side=tk.LEFT, padx=10)
        self.menu_widgets.append(start_btn)

        # Exit button using the existing create_button with danger colors
        exit_btn = self.ui.create_button(
            button_frame,
            "Exit",
            self.root.quit,
            width=15,
            bg=UIComponents.COLORS['danger'],
            activebackground=UIComponents.COLORS['danger_hover']
        )
        exit_btn.pack(side=tk.LEFT, padx=10)
        self.menu_widgets.append(exit_btn)



    def start_game(self):
        # Clear menu widgets before launching gameplay UI
        for w in self.menu_widgets:
            w.destroy()
        self.menu_widgets.clear()

        # Create gameplay UI
        print("Starting game...")
        self.gameplay_ui = GamePlayUI(
            root=self.root,
            player_white_turn=self.player_white_turn,
            is_play_with_ai=self.is_play_with_ai,
            depth=self.depth,
            return_to_menu_callback=self.show_menu
        )

    def show_menu(self):
        self.build_menu()

if __name__ == "__main__":
    menu_ui = MenuUI()