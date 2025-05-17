
# Move optimization functions

def generate_knight_moves(rows=6, cols=5):
    """Generate a dictionary of precomputed knight moves for each board square."""
    knight_deltas = [
        (-2, -1), (-2, +1),
        (-1, -2), (-1, +2),
        (+1, -2), (+1, +2),
        (+2, -1), (+2, +1)
    ]

    moves_from = {}

    for r in range(rows):
        for c in range(cols):
            moves = []
            for dr, dc in knight_deltas:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    moves.append((nr, nc))
            moves_from[(r, c)] = moves

    return moves_from


def generate_king_moves(rows=6, cols=5):
    moves_from = {}
    for r in range(rows):
        for c in range(cols):
            moves = []
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 6 and 0 <= nc < 5:
                        moves.append((nr, nc))
            moves_from[(r, c)] = moves
    return moves_from