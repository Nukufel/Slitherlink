import random

from settings import DIRECTIONS
from util import is_next_cell_valid
VALID_COMBINATIONS = {
    0: [[]],
    1: [["top"], ["bottom"], ["left"], ["right"]],
    2: [["top", "bottom"], ["left", "right"], ["top", "right"], ["top", "left"], ["bottom", "left"], ["bottom", "right"]],
    3: [["top", "bottom", "left"], ["top", "bottom", "right"], ["top", "left", "right"], ["bottom", "left", "right"]],
}


class Solver:
    def __init__(self, grid):
        self.grid = grid

    def solve(self, cells):
        for cell in cells:
            cell_number = cell.number
            combinations = VALID_COMBINATIONS[cell_number]
            self.set_boarders_and_crosses(combinations[0], cell)
            if self.is_valid_combination(cell):
                print(cell.row, cell.col, "is not valid")


    def is_valid_combination(self, cell):
        for key, value in cell.borders.items():
            if value:
                r = cell.row
                c = cell.col
                positions = None
                match key:
                    case "top":
                        positions = {
                                (r-1, c): ("left", "right"),
                                (r, c-1): ("top", "right"),
                                (r, c+1): ("top", "left"),
                                (r, c): ("right", "left")
                            }
                        pass
                    case "left":
                        positions = {
                            (r-1, c): ("left", "bottom"),
                            (r, c-1): ("top", "bottom"),
                            (r+1, c): ("top", "left"),
                            (r, c): ("top", "bottom")
                        }

                    case "bottom":
                        positions = {
                            (r, c): ("left", "right"),
                            (r, c-1): ("right", "bottom"),
                            (r, c+1): ("bottom", "left"),
                            (r-1, c): ("left", "right")
                        }
                    case "right":
                        positions = {
                            (r-1, c): ("right", "bottom"),
                            (r, c+1): ("top", "bottom"),
                            (r+1, c): ("top", "right"),
                            (r, c): ("top", "bottom")
                        }

                return self.has_possible_boarder(cell, positions)

    def has_possible_boarder(self, cell, positions):
        for key, value in positions.items():
            if is_next_cell_valid(cell, key):
                print("next cell is valid")
                next_cell = self.grid.cells[key[0]][key[1]]
                print(next_cell.row, next_cell.col)
                for pos in value:
                    print("pos")
                    if next_cell.borders[pos] is True or next_cell.borders[pos] or None:
                        print("ture")
                        return True
        return False

    def set_boarders_and_crosses(self, combination, cell):
        for pos in combination:
            self.grid.set_boarder(cell, pos, True)
            for boarder in cell.borders:
                if not cell.borders[boarder]:
                    self.grid.set_boarder(cell, pos, False)




