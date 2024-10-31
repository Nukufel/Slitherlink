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
                    print(cell.row, cell.col)
                    if not cell.is_satisfied():
                        if self.is_valid_border(cell, pos):
                            self.grid.set_boarder(cell, pos, True)


    def set_crosses_for_0(self):
        for row in self.grid.cells:
            for cell in row:
                if cell.number == 0:
                    for direction in DIRECTIONS.keys():
                        self.grid.set_boarder(cell, direction, False)

    def is_valid_border(self, cell, pos):
            positions = None
            match pos:
                case "top":
                    positions = {
                        (- 1, 0): ("left", "right"),
                        (0, - 1): ("top", "right"),
                        (0, 1): ("top", "left"),
                        (0, 0): ("right", "left")
                    }
                case "left":
                    positions = {
                        (- 1, 0): ("left", "bottom"),
                        (0,- 1): ("top", "bottom"),
                        (1, 0): ("top", "left"),
                        (0, 0): ("top", "bottom")
                    }

                case "bottom":
                    positions = {
                        (0, 0): ("left", "right"),
                        (0, - 1): ("right", "bottom"),
                        (0, 1): ("bottom", "left"),
                        (- 1, 0): ("left", "right")
                    }
                case "right":
                    positions = {
                        (- 1, 0): ("right", "bottom"),
                        (0, 1): ("top", "bottom"),
                        (1, 0): ("top", "right"),
                        (0, 1): ("top", "bottom")
                    }

            return self.has_possible_border(cell, positions)

    def has_possible_border(self, cell, positions):
        boarder_cntr = 0
        for pos, borders in positions.items():
            if is_next_cell_valid(cell, pos):
                next_cell = self.grid.cells[cell.row + pos[0]][cell.col + pos[1]]
                for border in borders:
                    if next_cell.borders[border] is True or next_cell.borders[border] is None:
                        if not next_cell.is_satisfied():
                            boarder_cntr += 1
        if boarder_cntr >= 4:
            return True
        return False





