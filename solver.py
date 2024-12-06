import time

from settings import DIRECTIONS, GRID_ROWS, GRID_COLS, BLUE, GREEN, RED, CELL_COUNT
from util import switch_color, hash_object
from copy import deepcopy

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
        while self.scout_patterns():
            pass
        cells = [cell for row in self.grid.cells for cell in row if cell.color is None]
        return not self.solve(cells)

    def solve(self, cells):
        try:
            cell = cells[-1]
        except IndexError:
            return True

        cells.remove(cell)

        for color in [GREEN, BLUE]:
            cell.color = color
            if self.is_possible_solution() and not self.is_original_solution():
                if self.solve(cells):
                    return True

        cell.color = None
        cells.append(cell)
        return False

    def count_adj_colors(self, cell):
        adj_cells = self.grid.get_adjacent_cells(cell, DIRECTIONS)
        green_count = 4 - len(adj_cells)
        blue_count = 0

        for adj_cell in adj_cells:
            if adj_cell.color == GREEN:
                green_count += 1
            if adj_cell.color == BLUE:
                blue_count += 1
        return green_count, blue_count

    def is_possible_solution(self):
        for row in self.grid.cells:
            for cell in row:

                green_count, blue_count = self.count_adj_colors(cell)

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
                    if cell.number in [1, 3] and (
                            (green_count > 1 and blue_count > 1) or (green_count > 3 or blue_count > 3)):
                        return False
                    if cell.number == 0 and green_count > 0 and blue_count > 0:
                        return False

                if cell.number == 2 and (green_count > 2 or blue_count > 2):
                    return False

        return True

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

    def scout_patterns(self):
        initial_hash = hash_object(self.grid)
        for row in self.grid.cells:
            for cell in row:
                if cell.number is None:
                    self.pattern_none(cell)

                if cell.number == 0:
                    self.pattern_0s(cell)

                if cell.number == 1:
                    self.pattern_1s(cell)

                if cell.number == 2:
                    self.pattern_2s(cell)

                if cell.number == 3:
                    self.pattern_3s(cell)

        if initial_hash == hash_object(self.grid):
            return False
        return True

    def pattern_none(self, cell):
        green_count, blue_count = self.count_adj_colors(cell)
        if green_count == 4:
            cell.color = GREEN
        if blue_count == 4:
            cell.color = BLUE

    def pattern_0s(self, cell):
        if cell.color is None and self.is_border_cell(cell):
            cell.color = GREEN

        if cell.color is None:
            adj_cells = self.grid.get_adjacent_cells(cell, DIRECTIONS)
            for adj_cell in adj_cells:
                if adj_cell.color is not None:
                    cell.color = adj_cell.color
                    break

        if cell.color is not None:
            self.color_adj_cells(cell, cell.color)

            adj_cells = self.grid.get_adjacent_cells(cell, DIRECTIONS)
            for adj_cell in adj_cells:
                if adj_cell.number == 3 and adj_cell.color is None:
                    self.color_adj_cells(adj_cell, switch_color(cell.color))

            diagonal_cells = self.get_diagonal_cell(cell)
            for diagonal_cell in diagonal_cells:
                if diagonal_cell.number == 3 and diagonal_cell.color is None:
                    diagonal_cell.color = switch_color(cell.color)

    def pattern_1s(self, cell):
        if cell.color is None and self.is_corner(cell):
            cell.color = GREEN
            adj_cells = self.grid.get_adjacent_cells(cell, DIRECTIONS)
            for adj_cell in adj_cells:
                if adj_cell.number == 3 and adj_cell.color is None:
                    adj_cell.color = BLUE

        if cell.color is None:
            green_count, blue_count = self.count_adj_colors(cell)
            if green_count > 1:
                cell.color = GREEN
            if blue_count > 1:
                cell.color = BLUE

        if cell.color is not None and self.is_border_cell(cell):
            adj_cells = self.grid.get_adjacent_cells(cell, DIRECTIONS)
            for adj_cell in adj_cells:
                if adj_cell.number == 1 and self.is_border_cell(adj_cell) and adj_cell.color is None:
                    adj_cell.color = cell.color

    def pattern_2s(self, cell):
        if self.is_corner(cell):
            self.color_adj_cells(cell, BLUE)

            adj_cells = self.grid.get_adjacent_cells(cell, DIRECTIONS)
            for adj_cell in adj_cells:
                if adj_cell.number == 1:
                    cell.color = BLUE
                    break

            diagonal_cells = self.get_diagonal_cell(cell)
            for diagonal_cell in diagonal_cells:
                if diagonal_cell.number == 3:
                    diagonal_cell.color = GREEN
                    cell.color = BLUE
                    break

    def pattern_3s(self, cell):
        if cell.color is None and self.is_corner(cell):
            cell.color = BLUE

        if cell.color is None and self.is_border_cell(cell):
            adj_cells = self.grid.get_adjacent_cells(cell, DIRECTIONS)
            for adj_cell in adj_cells:
                if adj_cell.number == 1 and self.is_border_cell(adj_cell) and adj_cell.color is None:
                    cell.color = BLUE
                    break

        if cell.color is None:
            green_count, blue_count = self.count_adj_colors(cell)
            if green_count > 1:
                cell.color = BLUE
            if blue_count > 1:
                cell.color = GREEN

        if cell.color is not None:
            adj_cells = self.grid.get_adjacent_cells(cell, DIRECTIONS)
            for adj_cell in adj_cells:
                if adj_cell.number == 3 and adj_cell.color is None:
                    adj_cell.color = switch_color(cell.color)

    def color_adj_cells(self, cell, color):
        adj_cells = self.grid.get_adjacent_cells(cell, DIRECTIONS)
        for adj_cell in adj_cells:
            if adj_cell.color is None:
                adj_cell.color = color

    def get_diagonal_cell(self, cell):
        diagonal_cords = [
            (-1, -1), # top left
            (-1, 1), # top right
            (1, 1), # bottom right
            (1, -1) # bottom left
        ]
        diagonal_cells = []
        for x, y in diagonal_cords:
            try:
                row = cell.row + x
                col = cell.col + y
                if row < 0 or col < 0:
                    raise IndexError
                diagonal_cells.append(self.grid.cells[row][col])
            except IndexError:
                pass
        return diagonal_cells

