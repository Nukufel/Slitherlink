from settings import DIRECTIONS, GRID_ROWS, GRID_COLS, BLUE, GREEN
from cell import Cell
from util import switch_color

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

    # rewrite
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

                if cell.number in [1, 3] and green_count > 1 and blue_count > 1:
                    return False
                if cell.number == 2:
                    if green_count > 2:
                        return False
                    if blue_count > 2:
                        return False
                if cell.number == 0 and green_count > 0 and blue_count > 0:
                    return False

        if not self.can_blue_be_connected():
            return False
        return True

    def can_blue_be_connected(self):
        start_blue = None
        for row in self.grid.cells:
            for cell in row:
                if not cell.color == GREEN and not start_blue:
                    start_blue = cell
                    break
        if self.get_all_possible_blue([start_blue]):
            return True
        return False

    def get_all_possible_blue(self, not_green_cells):
        connected_blue = not_green_cells

        if len(connected_blue) + len(self.get_all_greens()) == MAX_CELLS:
            return True

        for not_green_cell in not_green_cells:
            adj_cells = self.grid.get_adjacent_cells(not_green_cell, DIRECTIONS)
            for adj_cell in adj_cells:
                if adj_cell.color != GREEN and adj_cell not in connected_blue:
                    append(connected_blue, adj_cell)
                    if self.get_all_possible_blue(connected_blue):
                        return True
        return False

    def get_all_greens(self):
        greens = []
        for row in self.grid.cells:
            for cell in row:
                if cell.color == GREEN:
                    append(greens, cell)
        return greens

    def has_different_solution(self):
        for row in self.grid.cells:
            for cell in row:
                color = cell.color
                cell.color = switch_color(color)

                if self.is_possible_solution():
                    return True

                cell.color = color
        return False


def append(some_list, cell):
    if cell not in some_list:
        some_list.append(cell)
        return True
    return False