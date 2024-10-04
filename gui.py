import random

import pygame
import sys

CELL_SIZE = 20


class Cell:
    def __init__(self, row, col):
        self.row = row  # Row index
        self.col = col  # Column index
        self.color = GREEN

        # Borders: Whether each border is active (True or False)
        self.borders = {
            'top': None,
            'right': None,
            'bottom': None,
            'left': None
        }

        self.result = {
            'top': None,
            'right': None,
            'bottom': None,
            'left': None
        }

    def is_satisfied(self):
        true_boarders = [key for key in self.borders if self.borders[key] is True]
        true_results = [key for key in self.result if self.result[key] is True]
        if true_results == true_boarders:
            return True
        return False

    def toggle_border(self, border):
        """Toggle a specific border (top, right, bottom, left)."""
        if border in self.borders:
            if self.borders[border] is None:
                self.borders[border] = True
            elif self.borders[border] is True:
                self.borders[border] = False
            elif self.borders[border] is False:
                self.borders[border] = None

    def draw(self, window, offset_x=0, offset_y=0):
        """Draw the borders (active borders with thick lines) for the cell."""
        x = self.col * CELL_SIZE + offset_x
        y = self.row * CELL_SIZE + offset_y

        pygame.draw.line(window, BLACK, (x, y), (x + CELL_SIZE, y), 1)
        pygame.draw.line(window, BLACK, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 1)
        pygame.draw.line(window, BLACK, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 1)
        pygame.draw.line(window, BLACK, (x, y), (x, y + CELL_SIZE), 1)

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
            start1 = (x + CELL_SIZE/2 - 5, y - 5)
            end1 = (x + CELL_SIZE/2 + 5, y + 5)
            start2 = (x + CELL_SIZE/2 - 5, y + 5)
            end2 = (x + CELL_SIZE/2 + 5, y - 5)
            pygame.draw.line(window, RED, start1, end1, 4)
            pygame.draw.line(window, RED, start2, end2, 4)
        if self.borders['right'] is False:
            start1 = (x + CELL_SIZE - 5, y + CELL_SIZE/2 - 5)
            end1 = (x + CELL_SIZE + 5, y + CELL_SIZE/2 + 5)
            start2 = (x + CELL_SIZE + 5, y + CELL_SIZE / 2 - 5)
            end2 = (x + CELL_SIZE - 5, y + CELL_SIZE / 2 + 5)
            pygame.draw.line(window, RED, start1, end1, 4)
            pygame.draw.line(window, RED, start2, end2, 4)
        if self.borders['bottom'] is False:
            start1 = (x + CELL_SIZE/2 - 5, y + CELL_SIZE - 5)
            end1 = (x + CELL_SIZE/2 + 5, y + CELL_SIZE + 5)
            start2 = (x + CELL_SIZE/2 - 5, y + CELL_SIZE + 5)
            end2 = (x + CELL_SIZE/2 + 5, y + CELL_SIZE - 5)
            pygame.draw.line(window, RED, start1, end1, 4)
            pygame.draw.line(window, RED, start2, end2, 4)
        if self.borders['left'] is False:
            start1 = (x - 5, y + CELL_SIZE / 2 - 5)
            end1 = (x + 5, y + CELL_SIZE / 2 + 5)
            start2 = (x + 5, y + CELL_SIZE / 2 - 5)
            end2 = (x - 5, y + CELL_SIZE / 2 + 5)
            pygame.draw.line(window, RED, start1, end1, 4)
            pygame.draw.line(window, RED, start2, end2, 4)

        pygame.draw.line(window, self.color, (x,y), (x+CELL_SIZE, y+CELL_SIZE), 4)





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
        found_greens = [self.get_start_green()]
        blue_counter = 1
        ways = ("up", "right", "down", "left")

        next_cell = self.cells[random.randint(0, self.rows-1)][random.randint(0, self.cols-1)]
        next_cell.color = BLUE

        while True:
            blue_counter += 1
            way = random.choice(ways)

            match way:
                case "up":
                    try:
                        next_cell = self.cells[next_cell.row - 1][next_cell.col]
                        next_cell.color = BLUE
                    except:
                        pass
                case "right":
                    try:
                        next_cell = self.cells[next_cell.row][next_cell.col + 1]
                        next_cell.color = BLUE
                    except:
                        pass
                case "down":
                    try:
                        next_cell = self.cells[next_cell.row + 1][next_cell.col]
                        next_cell.color = BLUE
                    except:
                        pass
                case "left":
                    try:
                        next_cell = self.cells[next_cell.row][next_cell.col - 1]
                        next_cell.color = BLUE
                    except:
                        pass

    def get_start_green(self):
        row = random.choice([0, self.rows - 1])
        col = random.choice([0, self.cols - 1])

        if self.cells[row][col].color is not BLUE:
            return self.cells[row][col]
        else:
            return self.get_start_green()

    def get_all_connected(self, found_greens):
        for start_green in found_greens:
            try:
                if (self.cells[start_green.row - 1][start_green.col].color is GREEN and
                        self.cells[start_green.row - 1][start_green.col] not in found_greens):  # check up
                    found_greens.append(self.cells[start_green.row - 1][start_green.col])
            except:
                pass

            try:
                if (self.cells[start_green.row][start_green.col + 1].color is GREEN and
                        self.cells[start_green.row][start_green.col + 1] not in found_greens):  # check right
                    found_greens.append(self.cells[start_green.row][start_green.col + 1])
            except:
                pass

            try:
                if (self.cells[start_green.row + 1][start_green.col].color is GREEN and
                        self.cells[start_green.row + 1][start_green.col] not in found_greens):  # check down
                    found_greens.append(self.cells[start_green.row][start_green.col + 1])
            except:
                pass

            try:
                if (self.cells[start_green.row][start_green.col - 1].color is GREEN and
                        self.cells[start_green.row][start_green.col - 1] not in found_greens):  # check left
                    found_greens.append(self.cells[start_green.row][start_green.col + 1])
            except:
                pass

        print(len(found_greens))







# Initialize pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 800, 800  # Larger window
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Centered Slitherlink Grid")

# Frame rate settings
FPS = 60
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Cell and Grid size
CELL_SIZE = 50
GRID_ROWS, GRID_COLS = 10, 10

# Padding around the grid to prevent border cutoff
PADDING = 10  # Add some padding around the grid

# Calculate grid surface size with padding
GRID_WIDTH = GRID_COLS * CELL_SIZE + PADDING * 2
GRID_HEIGHT = GRID_ROWS * CELL_SIZE + PADDING * 2

# Create a grid object
grid = Grid(GRID_ROWS, GRID_COLS)



def game_loop():
    running = True

    # Create a separate surface for the grid with padding
    grid_surface = pygame.Surface((GRID_WIDTH, GRID_HEIGHT))

    # Calculate position to center the grid_surface in the main window
    grid_x = (WIDTH - GRID_WIDTH) // 2
    grid_y = (HEIGHT - GRID_HEIGHT) // 2

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Convert mouse coordinates to grid_surface coordinates
                relative_mouse_pos = (mouse_pos[0] - grid_x - PADDING, mouse_pos[1] - grid_y - PADDING)

                # Only handle clicks inside the grid surface
                if 0 <= relative_mouse_pos[0] <= GRID_WIDTH - PADDING * 2 and 0 <= relative_mouse_pos[
                    1] <= GRID_HEIGHT - PADDING * 2:
                    grid.handle_click(relative_mouse_pos)

        # Fill the main window with a white background
        WINDOW.fill(WHITE)

        # Fill the grid surface with a white background before drawing the grid
        grid_surface.fill(WHITE)

        # Draw the grid onto the grid_surface, adjusted by PADDING
        grid.draw(grid_surface, offset_x=PADDING, offset_y=PADDING)

        # Blit (draw) the grid_surface onto the main window at the calculated position
        WINDOW.blit(grid_surface, (grid_x, grid_y))

        # Update the display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    game_loop()

