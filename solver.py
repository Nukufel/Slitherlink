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
        self.cell_list = []
        self.clear_colors()
        self.cell_list.extend(self.scout_inside_patterns())
        self.cell_list.extend(self.scout_outside_patterns())

    def clear_colors(self):
        for row in self.grid.cells:
            for cell in row:
                cell.color = None

    # rewrite
    def is_possible_solution(self):
        for cell in self.cell_list:
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
                    self.append(connected_blue, adj_cell)
                    if self.get_all_possible_blue(connected_blue):
                        return True
        return False

    def get_all_greens(self):
        greens = []
        for row in self.grid.cells:
            for cell in row:
                if cell.color == GREEN:
                    greens.append(cell)
        return greens

    def get_next_uncolored_cell(self):
        for row in self.grid.cells:
            for cell in row:
                if cell.color is None:
                    return cell
        return None

    # rewrite
    def solve(self, max_recursion=None):
        possible_cells = []
        cell = self.get_next_uncolored_cell()
        if not cell:
            return True

        for color in [GREEN, BLUE]:
            self.set_colors_and_append(cell, color, self.cell_list)
            self.append(possible_cells, cell)

            for solved_cell in self.solve_by_colors():
                self.append(self.cell_list, solved_cell)
                self.append(possible_cells, solved_cell)
            if max_recursion is not None:
                if self.is_possible_solution() and max_recursion > 0:
                    if self.solve(max_recursion-1):
                        return True
            else:
                if self.is_possible_solution():
                    if self.solve():
                        return True

            for possible_cell in possible_cells:
                self.cell_list.remove(possible_cell)
                possible_cell.color = None
                possible_cells = []

        return False

    def set_colors_and_append(self, cell, color, new_list):
        if self.append(new_list, cell):
            cell.color = color

    def append(self, some_list, cell):
        if cell not in some_list:
            some_list.append(cell)
            return True
        return False

    # only patterns down here
    def has_specific_adjacent_cell(self, cell, number, invert=False):
        adj_cells = self.grid.get_adjacent_cells(cell, DIRECTIONS)
        for adj_cell in adj_cells:
            if invert:
                if adj_cell.number != number:
                    return adj_cell
            else:
                if adj_cell.number == number:
                    return adj_cell
        return None

    def get_diagonal_cell(self, cell):
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

    def is_corner(self, cell):
        return cell.row in {0, GRID_ROWS - 1} and cell.col in {0, GRID_COLS - 1}

    def is_border_cell(self, cell):
        return cell.row in {0, GRID_ROWS - 1} or cell.col in {0, GRID_COLS - 1}

    def has_2_border_3_neighbours(self, adj_cells):
        border_3s = []
        for adj_cell in adj_cells:
            if adj_cell.number == 3 and self.is_border_cell(adj_cell):
                border_3s.append(adj_cell)
        if len(border_3s) == 2:
            return border_3s
        return None

    def scout_outside_patterns(self):
        cell_list = []

        for row in self.grid.cells:
            for cell in row:
                if cell.number == 0 and self.is_border_cell(cell):
                    self.set_colors_and_append(cell, GREEN, cell_list)
                    adjacent_cell = self.grid.get_adjacent_cells(cell, DIRECTIONS)

                    for adj_cell in adjacent_cell:
                        self.set_colors_and_append(adj_cell, GREEN, cell_list)

                if cell.number == 1 and self.is_corner(cell):
                    self.get_row_of_1_from_corner(cell, cell_list)
        return cell_list

    def scout_inside_patterns(self):
        cell_list = []

        for row in self.grid.cells:
            for cell in row:
                if cell.number == 3 and self.is_corner(cell):
                    self.set_colors_and_append(cell, BLUE, cell_list)

                    adj_cell = self.has_specific_adjacent_cell(cell, 3)
                    if adj_cell:
                        self.set_colors_and_append(adj_cell, GREEN, cell_list)
                        self.set_colors_and_append(self.get_diagonal_cell(cell), BLUE, cell_list)

                        adj_cell_2 = self.has_specific_adjacent_cell(cell, 3, True)
                        if adj_cell_2:
                            self.set_colors_and_append(adj_cell_2, BLUE, cell_list)

                if cell.number == 2 and self.is_corner(cell):
                    diagonal_cell = self.get_diagonal_cell(cell)
                    adj_cells = self.grid.get_adjacent_cells(cell, DIRECTIONS)
                    if diagonal_cell.number == 3:
                        self.set_colors_and_append(diagonal_cell, GREEN, cell_list)
                        self.set_colors_and_append(cell, BLUE, cell_list)

                        for adj_cell in adj_cells:
                            self.set_colors_and_append(adj_cell, BLUE, cell_list)

                    for adj_cell in adj_cells:
                        if adj_cell.number == 1:
                            self.set_colors_and_append(cell, BLUE, cell_list)
                            self.set_colors_and_append(adj_cell, BLUE, cell_list)
                            for adj_adj_cell in self.grid.get_adjacent_cells(adj_cell, DIRECTIONS):
                                if self.is_border_cell(adj_adj_cell):
                                    self.set_colors_and_append(adj_adj_cell, BLUE, cell_list)

                if cell.number == 1 and self.is_corner(cell):
                    adj_cell = self.has_specific_adjacent_cell(cell, 3)
                    if adj_cell:
                        self.set_colors_and_append(cell, GREEN, cell_list)
                        self.set_colors_and_append(adj_cell, BLUE, cell_list)

                if self.is_corner(cell):
                    adj_cells = self.grid.get_adjacent_cells(cell, DIRECTIONS)
                    boarder_3s = self.has_2_border_3_neighbours(adj_cells)
                    if boarder_3s:
                        self.set_colors_and_append(cell, GREEN, cell_list)
                        for boarder_3 in boarder_3s:
                            self.set_colors_and_append(boarder_3, BLUE, cell_list)

                if cell.number == 1 and self.is_border_cell(cell):
                    adj_cells = self.grid.get_adjacent_cells(cell, DIRECTIONS)
                    boarder_3s = self.has_2_border_3_neighbours(adj_cells)
                    if boarder_3s:
                        self.set_colors_and_append(cell, BLUE, cell_list)
                        for boarder_3 in boarder_3s:
                            self.set_colors_and_append(boarder_3, BLUE, cell_list)
        return cell_list

    def get_row_of_1_from_corner(self, cell, my_list):
        adj_cell = self.has_specific_adjacent_cell(cell, 1)
        if adj_cell and self.is_border_cell(adj_cell) and adj_cell not in my_list:
            self.set_colors_and_append(adj_cell, GREEN, my_list)
            self.get_row_of_1_from_corner(adj_cell, my_list)

    def solve_by_colors(self):
        cell_list = []
        for row in self.grid.cells:
            for cell in row:
                adj_cells = self.grid.get_adjacent_cells(cell, DIRECTIONS)

                green_count = 4 - len(adj_cells)
                blue_count = 0

                if cell.color is None:
                    for adj_cell in adj_cells:
                        if adj_cell.color is GREEN:
                            green_count += 1
                        if adj_cell.color is BLUE:
                            blue_count += 1

                    if cell.number == 1:
                        if green_count > 1:
                            self.set_colors_and_append(cell, GREEN, cell_list)
                        elif blue_count > 1:
                            self.set_colors_and_append(cell, BLUE, cell_list)

                    if cell.number == 3:
                        if green_count > 1:
                            self.set_colors_and_append(cell, BLUE, cell_list)
                        elif blue_count > 1:
                            self.set_colors_and_append(cell, GREEN, cell_list)

                    if cell.number == 0:
                        if green_count >= 1:
                            self.set_colors_and_append(cell, GREEN, cell_list)
                        elif blue_count >= 1:
                            self.set_colors_and_append(cell, BLUE, cell_list)
        return cell_list
