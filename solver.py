import random

from settings import DIRECTIONS, GRID_ROWS, GRID_COLS
from util import is_next_cell_valid

MAX_CELLS = GRID_ROWS * GRID_COLS


class Solver:
    def __init__(self, grid):
        self.grid = grid
        self.stack = []

    def solve(self):
        self.set_crosses_for_0()
        for row in self.grid.cells:
            for cell in row:
                for pos in cell.get_empty_boarders():
                    if self.is_valid_border(cell, pos):
                        self.grid.set_boarder(cell, pos, True)

    def set_crosses_for_0(self):
        for row in self.grid.cells:
            for cell in row:
                if cell.number == 0:
                    for direction in DIRECTIONS.keys():
                        self.grid.set_boarder(cell, direction, False)

    def is_valid_border(self, cell, pos):
            r = cell.row
            c = cell.col
            positions = None
            match pos:
                case "top":
                    positions = {
                        (r - 1, c): ("left", "right"),
                        (r, c - 1): ("top", "right"),
                        (r, c + 1): ("top", "left"),
                        (r, c): ("right", "left")
                    }
                    pass
                case "left":
                    positions = {
                        (r - 1, c): ("left", "bottom"),
                        (r, c - 1): ("top", "bottom"),
                        (r + 1, c): ("top", "left"),
                        (r, c): ("top", "bottom")
                    }

                case "bottom":
                    positions = {
                        (r, c): ("left", "right"),
                        (r, c - 1): ("right", "bottom"),
                        (r, c + 1): ("bottom", "left"),
                        (r - 1, c): ("left", "right")
                    }
                case "right":
                    positions = {
                        (r - 1, c): ("right", "bottom"),
                        (r, c + 1): ("top", "bottom"),
                        (r + 1, c): ("top", "right"),
                        (r, c): ("top", "bottom")
                    }

            return self.has_possible_border(cell, positions)

    def has_possible_border(self, cell, positions):
        pass



