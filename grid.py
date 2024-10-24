from settings import CELL_SIZE, BLUE, GREEN, GRID_COLS, GRID_ROWS
from cell import Cell
import random


CELL_COUNT = GRID_COLS * GRID_ROWS


class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cells = []

        # Create the grid
        self.create_grid()

    def create_grid(self):
        """Create a grid with cells."""
        for row in range(self.rows):
            cell_row = []
            for col in range(self.cols):
                cell = Cell(row, col)
                cell_row.append(cell)
            self.cells.append(cell_row)

        self.make_puzzle()

    def draw(self, window, offset_x=0, offset_y=0):
        """Draw all the cells with a provided offset."""
        for row in self.cells:
            for cell in row:
                cell.draw(window, offset_x, offset_y)

    def handle_click(self, pos):
        """Handle clicks and toggle the nearest border of a cell."""
        x, y = pos
        col, row = x // CELL_SIZE, y // CELL_SIZE

        if row < self.rows and col < self.cols:
            cell = self.cells[row][col]
            cell_x, cell_y = col * CELL_SIZE, row * CELL_SIZE

            # Find the distance to each border
            distances = {
                'top': abs(y - cell_y),
                'right': abs(x - (cell_x + CELL_SIZE)),
                'bottom': abs(y - (cell_y + CELL_SIZE)),
                'left': abs(x - cell_x)
            }

            # Find the nearest border (minimum distance)
            nearest_border = min(distances, key=distances.get)

            # Toggle the nearest border
            cell.toggle_border(nearest_border)

            if nearest_border == "top" and row != 0:
                adjacent_cell = self.cells[row - 1][col]
                adjacent_cell.toggle_border("bottom")
            if nearest_border == "bottom" and row != self.rows - 1:
                adjacent_cell = self.cells[row + 1][col]
                adjacent_cell.toggle_border("top")
            if nearest_border == "left" and col != 0:
                adjacent_cell = self.cells[row][col - 1]
                adjacent_cell.toggle_border("right")
            if nearest_border == "right" and col != self.cols - 1:
                adjacent_cell = self.cells[row][col + 1]
                adjacent_cell.toggle_border("left")

    def make_puzzle(self):
        directions = {
            "top": (-1, 0),
            "right": (0, 1),
            "bottom": (1, 0),
            "left": (0, -1)
        }

        projected_blue_count = int(CELL_COUNT * random.randint(56, 60) / 100)

        first_blue = self.cells[random.randint(0, self.rows-1)][random.randint(0, self.cols-1)]
        first_blue.color = BLUE
        blue_cells = [first_blue]

        failed_count = 0

        # TODO more elegant way for failed_count
        while len(blue_cells) < projected_blue_count and failed_count < 20000:
            random_blue = random.choice(blue_cells)

            adjacent_cells = self.get_adjacent_cells(random_blue, directions)
            weights = self.weight_cell(adjacent_cells, directions, random_blue)
            adjacent_weighted_cells = {}

            for i, adjacent_cell in enumerate(adjacent_cells):
                if weights[i] > 50:
                    adjacent_weighted_cells[adjacent_cell] = weights[i]

            if len(adjacent_weighted_cells) > 0:
                keys = list(adjacent_weighted_cells.keys())
                values = list(adjacent_weighted_cells.values())

                random_cell = random.choices(keys, weights=values, k=1)[0]

                if random_cell not in blue_cells:
                    random_cell.color = BLUE
                    if self.all_connected(len(blue_cells)+1, directions):
                        failed_count = 0
                        blue_cells.append(random_cell)
                    else:
                        random_cell.color = GREEN
            else:
                failed_count += 1

        self.set_numbers_for_cells(directions)


    def is_next_cell_valid(self, cell, direction):
        if (not (cell.row == 0 and direction[0] == -1) and
                not (cell.col == 0 and direction[1] == -1) and
                not (cell.row == self.rows - 1 and direction[0] == 1) and
                not (cell.col == self.cols - 1 and direction[1] == 1)):
            return True
        return False

    def get_adjacent_cells(self, cell, directions):
        next_cells = []
        for direction in directions.values():
            if self.is_next_cell_valid(cell, direction):
                row = cell.row + direction[0]
                col = cell.col + direction[1]
                next_cells.append(self.cells[row][col])
        return next_cells

    def weight_cell(self, cells, directions, base_cell):
        scores = []
        for cell in cells:
            score = 100
            adjacent_cells = self.get_adjacent_cells(cell, directions)
            for adjacent_cell in adjacent_cells:
                if adjacent_cell.color == BLUE:
                    score -= 20
            score -= self.calc_consecutive_blues(cell, base_cell) * 5
            score += random.randint(-5, 5)
            if score < 0:
                score = 0
            scores.append(score)
        return scores

    def calc_consecutive_blues(self, cell, base_cell):
        count = 1
        opposite_direction = (base_cell.row - cell.row, base_cell.col - cell.col)
        next_cell = cell
        while True:
            if not self.is_next_cell_valid(next_cell, opposite_direction):
                break
            next_cell = self.cells[next_cell.row + opposite_direction[0]][next_cell.col + opposite_direction[1]]
            if next_cell.color == BLUE:
                count += 1
            else:
                break
        return count

    def get_start_greens(self):
        start_greens = []
        for row in self.cells:
            for cell in row:
                if (cell.row in [0, self.rows - 1] or cell.col in [0, self.cols - 1]) and cell.color == GREEN:
                    start_greens.append(cell)
        return start_greens

    def all_connected(self, blue_count, directions):
        found_greens = self.get_start_greens()

        for start_green in found_greens:
            for d_row, d_col in directions.values():
                try:
                    adj_cell = self.cells[start_green.row + d_row][start_green.col + d_col]
                    if adj_cell.color != BLUE and adj_cell not in found_greens:
                        found_greens.append(adj_cell)
                except IndexError:
                    pass

        max_cells = self.rows * self.cols
        return max_cells - blue_count == len(found_greens)

    def set_numbers_for_cells(self, directions):
        for row in self.cells:
            for cell in row:
                if cell.color == BLUE:
                    for direction_name, direction in directions.items():
                        one_direction = {direction_name: direction}
                        adjacent_cell = self.get_adjacent_cells(cell, one_direction)
                        if (adjacent_cell and adjacent_cell[0].color == GREEN) or not adjacent_cell:
                            cell.result[direction_name] = True
                            cell.borders[direction_name] = True     # TODO remove this line
