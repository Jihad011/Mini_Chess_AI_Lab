import random

# Player
WHITE = 1
BLACK = -1

TOTAL_PIECE_COUNT = 20
EMPTY = 0
# White pieces
WHITE_PAWN = 1
WHITE_ROOK = 2
WHITE_KNIGHT = 3
WHITE_BISHOP = 4
WHITE_QUEEN = 5
WHITE_KING = 6

# Black pieces (negative of white)
BLACK_PAWN = -1
BLACK_ROOK = -2
BLACK_KNIGHT = -3
BLACK_BISHOP = -4
BLACK_QUEEN = -5
BLACK_KING = -6

# Optional maps for lookup
PIECE_SYMBOLS = {
    WHITE_PAWN: '♙', WHITE_ROOK: '♖', WHITE_KNIGHT: '♘', WHITE_BISHOP: '♗',
    WHITE_QUEEN: '♕', WHITE_KING: '♔',
    BLACK_PAWN: '♟', BLACK_ROOK: '♜', BLACK_KNIGHT: '♞', BLACK_BISHOP: '♝',
    BLACK_QUEEN: '♛', BLACK_KING: '♚',
}

# types and values are based on abs value
PIECE_TYPES = {
    1: 'PAWN', 2: 'ROOK', 3: 'KNIGHT', 4: 'BISHOP', 5: 'QUEEN', 6: 'KING'
}
PIECE_VALUES = {
    1: 100,     # Pawn
    2: 500,     # Rook
    3: 320,     # Knight
    4: 330,     # Bishop
    5: 900,     # Queen
    6: 20000,   # King
}


WHITE_PLAYER_PERSPECTIVE = [
    [BLACK_ROOK, BLACK_KNIGHT, BLACK_BISHOP, BLACK_QUEEN, BLACK_KING],
    [BLACK_PAWN] * 5,
    [EMPTY] * 5,
    [EMPTY] * 5,
    [WHITE_PAWN] * 5,
    [WHITE_ROOK, WHITE_KNIGHT, WHITE_BISHOP, WHITE_QUEEN, WHITE_KING],
]

BOARD_ROW = len(WHITE_PLAYER_PERSPECTIVE)
BOARD_COL = len(WHITE_PLAYER_PERSPECTIVE[0])

# WHITE_PLAYER_PERSPECTIVE = [
#     [BLACK_KING, EMPTY, EMPTY, EMPTY, EMPTY],
#     [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
#     [EMPTY, EMPTY, BLACK_BISHOP, EMPTY, EMPTY],
#     [EMPTY] * 5,
#     [EMPTY, BLACK_KNIGHT, EMPTY, EMPTY, EMPTY],
#     [EMPTY, EMPTY, EMPTY, WHITE_KING, EMPTY],
# ]

BLACK_PLAYER_PERSPECTIVE = [[row[::-1] for row in WHITE_PLAYER_PERSPECTIVE[::-1]]]




# Initialize Zobrist table (13 piece types including empty, 6 rows, 5 columns)
ZOBRIST_PIECE_SQUARE = [
    [[random.getrandbits(64) for _ in range(5)] for _ in range(6)]
    for _ in range(13)
]

ZOBRIST_TURN = random.getrandbits(64)

