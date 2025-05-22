## ♟️ MiniChess

**MiniChess** is a compact chess variant played on a **5×6 board** (5 columns, 6 rows), designed for quick gameplay and experimenting with chess AI logic.

### 📏 Rules and Mechanics

- **No Castling**
- **No Double Pawn Move** (no en passant possible)
- **Only Queen Promotion**
- **King Capture Ends the Game** (no check/checkmate detection)

### 🕹️ Game Modes

- **Player vs Player**
- **Player vs AI (Engine)**

### 🧠 AI Engine Features

- **Minimax with Alpha-Beta Pruning**
- **Transposition Table** for board state caching
- **Move Ordering**:
  - Captures prioritized as using MVV-LVA
- **Basic Evaluation Function**
- **Quiescence search** for capture moves


## Requirements

- Python 3.13 or higher
- Required packages will be automatically installed in the steps below.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Jihad011/Mini_Chess_AI_Lab.git
   ```

2. Navigate to the project directory:
   ```
   cd Mini_Chess_AI_Lab
   ```

3. Set up a virtual environment (this will create a `venv/` folder in the project directory):
   ```
   python -m venv venv
   ```

4. Activate the virtual environment:

   - **On Windows (Command Prompt):**
     ```bash
     venv\Scripts\activate
     ```

   - **On Windows (PowerShell):**
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```

   - **On macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```


5. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## 🎮 Running the Game

To launch the MiniChess application, run:

```bash
   python app.py
