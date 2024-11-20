from settings import DIRECTIONS, GRID_ROWS, GRID_COLS, BLUE, GREEN, RED
from util import switch_color
import copy

MAX_CELLS = GRID_ROWS * GRID_COLS
CORNERS = [
    (0, 0),
    (0, GRID_COLS - 1),
    (GRID_ROWS - 1, GRID_COLS - 1),
    (GRID_ROWS - 1, 0)
]


class Solver:
    def __init__(self, grid):
        self.grid = grid

    def has_single_solution(self):
        for row in self.grid.cells:
            for cell in row:

                color = cell.color
                cell.color = switch_color(color)

                if self.is_possible_cell(cell):
                    cell.color = color
                    return False

                cell.color = color
        return True

    def is_possible_cell(self, cell):
        for cell in self.get_cells_to_test(cell):
            adj_cells = self.grid.get_adjacent_cells(cell, DIRECTIONS)
            green_count = 4 - len(adj_cells)
            blue_count = 0

            for adj_cell in adj_cells:
                if adj_cell.color == GREEN:
                    green_count += 1
                if adj_cell.color == BLUE:
                    blue_count += 1

            if cell.number in [1, 3] and green_count > 1 and blue_count > 1 and (green_count > 3 or blue_count > 3):
                return False
            if cell.number == 2 and (green_count > 2 or blue_count > 2):
                return False
            if cell.number == 0 and green_count > 0 and blue_count > 0:
                return False
        return True

    def get_cells_to_test(self, cell):
        cells = self.grid.get_adjacent_cells(cell, DIRECTIONS)
        cells.append(cell)
        return cells

    def set_gird(self, grid):
        self.grid = grid
