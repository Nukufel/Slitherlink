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
        self.solution_cntr = 0

    def has_single_solution(self):

        cells = [cell for row in self.grid.cells for cell in row]
        cntr = len(cells)

        print("checking every combination of relevant cells")
        self.solution_cntr = 0

        return not self.solve(cells, cntr)

    def solve(self, cells, cntr):
        if cntr <= 0:
            if self.solution_cntr == 0:
                self.solution_cntr += 1
                return False
            return True

        cell = cells[cntr - 1]
        original_color = cell.color

        for color in [BLUE, GREEN]:
            cell.color = color

            if self.is_possible_cell(cell): # check if it is the solution grid
                if self.solve(cells, cntr - 1):
                    return True

        cell.color = original_color
        return False

    def is_possible_cell(self, base_cell):
        for cell in self.get_cells_to_test(base_cell):
            adj_cells = self.grid.get_adjacent_cells(cell, DIRECTIONS)
            green_count = 4 - len(adj_cells)
            blue_count = 0

            for adj_cell in adj_cells:
                if adj_cell.color == GREEN:
                    green_count += 1
                if adj_cell.color == BLUE:
                    blue_count += 1

            if cell.number in [1, 3] and ((green_count > 1 and blue_count > 1) or (green_count > 3 or blue_count > 3)):
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
