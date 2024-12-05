from settings import DIRECTIONS, GRID_ROWS, GRID_COLS, BLUE, GREEN, RED, CELL_COUNT


class Solver:
    def __init__(self, grid, original_grid):
        self.grid = grid
        self.original_gird = original_grid

    def has_single_solution(self):
        self.grid.remove_colors()
        cells = [cell for row in self.grid.cells for cell in row]
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
