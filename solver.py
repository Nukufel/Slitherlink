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
            print("Scouting patterns")
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
        copy_grid = deepcopy(self.grid)
        for row in self.grid.cells:
            for cell in row:

                if cell.number == 0:
                    if self.is_border_cell(cell):
                        cell.color = GREEN
                    if cell.color is None:
                        adj_cells = self.grid.get_adjacent_cells(cell, DIRECTIONS)
                        color = [cell.color for cell in adj_cells if cell.color is not None][0]
                        if color:
                            cell.color = color
                    if cell.color is not None:
                        self.color_adj_cells(cell, cell.color)

                if cell.number == 3:
                    if self.is_corner(cell):
                        cell.color = BLUE
                    if cell.color is not None:
                        adj_cells = self.grid.get_adjacent_cells(cell, DIRECTIONS)
                        adj_3s = [adj_cell for adj_cell in adj_cells if cell.number == 3]
                        for adj_3 in adj_3s:
                            adj_3.color = switch_color(cell.color)

                if cell.number == 1:
                    if self.is_corner(cell):
                        cell.color = GREEN
                    if cell.color is not None:
                        if self.is_border_cell(cell):
                            adj_cells = self.grid.get_adjacent_cells(cell, DIRECTIONS)
                            adj_boarder_1s = [adj_cell for adj_cell in adj_cells if cell.number == 1 and self.is_border_cell(adj_cell)]
                            for adj_boarder_1 in adj_boarder_1s:
                                adj_boarder_1.color = cell.color

                if cell.number == 2:
                    if self.is_corner(cell):
                        self.color_adj_cells(cell, BLUE)
                        diagonal_cell = self.get_corner_diagonal_cell(cell)
                        if diagonal_cell.number == 3:
                            diagonal_cell.color = GREEN
                            cell.color = BLUE

            if hash_object(copy_grid) == hash_object(self.grid):
                return False
            return True

    def color_adj_cells(self, cell, color):
        adj_cells = self.grid.get_adjacent_cells(cell, DIRECTIONS)
        for adj_cell in adj_cells:
            adj_cell.color = color

    def get_corner_diagonal_cell(self, cell):
        diagonal_to_corner = {
            CORNERS[0]: (GRID_ROWS - (GRID_COLS - 1), GRID_COLS - (GRID_COLS - 1)),
            CORNERS[1]: (GRID_ROWS - (GRID_COLS - 1), GRID_COLS - 2),
            CORNERS[2]: (GRID_ROWS - 2, GRID_COLS - 2),
            CORNERS[3]: (GRID_ROWS - 2, GRID_COLS - (GRID_COLS - 1))
        }
        for key, pos in diagonal_to_corner.items():
            if key == (cell.row, cell.col):
                return self.grid.cells[pos[0]][pos[1]]
        return None






