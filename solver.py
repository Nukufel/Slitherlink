from settings import DIRECTIONS, GRID_ROWS, GRID_COLS, BLUE, GREEN
from util import switch_color
import numpy as np

CORNERS = [
    (0, 0),
    (0, GRID_COLS - 1),
    (GRID_ROWS - 1, GRID_COLS - 1),
    (GRID_ROWS - 1, 0)
]




class Solver:
    def __init__(self, grid, original_grid):
        self.grid = grid
        self.original_grid = original_grid
        self.color_count_per_cell = {}

    def has_single_solution(self):
        self.grid.remove_colors()
        while self.scout_patterns():
            pass
        cells = self.grid.cells.flatten().tolist()
        return not self.solve(cells)

    def solve(self, cells):
        try:
            cell = cells[-1]
        except IndexError:
            return True

        cells.remove(cell)

        for color in [GREEN, BLUE]:
            cell.color = color
            if self.is_possible_solution(cell) and not self.is_original_solution():
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

    def is_possible_solution(self, cell):
        adj_cells = self.grid.get_adjacent_cells(cell, DIRECTIONS)
        adj_cells.append(cell)

        for cell in adj_cells:

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
                if cell.color != self.original_grid.cells[cell.row, cell.col].color:
                    return False
        return True

    def is_corner(self, cell):
        return cell.row in {0, GRID_ROWS - 1} and cell.col in {0, GRID_COLS - 1}

    def is_border_cell(self, cell):
        return cell.row in {0, GRID_ROWS - 1} or cell.col in {0, GRID_COLS - 1}

    def scout_patterns(self):
        changed = False
        for row in self.grid.cells:
            for cell in row:
                adj_cells = self.grid.get_adjacent_cells(cell, DIRECTIONS)
                if cell.number is None:
                    changed = self.pattern_none(cell)

                if cell.number == 0:
                    changed = self.pattern_0s(cell, adj_cells)

                if cell.number == 1:
                    changed = self.pattern_1s(cell, adj_cells)

                if cell.number == 2:
                    changed = self.pattern_2s(cell, adj_cells)

                if cell.number == 3:
                    changed = self.pattern_3s(cell, adj_cells)

        return changed

    def pattern_none(self, cell):
        changed = False
        green_count, blue_count = self.count_adj_colors(cell)
        if green_count == 4:
            cell.color = GREEN
            changed = True
        if blue_count == 4:
            cell.color = BLUE
            changed = True

        return changed

    def pattern_0s(self, cell, adj_cells):
        changed = False
        if cell.color is None and self.is_border_cell(cell):
            cell.color = GREEN
            changed = True

        if cell.color is None:
            for adj_cell in adj_cells:
                if adj_cell.color is not None:
                    cell.color = adj_cell.color
                    changed = True
                    break

        if cell.color is not None:
            changed = self.color_adj_cells(cell, cell.color)
            for adj_cell in adj_cells:
                if adj_cell.number == 3 and adj_cell.color is None:
                    self.color_adj_cells(adj_cell, switch_color(cell.color))

            diagonal_cells = self.get_diagonal_cell(cell)
            for diagonal_cell in diagonal_cells:
                if diagonal_cell.number == 3 and diagonal_cell.color is None:
                    diagonal_cell.color = switch_color(cell.color)

        return changed

    def pattern_1s(self, cell, adj_cells):
        changed = False
        if self.is_corner(cell) and cell.color is None:
            cell.color = GREEN
            for adj_cell in adj_cells:
                if adj_cell.number == 3 and adj_cell.color is None:
                    adj_cell.color = BLUE
                    changed = True

        if cell.color is None:
            green_count, blue_count = self.count_adj_colors(cell)
            if green_count > 1:
                cell.color = GREEN
                changed = True
            if blue_count > 1:
                cell.color = BLUE
                changed = True

        if self.is_border_cell(cell) and cell.color is not None:
            for adj_cell in adj_cells:
                if adj_cell.number == 1 and self.is_border_cell(adj_cell) and adj_cell.color is None:
                    adj_cell.color = cell.color
                    changed = True

        return changed

    def pattern_2s(self, cell, adj_cells):
        changed = False
        if self.is_corner(cell):
            changed = self.color_adj_cells(cell, BLUE)

            for adj_cell in adj_cells:
                if adj_cell.number == 1 and cell.color is None:
                    cell.color = BLUE
                    changed = True
                    break

            diagonal_cells = self.get_diagonal_cell(cell)
            for diagonal_cell in diagonal_cells:
                if diagonal_cell.number == 3 and (diagonal_cell.color is None or cell.color is None):
                    diagonal_cell.color = GREEN
                    cell.color = BLUE
                    changed = True
                    break

        return changed

    def pattern_3s(self, cell, adj_cells):
        changed = False
        if self.is_corner(cell) and cell.color is None:
            cell.color = BLUE
            changed = True

        if self.is_border_cell(cell) and cell.color is None:
            for adj_cell in adj_cells:
                if adj_cell.number == 1 and self.is_border_cell(adj_cell) and adj_cell.color is None:
                    cell.color = BLUE
                    changed = True
                    break

        if cell.color is None:
            green_count, blue_count = self.count_adj_colors(cell)
            if green_count > 1:
                cell.color = BLUE
                changed = True
            if blue_count > 1:
                cell.color = GREEN
                changed = True

        if cell.color is not None:
            for adj_cell in adj_cells:
                if adj_cell.number == 3 and adj_cell.color is None:
                    adj_cell.color = switch_color(cell.color)
                    changed = True

        return changed

    def color_adj_cells(self, cell, color):
        changed = False
        adj_cells = self.grid.get_adjacent_cells(cell, DIRECTIONS)
        for adj_cell in adj_cells:
            if adj_cell.color is None:
                adj_cell.color = color
                changed = True
        return changed

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
                diagonal_cells.append(self.grid.cells[row, col])
            except IndexError:
                pass
        return diagonal_cells

