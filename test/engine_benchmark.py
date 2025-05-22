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

def benchmark_engine_vs_engine(max_moves=50, depth=4, e1_quiescence=False, e2_quiescence=False):
    # Create two engines with different colors
    engine_white = Engine(depth, engine_white_turn=True, use_quiescence=e1_quiescence)
    engine_black = Engine(depth, engine_white_turn=False, use_quiescence=e2_quiescence)
    
    # Initialize game
    chess_game = ChessGame(engine=None)
    # chess_game.board_state.board = TEST_BOARD
    move_count = 0
    total_node_visited = 0
    total_q_node_visited = 0
    
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
        total_node_visited += engine_white.stats.nodes_visited + engine_black.stats.nodes_visited
        total_q_node_visited += engine_white.stats.q_nodes_visited + engine_black.stats.q_nodes_visited

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
    print(f"Nodes Visited: {total_node_visited} + {total_q_node_visited} = {total_node_visited + total_q_node_visited}")
    print(f"Average nodes visited per move: {(total_node_visited + total_q_node_visited) / move_count:.2f}")
    print("\nWhite engine last move stats:")
    print(engine_white.stats)
    print("\nBlack engine last move stats:")
    print(engine_black.stats)

if __name__ == "__main__":
    benchmark_engine_vs_engine(max_moves=20, depth=5, e1_quiescence=True, e2_quiescence=True)

# True False

# 20 move game

# depth = 3
# Total time: 0.182625 seconds
# Average time per move: 0.009131 seconds
# Nodes Visited: 15294 + 0 = 15294
# Average nodes visited per move: 764.70


# depth = 3 (quiescence)
# Total time: 0.921213 seconds
# Average time per move: 0.046061 seconds
# Nodes Visited: 17940 + 42028 = 59968
# Average nodes visited per move: 2998.40


# depth = 4
# Total time: 1.733805 seconds
# Average time per move: 0.086690 seconds
# Nodes Visited: 155104 + 0 = 155104
# Average nodes visited per move: 7755.20


# depth = 4 (quiescence)
# Total time: 5.261580 seconds
# Average time per move: 0.263079 seconds
# Nodes Visited: 223009 + 327329 = 550338
# Average nodes visited per move: 27516.90


# depth = 5
# Total time: 5.334207 seconds
# Average time per move: 0.266710 seconds
# Nodes Visited: 471815 + 0 = 471815
# Average nodes visited per move: 23590.75


# depth = 5 (quiescence)
# Total time: 10.887982 seconds
# Average time per move: 0.544399 seconds
# Nodes Visited: 328786 + 554963 = 883749
# Average nodes visited per move: 44187.45


# depth = 6
# Total time: 21.239188 seconds
# Average time per move: 1.061959 seconds
# Nodes Visited: 1987738 + 0 = 1987738
# Average nodes visited per move: 99386.90


# depth = 6 (quiescence)
# Total time: 66.851335 seconds
# Average time per move: 3.342567 seconds
# Nodes Visited: 2582871 + 4064699 = 6647570
# Average nodes visited per move: 332378.50


# normal vs q engine stats

# White engine last move stats:
# Nodes Visited: 16355
# Q Nodes Visited: 0
# Evaluation: -150.00
#
# Black engine last move stats: Q
# Nodes Visited: 17733
# Q Nodes Visited: 19380
# Evaluation: 745.00

# White engine last move stats: Q
# Nodes Visited: 12937
# Q Nodes Visited: 23119
# Evaluation: 615.00
#
# Black engine last move stats:
# Nodes Visited: 5282
# Q Nodes Visited: 0
# Evaluation: -460.00