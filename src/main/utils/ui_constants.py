import os

# Base path relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", "..", ".."))
IMAGE_DIR = os.path.join(PROJECT_ROOT, "src", "main" ,"resources", "Images")

ICON_DIR = os.path.join(IMAGE_DIR, "Icons")
APP_ICON_PATH = os.path.join(ICON_DIR, "app_icon2.png")

BG_DIR = os.path.join(IMAGE_DIR, "Backgrounds")
APP_BG_PATH = os.path.join(BG_DIR, "app_bg.jpg")

PIECE_IMAGE_DIR = os.path.join(IMAGE_DIR, "Pieces")
PIECE_IMAGES = {
    1: os.path.join(PIECE_IMAGE_DIR, "white-pawn.png"),
    2: os.path.join(PIECE_IMAGE_DIR, "white-rook.png"),
    3: os.path.join(PIECE_IMAGE_DIR, "white-knight.png"),
    4: os.path.join(PIECE_IMAGE_DIR, "white-bishop.png"),
    5: os.path.join(PIECE_IMAGE_DIR, "white-queen.png"),
    6: os.path.join(PIECE_IMAGE_DIR, "white-king.png"),

    -1: os.path.join(PIECE_IMAGE_DIR, "black-pawn.png"),
    -2: os.path.join(PIECE_IMAGE_DIR, "black-rook.png"),
    -3: os.path.join(PIECE_IMAGE_DIR, "black-knight.png"),
    -4: os.path.join(PIECE_IMAGE_DIR, "black-bishop.png"),
    -5: os.path.join(PIECE_IMAGE_DIR, "black-queen.png"),
    -6: os.path.join(PIECE_IMAGE_DIR, "black-king.png"),
}


# Board Colors and types
GRAY = 1
BLUE = 2
GREEN = 3
PURPLE = 4
MARINE = 5

GRAY_BOARD = {
    "LIGHT": "#f0d9b5",
    "DARK": "#b58863"
}

BLUE_BOARD = {
    "LIGHT": "#dee3e6",
    "DARK": "#8ca2ad"
}

GREEN_BOARD = {
    "LIGHT": "#eeeed2",
    "DARK": "#769656"
}

PURPLE_BOARD = {
    "LIGHT": "#e8e9f3",
    "DARK": "#7d6b91"
}

MARINE_BOARD = {
    "LIGHT": "#e8ebef",
    "DARK": "#485a70"
}