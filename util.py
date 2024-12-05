import hashlib
import pickle

from settings import GRID_ROWS, GRID_COLS, GREEN, BLUE


def is_next_cell_valid(cell, direction):
    if (not (cell.row == 0 and direction[0] == -1) and
            not (cell.col == 0 and direction[1] == -1) and
            not (cell.row == GRID_ROWS - 1 and direction[0] == 1) and
            not (cell.col == GRID_COLS - 1 and direction[1] == 1)):
        return True
    return False


def get_opposite_direction(direction):
    if direction == "top":
        return "bottom"
    if direction == "right":
        return "left"
    if direction == "bottom":
        return "top"
    if direction == "left":
        return "right"


def switch_color(color):
    if color == GREEN:
        return BLUE
    return GREEN


def hash_object(obj):
    return hashlib.md5(pickle.dumps(obj)).hexdigest()

