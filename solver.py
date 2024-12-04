from settings import DIRECTIONS, GRID_ROWS, GRID_COLS, BLUE, GREEN, RED
from util import switch_color
import random

MAX_CELLS = GRID_ROWS * GRID_COLS
CORNERS = [
    (0, 0),
    (0, GRID_COLS - 1),
    (GRID_ROWS - 1, GRID_COLS - 1),
    (GRID_ROWS - 1, 0)
]


class Solver:
    def __init__(self, grid, original_grid):
        self.grid = grid
        self.original_gird = original_grid

    def has_single_solution(self):
        self.grid.remove_colors()
        return self.solve(self.scout_patterns())

    def solve(self, cells):

        if len(cells) > MAX_CELLS:
            return True

        rand_cell = cells[-1]
        green_adj_cells = [cell for cell in self.grid.get_adjacent_cells(rand_cell, DIRECTIONS) if cell.color is None]

        if green_adj_cells:
            cell = random.choice(green_adj_cells)
            for color in [GREEN, BLUE]:
                cell.color = color
                cells.append(cell)
                if self.is_possible_solution():
                    if self.solve(cells):
                        return True
            cell.color = None
            cells.remove(cell)
        return False

    def get_all_blue_cells(self):
        blue_cells = []

        for row in self.grid.cells:
            for cell in row:
                if cell.color == BLUE:
                    blue_cells.append(cell)
        return blue_cells

    def scout_patterns(self):
        found_cells = []
        for row in self.grid.cells:
            for cell in row:
                if cell.number == 0 and self.is_border_cell(cell):
                    cell.color = GREEN
                    found_cells.append(cell)
                if cell.number == 3 and self.is_corner(cell):
                    cell.color = BLUE
                    found_cells.append(cell)
                if cell.number == 1 and self.is_corner(cell):
                    cell.color = GREEN
                    found_cells.append(cell)
                if cell.number == 2 and self.is_corner(cell):
                    found_cells.extend(self.color_adj_cells(cell, BLUE))
        return found_cells

    def color_adj_cells(self, cell, color):
        found_cells = []
        adj_cells = self.grid.get_adjacent_cells(cell, DIRECTIONS)
        for adj_cell in adj_cells:
            adj_cell.color = color
            found_cells.append(adj_cell)
        return found_cells


    def is_possible_solution(self):
        for row in self.grid.cells:
            for cell in row:
                adj_cells = self.grid.get_adjacent_cells(cell, DIRECTIONS)
                green_count = 4 - len(adj_cells)
                blue_count = 0

                for adj_cell in adj_cells:
                    if adj_cell.color == GREEN:
                        green_count += 1
                    if adj_cell.color == BLUE:
                        blue_count += 1

                if cell.color == GREEN:
                    if cell.number == 3 and green_count > 1:
                        return False
                    if cell.number == 1 and blue_count > 1:
                        return False
                    if cell.number == 0 and blue_count > 0:
                        return False
                elif cell.color == BLUE:
                    if cell.number == 3 and blue_count > 1:
                        return False
                    if cell.number == 1 and green_count > 1:
                        return False
                    if cell.number == 0 and green_count > 0:
                        return False
                else:
                    if cell.number in [1, 3] and ((green_count > 1 and blue_count > 1) or (green_count > 3 or blue_count > 3)):
                        return False
                    if cell.number == 0 and green_count > 0 and blue_count > 0:
                        return False

                if cell.number == 2 and (green_count > 2 or blue_count > 2):
                    return False

        return True

    def get_cells_to_test(self, cell):
        cells = self.grid.get_adjacent_cells(cell, DIRECTIONS)
        cells.append(cell)
        return cells

    def set_gird(self, grid):
        self.grid = grid

    def is_original_solution(self):
        for row in self.grid.cells:
            for cell in row:
                if cell.color != self.original_gird.cells[cell.row][cell.col].color:
                    return False
        return True

    def is_corner(self, cell):
        return cell.row in {0, GRID_ROWS - 1} and cell.col in {0, GRID_COLS - 1}

    def is_border_cell(self, cell):
        return cell.row in {0, GRID_ROWS - 1} or cell.col in {0, GRID_COLS - 1}

