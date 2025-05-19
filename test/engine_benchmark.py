import time
from src.main.utils.constants import *
from src.main.engine.engine import Engine
from src.main.gameplay.board_state import BoardState
from src.main.gameplay.chess_game import ChessGame


TEST_BOARD = [
    [BLACK_KING, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY] * 5,
    [EMPTY, BLACK_KNIGHT, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, WHITE_KING, EMPTY],
]

def benchmark_engine_vs_engine(max_moves=50, depth=5):
    # Create two engines with different colors
    engine_white = Engine(depth, engine_white_turn=True)
    engine_black = Engine(depth, engine_white_turn=False)
    
    # Initialize game
    chess_game = ChessGame(engine=None)
    # chess_game.board_state.board = TEST_BOARD
    move_count = 0
    
    print("Starting engine vs engine game...")
    print(chess_game.board_state.print_board())
    
    start_time = time.time()
    
    while move_count < max_moves:
        # White's turn
        if chess_game.get_turn():
            move = engine_white.play_move(chess_game.board_state.copy())
        # Black's turn
        else:
            move = engine_black.play_move(chess_game.board_state.copy())
            
        # Make the move
        chess_game.board_state.make_move(move)
        move_count += 1
        
        print(f"\nMove {move_count}: {move}")
        print(chess_game.board_state.print_board())
        
        # Check for checkmate
        if chess_game.is_game_over():
            winner = "Black" if chess_game.get_turn() else "White"
            print(f"\nCheckmate! {winner} wins in {move_count} moves!")
            break
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\nGame Statistics:")
    print(f"Total moves: {move_count}")
    print(f"Total time: {total_time:.6f} seconds")
    print(f"Average time per move: {total_time/move_count:.6f} seconds")
    print("\nWhite engine stats:")
    print(engine_white.stats)
    print("\nBlack engine stats:")
    print(engine_black.stats)

if __name__ == "__main__":
    benchmark_engine_vs_engine(max_moves=10, depth=5)



# 20 move game

# depth = 5
# Total time: 5.480119 seconds
# Average time per move: 0.274006 seconds
# Nodes Visited: 7625 + 7877 = 15502


# depth = 6
# Total time: 17.570615 seconds
# Average time per move: 0.878531 seconds
# Nodes Visited: 16607 + 20789


# depth = 7
# Total time: 136.012213 seconds
# Average time per move: 6.800611 seconds
# Nodes Visited: 194355 + 286565
