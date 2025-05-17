from typing import Any

from src.main.engine.stats import Stats
from src.main.engine.transposition_table import TTEntry
from src.main.gameplay.board_state import BoardState
from src.main.gameplay.move_generator import MoveGenerator
from src.main.gameplay.move_state import MoveState
from src.main.engine.evaluation import evaluate_board
from src.main.utils.constants import *


class Engine:
    def __init__(self, depth=5, engine_white_turn=False):
        self.depth = depth
        self.engine_white_turn = engine_white_turn
        self.move_generator = MoveGenerator()
        self.transposition_table = {}
        self.stats = Stats()
        self.CHECK_MATE_SCORE = 1000000


    def engines_turn(self, board_state: BoardState) -> bool:
        return board_state.is_white_turn == self.engine_white_turn

    def play_move(self, board_state: BoardState) -> MoveState:

        self.stats.reset()
        best_move = None
        best_score = float('-inf')

        # Generate all possible moves for the current player
        possible_moves = self.gen_and_order_move(board_state)

        for move in possible_moves:

            board_state.make_move(move)
            score = self.alpha_beta(board_state, self.depth - 1, float('-inf'), float('inf'), False)
            board_state.undo_move()

            # Update the best move based on score
            if score > best_score:
                best_score = score
                best_move = move

        self.stats.evaluation = best_score
        print(f"Evaluation: {best_score}")
        return best_move



    def alpha_beta(self, board_state: BoardState, depth: int, alpha: float, beta: float, is_maximizing_player: bool) -> float | int | Any:
        original_alpha = alpha
        original_beta = beta
        key = hash(board_state)

        # Transposition table lookup
        entry = self.transposition_table.get(key)
        if entry and entry.depth >= depth:
            if entry.flag == 'EXACT':
                return entry.value
            elif entry.flag == 'LOWERBOUND':
                alpha = max(alpha, entry.value)
            elif entry.flag == 'UPPERBOUND':
                beta = min(beta, entry.value)
            if alpha >= beta:
                return entry.value

        # main alpha-beta search
        if board_state.is_check_mate():
            score = self.CHECK_MATE_SCORE + depth
            return -score if is_maximizing_player else score

        if depth == 0:
            return evaluate_board(board_state, self.engine_white_turn)



        possible_moves = self.gen_and_order_move(board_state)
        if not possible_moves:
            return 0  # Stale-mate

        self.stats.nodes_visited += 1
        if is_maximizing_player:
            max_eval = float('-inf')
            best_move = None

            for move in possible_moves:
                board_state.make_move(move)
                eval = self.alpha_beta(board_state, depth - 1, alpha, beta, False)  # Minimize for the opponent
                board_state.undo_move()

                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)

                if beta <= alpha:
                    break  # Prune the search

            # Store in TT
            flag = (
                'EXACT' if original_alpha < max_eval < original_beta else
                'LOWERBOUND' if max_eval >= original_beta else
                'UPPERBOUND'
            )
            self.transposition_table[key] = TTEntry(max_eval, depth, flag, best_move)

            return max_eval
        else:
            min_eval = float('inf')
            best_move = None

            for move in possible_moves:
                board_state.make_move(move)
                eval = self.alpha_beta(board_state, depth - 1, alpha, beta, True)  # Maximize for the player
                board_state.undo_move()

                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)

                if beta <= alpha:
                    break  # Prune the search


            # Store in TT
            flag = (
                'EXACT' if alpha < min_eval < original_beta else
                'UPPERBOUND' if min_eval <= alpha else
                'LOWERBOUND'
            )
            self.transposition_table[key] = TTEntry(min_eval, depth, flag, best_move)
            return min_eval



    def move_ordering(self, moves: list[MoveState]) -> list[MoveState]:
        def move_score(move: MoveState) -> int:
            score = 0
            if move.captured_piece:
                # MVV-LVA (Most Valuable Victim - Least Valuable Attacker)
                captured_value = PIECE_VALUES.get(abs(move.captured_piece), 0)
                attacker_value = PIECE_VALUES.get(abs(move.moved_piece), 0)
                score += captured_value * 10 - attacker_value

            return score

        return sorted(moves, key=move_score, reverse=True)



    def gen_and_order_move(self, board_state: BoardState) -> list[MoveState]:
        possible_moves = self.move_generator.generate_all_moves(board_state)
        possible_moves = self.move_ordering(possible_moves)
        return possible_moves