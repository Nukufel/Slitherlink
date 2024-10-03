import pygame
import sys

CELL_SIZE = 20


class Line:
    def __init__(self, start, end):
        self.start = start  # Tuple (x, y)
        self.end = end      # Tuple (x, y)
        self.active = False # Whether the line is drawn or not

    def toggle(self):
        """Toggle the line on/off."""
        self.active = not self.active

    def draw(self, window, color= (50, 50, 255), width= 3):
        """Draw the line on the screen if it's active."""
        if self.active:
            pygame.draw.line(window, color,
                             (self.start[0] * CELL_SIZE, self.start[1] * CELL_SIZE),
                             (self.end[0] * CELL_SIZE, self.end[1] * CELL_SIZE), width)


class Cell:
    def __init__(self, row, col, number=None):
        self.row = row  # Row position of the cell
        self.col = col  # Column position of the cell
        self.number = number  # The number inside the cell (0, 1, 2, 3) or None

        # The four lines: top, right, bottom, left (clockwise)
        self.lines = {
            'top': None,
            'right': None,
            'bottom': None,
            'left': None
        }

    def set_lines(self, top, right, bottom, left):
        """Assign the four lines for the cell."""
        self.lines['top'] = top
        self.lines['right'] = right
        self.lines['bottom'] = bottom
        self.lines['left'] = left

    def is_satisfied(self):
        """Check if the number of active lines matches the cell's number."""
        active_lines = sum(line.active for line in self.lines.values())
        return active_lines == self.number if self.number is not None else True

    def draw(self, window):
        """Draw the number inside the cell."""
        if self.number is not None:
            font = pygame.font.SysFont(None, 36)
            num_surface = font.render(str(self.number), True, BLACK)
            window.blit(num_surface, (self.col * CELL_SIZE + CELL_SIZE // 2 - 10,
                                      self.row * CELL_SIZE + CELL_SIZE // 2 - 10))


# Initialize pygame
pygame.init()

# Set window dimensions
WIDTH, HEIGHT = 600, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slitherlink")

# Set the FPS (Frames Per Second)
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (50, 50, 255)

# Game clock
clock = pygame.time.Clock()

# Game Loop
def game_loop():
    running = True
    while running:
        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Game Logic Here

        # Draw Everything
        WINDOW.fill(WHITE)
        # draw_grid()  # Call this function to draw the game grid

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
