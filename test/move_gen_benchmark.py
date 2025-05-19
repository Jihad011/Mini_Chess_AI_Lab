import time

from src.main.engine.evaluation import evaluate_board
from src.main.gameplay.board_state import BoardState
from src.main.gameplay.move_generator import MoveGenerator

def benchmark_move_generation(runs=100000):
    board_state = BoardState(True)
    move_generator = MoveGenerator()


    start = time.time()

    total_moves = 0
    total_eval = 0
    for _ in range(runs):
        moves = move_generator.generate_all_moves(board_state)
        total_moves += len(moves)
        total_eval += evaluate_board(board_state, True)

    end = time.time()
    duration = end - start

    print(f"Benchmark: {runs} runs")
    print(f"Total moves generated: {total_moves}")
    print(f"Time taken: {duration:.4f} seconds")
    print(f"Moves per second: {total_moves / duration:.2f}")
    print(f"Total evaluation value(must be 0): {total_eval}")

if __name__ == "__main__":
    benchmark_move_generation()


# Time taken: 3.3296 seconds
# Moves per second: 210237.23