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
        self.search_patterns()

    def clear_colors(self):
        for row in self.grid.cells:
            for cell in row:
                cell.color = None

    # rewrite
    def is_possible_solution(self):
        for cell in self.cell_list:
            if cell.number:
                adj_cells = self.grid.get_adjacent_cells(cell, DIRECTIONS)
                green_count = 4 - len(adj_cells)
                blue_count = 0
                for adj_cell in adj_cells:
                    if adj_cell.color == GREEN:
                        green_count += 1
                    elif adj_cell.color == BLUE:
                        blue_count += 1
                if not green_count <= cell.number or not blue_count <= cell.number:
                    return False
        if not self.can_blue_be_connected():
            return False
        return True

    def is_blue_connected(self):
        start_blue = None
        all_blues = []
        for row in self.grid.cells:
            for cell in row:
                if cell.color == BLUE and not start_blue:
                    start_blue = cell
                if cell.color == BLUE:
                    all_blues.append(cell)

        connected_blue = self.get_all_connected_blue([start_blue])
        if len(connected_blue) == len(all_blues):
            return True

    def get_all_connected_blue(self, blue_cells):
        connected_blue = []
        for blue_cell in blue_cells:
            adj_cells = self.grid.get_adjacent_cells(blue_cell, DIRECTIONS)
            for adj_cell in adj_cells:
                if adj_cell.color == BLUE:
                    self.append(connected_blue, adj_cell)
                    return self.get_all_connected_blue(connected_blue)
        return connected_blue

    def can_blue_be_connected(self):
        start_blue = None
        for row in self.grid.cells:
            for cell in row:
                if cell.color == BLUE and not start_blue:
                    start_blue = cell
                    break
        possible_blue = self.get_all_connected_blue([start_blue])
        if len(possible_blue) + len(self.get_all_greens()) == MAX_CELLS:
            return True
        return False

    def get_all_possible_blue(self, not_green_cells):
        connected_blue = []
        for not_green_cell in not_green_cells:
            adj_cells = self.grid.get_adjacent_cells(not_green_cell, DIRECTIONS)
            for adj_cell in adj_cells:
                if adj_cell.color != GREEN:
                    self.append(connected_blue, adj_cell)
                    return self.get_all_connected_blue(connected_blue)
        return connected_blue

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
    def solve(self):
        possible_cells = []
        cell = self.get_next_uncolored_cell()

        if not cell:
            return True

        for color in [GREEN, BLUE]:

            self.set_colors_and_append(cell, color, self.cell_list)
            possible_cells.append(cell)
            possible_cells.extend(self.search_patterns())

            if self.is_possible_solution():
                if self.solve():
                    return True

            for cell in possible_cells:
                self.cell_list.remove(cell)
                cell.color = None
                possible_cells = []

        return False

    def search_patterns(self):
        has_pattern = True
        extend_list = []
        while has_pattern:
            temp_list = []
            for cell in self.cell_list:
                temp_list.extend(self.solve_1_and_3_by_colors())
                temp_list.extend(self.scout_pattern(cell, cell.color))
            if not temp_list:
                has_pattern = False
            self.cell_list.extend(temp_list)
            extend_list.extend(temp_list)
        return extend_list

    def set_colors_and_append(self, cell, color, new_list):
        if self.append(new_list, cell):
            cell.color = color

    def append(self, new_list, cell):
        if cell not in new_list and cell not in self.cell_list:
            new_list.append(cell)
            return True
        return False

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
            CORNERS[0]: (GRID_ROWS-(GRID_COLS-1), GRID_COLS-(GRID_COLS-1)),
            CORNERS[1]: (GRID_ROWS-(GRID_COLS-1), GRID_COLS-2),
            CORNERS[2]: (GRID_ROWS-2, GRID_COLS-2),
            CORNERS[3]: (GRID_ROWS-2, GRID_COLS-(GRID_COLS-1))
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

    def get_row_of_1_from_corner(self, cell, my_list):
        adj_cell = self.has_specific_adjacent_cell(cell, 1)
        if adj_cell and self.is_border_cell(adj_cell) and adj_cell not in my_list:
            self.set_colors_and_append(adj_cell, GREEN, my_list)
            self.get_row_of_1_from_corner(adj_cell, my_list)

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

    def scout_pattern(self, cell, color):
        new_list = []

        for adjacent_cell in self.grid.get_adjacent_cells(cell, DIRECTIONS):
            if cell.color is not None or adjacent_cell.color is not None:
                cell_num = cell.number
                adj_num = adjacent_cell.number

                if cell_num == 0:
                    adjacent_cell.color = cell.color
                    self.append(new_list, adjacent_cell)

                if adj_num == 0:
                    adjacent_cell.color = color
                    self.append(new_list, adjacent_cell)

                if self.is_corner(cell) and cell_num == 1 and adj_num == 3:
                    adjacent_cell.color = switch_color(color)
                    self.append(new_list, adjacent_cell)

                if cell_num == 3 and adj_num == 3:
                    adjacent_cell.color = switch_color(color)
                    self.append(new_list, adjacent_cell)

                if cell_num == 1 and adj_num == 1 and self.is_border_cell(cell):
                    adjacent_cell.color = color
                    self.append(new_list, adjacent_cell)
        return new_list

    def solve_1_and_3_by_colors(self):
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
        return cell_list
