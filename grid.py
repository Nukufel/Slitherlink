from settings import CELL_SIZE, BLUE
from cell import Cell


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

        # self.make_puzzle()

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
        pass

    def get_start_green(self):
        start_greens = []
        for row in self.cells:
            for cell in row:
                if (cell.row in [0, self.rows - 1] or cell.col in [0, self.cols - 1]) and cell.color == GREEN:
                    start_greens.append(cell)
        return start_greens

    def all_connected(self, blue_count):
        found_greens = self.get_start_green()

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
