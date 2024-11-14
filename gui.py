from settings import WIDTH, HEIGHT, GRID_COLS, GRID_ROWS, CELL_SIZE, PADDING, FPS, WHITE
from grid import Grid
import pygame
import sys


# Initialize pygame
pygame.init()

# Window settings
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Centered Slitherlink Grid")

# Frame rate settings
clock = pygame.time.Clock()

# Calculate grid surface size with padding
GRID_WIDTH = GRID_COLS * CELL_SIZE + PADDING * 2
GRID_HEIGHT = GRID_ROWS * CELL_SIZE + PADDING * 2

# Create a grid object
grid = Grid()


def game_loop():
    running = True

    # Create a separate surface for the grid with padding
    grid_surface = pygame.Surface((GRID_WIDTH, GRID_HEIGHT))

    # Calculate position to center the grid_surface in the main window
    grid_x = (WIDTH - GRID_WIDTH) // 2
    grid_y = (HEIGHT - GRID_HEIGHT) // 2

    while running:
        if grid.is_solved():
            print("Puzzle solved!")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Convert mouse coordinates to grid_surface coordinates
                relative_mouse_pos = (mouse_pos[0] - grid_x - PADDING, mouse_pos[1] - grid_y - PADDING)

                # Only handle clicks inside the grid surface
                if (0 <= relative_mouse_pos[0] <= GRID_WIDTH - PADDING * 2 and
                        0 <= relative_mouse_pos[1] <= GRID_HEIGHT - PADDING * 2):
                    grid.handle_click(relative_mouse_pos)


        # Fill the main window with a white background
        WINDOW.fill(WHITE)

        # Fill the grid surface with a white background before drawing the grid
        grid_surface.fill(WHITE)

        # Draw the grid onto the grid_surface, adjusted by PADDING
        grid.draw_grid(grid_surface, offset_x=PADDING, offset_y=PADDING)

        # Blit (draw) the grid_surface onto the main window at the calculated position
        WINDOW.blit(grid_surface, (grid_x, grid_y))

        # Update the display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    game_loop()
