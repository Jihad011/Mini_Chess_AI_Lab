from src.main.utils.constants import *

# Position bonus maps (white perspective)
PAWN_POSITION_BONUS = [
    [80, 80, 80, 80, 80],
    [50, 50, 50, 50, 50],
    [30, 30, 40, 30, 30],
    [20, 20, 30, 20, 20],
    [10, 10, 20, 10, 10],
    [0,  0,  0,  0,  0]
]

KNIGHT_POSITION_BONUS = [
    [-20, -10,  0, -10, -20],
    [-10,  0,  10,  0, -10],
    [0,   10,  20, 10,  0],
    [0,   10,  20, 10,  0],
    [-10,  0,  10,  0, -10],
    [-20, -10,  0, -10, -20]
]

BISHOP_POSITION_BONUS = [
    [ 0, -5,  0, -5, 10],
    [-5,  0,  0,  0, -5],
    [ 0, 10, 15, 10,  0],
    [ 0, 10, 15, 10,  0],
    [10, 10,  5, 10, 10],
    [ 5, -5,  0, -5,  5]
]

ROOK_POSITION_BONUS = [
    [0,  0,  5,  0,  0],
    [5,  5,  5,  5,  5],
    [0,  0,  0,  0,  0],
    [0,  0,  0,  0,  0],
    [5,  5,  5,  5,  5],
    [0,  0,  5,  0,  0]
]

QUEEN_POSITION_BONUS = [
    [-10, -5,  0, -5, -10],
    [-5,  0,  5,  0, -5],
    [0,   5,  10, 5,  0],
    [0,   5,  10, 5,  0],
    [-5,  0,  5,  0, -5],
    [-10, -5,  0, -5, -10]
]

KING_POSITION_BONUS = [
    [-60, -60, -60, -60, -60],
    [-60, -60, -60, -60, -60],
    [-40, -40, -40, -40, -40],
    [-20, -20, -20, -20, -20],
    [-10, -10, -10, -10, -10],
    [ 30,  20,   0,  20,  30]
]


KING_POSITION_BONUS_ENDGAME = [
    [ 0,  10,  20,  10,  0],
    [10,  30,  40,  30, 10],
    [20,  40,  50,  40, 20],
    [20,  40,  50,  40, 20],
    [10,  30,  40,  30, 10],
    [ 0,  10,  20,  10,  0],
]



POSITION_BONUS = {
    abs(WHITE_PAWN): PAWN_POSITION_BONUS,
    abs(WHITE_KNIGHT): KNIGHT_POSITION_BONUS,
    abs(WHITE_BISHOP): BISHOP_POSITION_BONUS,
    abs(WHITE_ROOK): ROOK_POSITION_BONUS,
    abs(WHITE_QUEEN): QUEEN_POSITION_BONUS,
    abs(WHITE_KING): KING_POSITION_BONUS
}

TRADE_BONUS = 10
