from settings import DIRECTIONS, GRID_ROWS, GRID_COLS, BLUE, GREEN
from util import is_next_cell_valid

MAX_CELLS = GRID_ROWS * GRID_COLS


class Solver:
    def __init__(self, grid):
        self.grid = grid
        self.clear_colors()
        self.scout_inside_patterns()
        self.scout_outside_patterns()



    def solve(self):
        cell = self.is_full_grid()
        if not cell:
            return True
        else:
            for color in [GREEN, BLUE]:
                if self.has_possible_amount_of_neighbours(cell, color):
                    cell.color = color
                    if self.solve():
                        return True
                    cell.color = None
            return False

    def clear_colors(self):
        for row in self.grid.cells:
            for cell in row:
                cell.color = None

    def scout_outside_patterns(self):
        pattern_corner_1 = [(0,0),(0,GRID_COLS-1),(GRID_ROWS-1,0),(GRID_ROWS-1,GRID_COLS-1)]
        for row in self.grid.cells:
                for cell in row:
                    if cell.number == 0:
                        if (cell.row == 0 or cell.row == GRID_ROWS-1) and (cell.col == 0 or cell.col == GRID_COLS-1):
                            cell.color = GREEN
                    if cell.number == 1:
                        pattern = (cell.row, cell.col)
                        if pattern in pattern_corner_1:
                            cell.color = GREEN

    def scout_inside_patterns(self):
        pattern_corner_3 = [(0,0),(0,GRID_COLS-1),(GRID_ROWS-1,0),(GRID_ROWS-1,GRID_COLS-1)]
        for row in self.grid.cells:
            for cell in row:
                if cell.number == 3:
                    pattern = (cell.row, cell.col)
                    if pattern in pattern_corner_3:
                        cell.color = BLUE

    def has_possible_amount_of_neighbours(self, cell, color):
        blue_count = 0
        green_count = 0
        for key, value in DIRECTIONS.items():
            one_direction = {key: value}
            adjacent_cell = self.grid.get_adjacent_cells(cell, one_direction)
            if adjacent_cell:
                if adjacent_cell[0].color == BLUE:
                    blue_count += 1
                elif adjacent_cell[0].color == GREEN:
                    green_count += 1
            else:
                green_count += 1

        if color == GREEN:
            if blue_count <= cell.number and green_count <= (4 - cell.number):
                return True
        elif color == BLUE:
            if blue_count <= (4 - cell.number) and green_count <= cell.number:
                return True
        return False

    def is_full_grid(self):
        for row in self.grid.cells:
            for cell in row:
                if cell.color is None:
                    return cell
        return None





