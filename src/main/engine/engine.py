from typing import Any

from src.main.engine.stats import Stats
from src.main.engine.transposition_table import TTEntry
from src.main.gameplay.board_state import BoardState
from src.main.gameplay.move_generator import MoveGenerator
from src.main.gameplay.move_state import MoveState
from src.main.engine.evaluation import evaluate_board
from src.main.utils.constants import *


class Engine:
    def __init__(self, depth=5, engine_white_turn=False, use_quiescence=True):
        self.depth = depth
        self.q_depth = 3
        self.use_quiescence = use_quiescence
        self.engine_white_turn = engine_white_turn
        self.move_generator = MoveGenerator()
        self.transposition_table = {}
        self.tt_threshold = 200000
        self.stats = Stats()
        self.CHECK_MATE_SCORE = 1000000


    def engines_turn(self, board_state: BoardState) -> bool:
        return board_state.is_white_turn == self.engine_white_turn

    def trim_transposition_table(self, threshold):

        if len(self.transposition_table) >= threshold:
            # Sort items by depth (higher depth entries are more valuable)
            sorted_items = sorted(
                self.transposition_table.items(), 
                key=lambda x: x[1].depth,
                reverse=True
            )
            # Keep only the top half
            half_size = len(sorted_items) // 2
            self.transposition_table = dict(sorted_items[:half_size])
            # print(f"Trimmed transposition table from {len(sorted_items)} to {len(self.transposition_table)} entries")


    def play_move(self, board_state: BoardState) -> MoveState:
        # print(f"Transposition table size: {len(self.transposition_table)}")
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

        # Trim the transposition table after completing the search
        self.trim_transposition_table(self.tt_threshold)
        
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

        self.stats.nodes_visited += 1
        # main alpha-beta search
        if board_state.is_check_mate():
            score = self.CHECK_MATE_SCORE + depth
            return -score if is_maximizing_player else score

        if depth == 0:
            if self.use_quiescence:
                return self.quiescence_search(board_state, self.q_depth, alpha, beta, is_maximizing_player)
            else:
                return evaluate_board(board_state, self.engine_white_turn)



        possible_moves = self.gen_and_order_move(board_state)
        if not possible_moves:
            return 0  # Stale-mate


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
                'EXACT' if original_alpha < min_eval < original_beta else
                'UPPERBOUND' if min_eval <= original_alpha else
                'LOWERBOUND'
            )
            self.transposition_table[key] = TTEntry(min_eval, depth, flag, best_move)
            return min_eval




    def quiescence_search(self, board_state: BoardState, depth: int, alpha: float, beta: float, is_maximizing_player: bool) -> float:
        # Lookup position in transposition table
        key = hash(board_state)
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

        original_alpha = alpha
        original_beta = beta
        self.stats.q_nodes_visited += 1

        # Check terminal conditions
        if board_state.is_check_mate():
            score = self.CHECK_MATE_SCORE + depth
            return -score if is_maximizing_player else score

        # Stand-pat: Evaluate the current position
        stand_pat = evaluate_board(board_state, self.engine_white_turn)

        # Early cutoffs
        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat


        # Base case: reached max quiescence depth
        if depth <= 0:
            return stand_pat

        # Generate only capture moves for quiescence search
        possible_moves = self.move_generator.generate_capture_moves(board_state)
        possible_moves = self.move_ordering(possible_moves)

        if not possible_moves:
            return stand_pat  # No captures available


        best_move = None

        if is_maximizing_player:
            max_eval = stand_pat

            for move in possible_moves:
                board_state.make_move(move)
                eval = self.quiescence_search(board_state, depth - 1, alpha, beta, False)
                board_state.undo_move()

                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, max_eval)

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
            min_eval = stand_pat

            for move in possible_moves:
                board_state.make_move(move)
                eval = self.quiescence_search(board_state, depth - 1, alpha, beta, True)
                board_state.undo_move()

                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, min_eval)

                if beta <= alpha:
                    break  # Prune the search

            # Store in TT
            flag = (
                'EXACT' if original_alpha < min_eval < original_beta else
                'UPPERBOUND' if min_eval <= original_alpha else
                'LOWERBOUND'
            )
            self.transposition_table[key] = TTEntry(min_eval, depth, flag, best_move)

            return min_eval






    def move_ordering(self, moves: list[MoveState]) -> list[MoveState]:

        if not moves:
            return moves

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