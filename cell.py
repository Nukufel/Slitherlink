from settings import GREEN, BLACK, RED, CELL_SIZE
import pygame


class Cell:
    def __init__(self, row, col):
        self.row = row  # Row index
        self.col = col  # Column index
        self.number = None
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

    def calc_number(self):
        count = 0
        for value in self.result.values():
            if value:
                count += 1
        return count

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
        self.number = self.calc_number()
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

        # Draw crosses for inactive borders
        if self.borders['top'] is False:
            start1 = (x + CELL_SIZE / 2 - 5, y - 5)
            end1 = (x + CELL_SIZE / 2 + 5, y + 5)
            start2 = (x + CELL_SIZE / 2 - 5, y + 5)
            end2 = (x + CELL_SIZE / 2 + 5, y - 5)
            pygame.draw.line(window, RED, start1, end1, 4)
            pygame.draw.line(window, RED, start2, end2, 4)
        if self.borders['right'] is False:
            start1 = (x + CELL_SIZE - 5, y + CELL_SIZE / 2 - 5)
            end1 = (x + CELL_SIZE + 5, y + CELL_SIZE / 2 + 5)
            start2 = (x + CELL_SIZE + 5, y + CELL_SIZE / 2 - 5)
            end2 = (x + CELL_SIZE - 5, y + CELL_SIZE / 2 + 5)
            pygame.draw.line(window, RED, start1, end1, 4)
            pygame.draw.line(window, RED, start2, end2, 4)
        if self.borders['bottom'] is False:
            start1 = (x + CELL_SIZE / 2 - 5, y + CELL_SIZE - 5)
            end1 = (x + CELL_SIZE / 2 + 5, y + CELL_SIZE + 5)
            start2 = (x + CELL_SIZE / 2 - 5, y + CELL_SIZE + 5)
            end2 = (x + CELL_SIZE / 2 + 5, y + CELL_SIZE - 5)
            pygame.draw.line(window, RED, start1, end1, 4)
            pygame.draw.line(window, RED, start2, end2, 4)
        if self.borders['left'] is False:
            start1 = (x - 5, y + CELL_SIZE / 2 - 5)
            end1 = (x + 5, y + CELL_SIZE / 2 + 5)
            start2 = (x + 5, y + CELL_SIZE / 2 - 5)
            end2 = (x - 5, y + CELL_SIZE / 2 + 5)
            pygame.draw.line(window, RED, start1, end1, 4)
            pygame.draw.line(window, RED, start2, end2, 4)

        pygame.draw.line(window, self.color, (x, y), (x + CELL_SIZE, y + CELL_SIZE), 4)
        self.draw_number(window, x, y)

    def draw_number(self, window, x, y):
        """Draw the number in the middle of the cell."""
        font = pygame.font.SysFont(None, 24)
        text = font.render(str(self.number), True, BLACK)
        text_rect = text.get_rect(center=(x + CELL_SIZE / 2, y + CELL_SIZE / 2))
        window.blit(text, text_rect)