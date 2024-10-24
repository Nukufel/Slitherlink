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
        # directions = ["top", "right", "bottom", "left"]
        directions = [(-1,0), (0,1), (1,0), (0,-1)]
        projected_blue_count = (int)(CELL_COUNT * random.randint(56, 60)/100)
        print(projected_blue_count)

        first_blue = self.cells[random.randint(0, self.rows-1)][random.randint(0, self.cols-1)]
        first_blue.color = BLUE
        blue_cells = [first_blue]

        failed_count = 0

        # TODO more elegant way for failed_count
        while len(blue_cells) < projected_blue_count and failed_count < 10000:
            random_blue = random.choice(blue_cells)

            adjacent_cells = self.get_adjacent_cells(random_blue, directions)
            weights = self.weight_cell(adjacent_cells, directions)
            adjacent_weighted_cells = {}

            for i, adjacent_cell in enumerate(adjacent_cells):
                if weights[i] > 60:
                    adjacent_weighted_cells[adjacent_cell] = weights[i]

            if len(adjacent_weighted_cells) > 0:
                keys = list(adjacent_weighted_cells.keys())
                values = list(adjacent_weighted_cells.values())

                random_cell = random.choices(keys, weights=values, k=1)[0]

                if random_cell not in blue_cells:
                    random_cell.color = BLUE
                    if self.all_connected(len(blue_cells)+1):
                        failed_count = 0
                        blue_cells.append(random_cell)
                    else:
                        random_cell.color = GREEN
            else:
                failed_count += 1

    def get_adjacent_cells(self, base_cell, directions):
        next_cells = []
        for direction in directions:
            if (not (base_cell.row == 0 and direction[0] == -1) and
                    not (base_cell.col == 0 and direction[1] == -1) and
                    not (base_cell.row == self.rows - 1 and direction[0] == 1) and
                    not (base_cell.col == self.cols - 1 and direction[1] == 1)):
                row = base_cell.row + direction[0]
                col = base_cell.col + direction[1]
                next_cells.append(self.cells[row][col])
        return next_cells

    def weight_cell(self, cells, directions):
        scores = []
        for cell in cells:
            score = 100
            adjacent_cells = self.get_adjacent_cells(cell, directions)
            for adjacent_cell in adjacent_cells:
                if adjacent_cell.color == BLUE:
                    score -= 20
            # TODO somehow avoid long straight lines
            scores.append(score)
        return scores

    def check_straight_lines(self, cell, direction):
        match direction:
            case (-1, 0): # top
                pass
            case (0, 1): # left
                pass
            case (1, 0): # down
                pass
            case (0, -1):
                pass

    def get_start_greens(self):
        start_greens = []
        for row in self.cells:
            for cell in row:
                if (cell.row in [0, self.rows - 1] or cell.col in [0, self.cols - 1]) and cell.color == GREEN:
                    start_greens.append(cell)
        return start_greens

    def all_connected(self, blue_count):
        found_greens = self.get_start_greens()

        for start_green in found_greens:
            try:
                if (self.cells[start_green.row - 1][start_green.col].color is not BLUE and
                        self.cells[start_green.row - 1][start_green.col] not in found_greens):  # check up
                    found_greens.append(self.cells[start_green.row - 1][start_green.col])
            except:
                pass

            try:
                if (self.cells[start_green.row][start_green.col + 1].color is not BLUE and
                        self.cells[start_green.row][start_green.col + 1] not in found_greens):  # check right
                    found_greens.append(self.cells[start_green.row][start_green.col + 1])
            except:
                pass

            try:
                if (self.cells[start_green.row + 1][start_green.col].color is not BLUE and
                        self.cells[start_green.row + 1][start_green.col] not in found_greens):  # check down
                    found_greens.append(self.cells[start_green.row + 1][start_green.col])
            except:
                pass

            try:
                if (self.cells[start_green.row][start_green.col - 1].color is not BLUE and
                        self.cells[start_green.row][start_green.col - 1] not in found_greens):  # check left
                    found_greens.append(self.cells[start_green.row][start_green.col - 1])
            except:
                pass

        max_cells = self.rows * self.cols

        if max_cells - blue_count == len(found_greens):
            return True
        return False
