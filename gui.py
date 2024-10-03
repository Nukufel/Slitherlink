import pygame
import sys

CELL_SIZE = 20


class Cell:
    def __init__(self, row, col):
        self.row = row  # Row index
        self.col = col  # Column index

        # Borders: Whether each border is active (True or False)
        self.borders = {
            'top': None,
            'right': None,
            'bottom': None,
            'left': None
        }

    def toggle_border(self, border):
        """Toggle a specific border (top, right, bottom, left)."""
        if border in self.borders:
            if self.borders[border] is None:
                self.borders[border] = True
            elif self.borders[border] is True:
                self.borders[border] = False
            elif self.borders[border] is False:
                self.borders[border] = None

    def draw(self, window):
        """Draw the borders (active borders with thick lines) for the cell."""
        x, y = self.col * CELL_SIZE, self.row * CELL_SIZE

        # Draw borders (thicker lines for active borders)
        if self.borders['top']:
            pygame.draw.line(window, BLACK, (x, y), (x + CELL_SIZE, y), 4)
        if self.borders['right']:
            pygame.draw.line(window, BLACK, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 4)
        if self.borders['bottom']:
            pygame.draw.line(window, BLACK, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 4)
        if self.borders['left']:
            pygame.draw.line(window, BLACK, (x, y), (x, y + CELL_SIZE), 4)
        if self.borders['top'] is False:
            pygame.draw.line(window, RED, (x, y), (x + CELL_SIZE, y), 4)
        if self.borders['right'] is False:
            pygame.draw.line(window, RED, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 4)
        if self.borders['bottom'] is False:
            pygame.draw.line(window, RED, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 4)
        if self.borders['left'] is False:
            pygame.draw.line(window, RED, (x, y), (x, y + CELL_SIZE), 4)


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

    def draw(self, window):
        """Draw all the cells."""
        for row in self.cells:
            for cell in row:
                cell.draw(window)


# Initialize pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 600, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dynamic Slitherlink")

# Frame rate settings
FPS = 60
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Cell and Grid size
CELL_SIZE = 100

# Create a grid object
grid = Grid(5, 5)


def game_loop():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                grid.handle_click(mouse_pos)

        # Fill the screen with a white background
        WINDOW.fill(WHITE)

        # Draw the grid of cells
        grid.draw(WINDOW)

        # Update the display with the latest changes
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    game_loop()