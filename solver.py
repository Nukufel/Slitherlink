from settings import DIRECTIONS, GRID_ROWS, GRID_COLS, BLUE, GREEN
from util import is_next_cell_valid

MAX_CELLS = GRID_ROWS * GRID_COLS
CORNERS = [(0,0),(0,GRID_COLS-1),(GRID_ROWS-1,0),(GRID_ROWS-1,GRID_COLS-1)]


class Solver:
    def __init__(self, grid):
        self.grid = grid
        self.cell_list = []
        self.clear_colors()
        self.cell_list.extend(self.scout_inside_patterns())
        self.cell_list.extend(self.scout_outside_patterns())
        self.search_patterns()

    def solve(self):
        cell = self.get_next_cell()
        if not cell:
            return True

        for color in [GREEN, BLUE]:
            if self.has_possible_amount_of_neighbours(cell, color):
                cell.color = color

                if self.solve():
                    return True

                cell.color = None
            self.cell_list.remove(cell)
        return False

    def search_patterns(self):

        print(f"cell_list start {len(self.cell_list)}")
        has_pattern = True

        while has_pattern:
            extend_list = []
            for cell in self.cell_list:
                print(f"cell {cell}")
                print(cell.row, cell.col)
                extend_list.extend(self.scout_pattern(cell, cell.color))
            if not extend_list:
                print("empty")
                has_pattern = False
            print(f"extend_list {len(extend_list)}")
            self.cell_list.extend(extend_list)
        print(f"cell_list {len(self.cell_list)}")

    def clear_colors(self):
        for row in self.grid.cells:
            for cell in row:
                cell.color = None

    def scout_outside_patterns(self):
        cell_list = []

        for row in self.grid.cells:
            for cell in row:
                if cell.number == 0:
                    if cell.row == 0 or cell.row == GRID_ROWS-1 or cell.col == 0 or cell.col == GRID_COLS-1:
                        cell.color = GREEN
                        cell_list.append(cell)
                if cell.number == 1:
                    pattern = (cell.row, cell.col)
                    if pattern in CORNERS:
                        cell.color = GREEN
                        cell_list.append(cell)
        return cell_list

    def scout_inside_patterns(self):
        cell_list = []
        diagonal_to_corner = {
            CORNERS[0]: (GRID_ROWS-(GRID_COLS-1), GRID_COLS-(GRID_COLS-1)),
            CORNERS[1]: (GRID_ROWS-(GRID_COLS-1), GRID_COLS-2),
            CORNERS[2]: (GRID_ROWS-2, GRID_COLS-(GRID_COLS-1)),
            CORNERS[3]: (GRID_ROWS-2, GRID_COLS-2)
        }
        for row in self.grid.cells:
            for cell in row:
                cords = (cell.row, cell.col)
                if cords in CORNERS:
                    if cell.number == 3:
                        cell.color = BLUE
                        self.append(cell_list, cell)
                    if cell.number == 2:
                        for key, pos in diagonal_to_corner.items():
                            if key == cords:
                                diagonal_cell = self.grid.cells[pos[0]][pos[1]]
                                if diagonal_cell.number == 3:
                                    adj_cells = self.grid.get_adjacent_cells(cell, DIRECTIONS)
                                    for adj_cell in adj_cells:
                                        adj_cell.color = BLUE
                                        self.append(cell_list, adj_cell)
                                    cell.color = BLUE
                                    self.append(cell_list, cell)
                                    diagonal_cell.color = GREEN
                                    self.append(cell_list, diagonal_cell)
        return cell_list

    def scout_pattern(self, cell, color):
        new_list = []
        for adjacent_cell in self.grid.get_adjacent_cells(cell, DIRECTIONS):
            cords = (cell.row, cell.col)
            cell_num = cell.number
            adj_num = adjacent_cell.number
            if cell_num == 0:
                adjacent_cell.color = cell.color
                self.append(new_list, adjacent_cell)
            if cords in CORNERS and cell_num == 1 and adj_num == 3:
                adjacent_cell.color = self.switch_color(color)
                self.append(new_list, adjacent_cell)
            if cell.number == 3 and adj_num == 3:
                adjacent_cell.color = self.switch_color(color)
                self.append(new_list, adjacent_cell)
            if cell_num == 1 and adj_num == 1:
                if cell.row == 0 or cell.row == GRID_ROWS-1 or cell.col == 0 or cell.col == GRID_COLS-1:
                    adjacent_cell.color = color
                    self.append(new_list, adjacent_cell)
            if adj_num == 0:
                adjacent_cell.color = color
                self.append(new_list, adjacent_cell)
            if adj_num == 3:
                direction = (adjacent_cell.row - cell.row, adjacent_cell.col - cell.col)
                one_direction = {"none": direction}
                adj_adj_cell = self.grid.get_adjacent_cells(adjacent_cell, one_direction)
                if adj_adj_cell and adj_adj_cell[0].number == 3:
                    adjacent_cell.color = self.switch_color(color)
                    self.append(new_list, adjacent_cell)
                    adj_adj_cell[0].color = color
                    self.append(new_list, adj_adj_cell)
        return new_list

    def append(self, new_list, cell):
        if cell not in new_list and cell not in self.cell_list:
            new_list.append(cell)

    def switch_color(self, color):
        if color == GREEN:
            return BLUE
        return GREEN

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

    def get_next_cell(self, last_cell=None):
        if not last_cell:
            return self.cell_list[0]
        for i, cell in enumerate(self.cell_list):
            if cell is last_cell and i+1 < len(self.cell_list):
                return self.cell_list[i+1]
            return None








