
VALID_COMBINATIONS = {
    0: [],
    1: [["top"], ["bottom"], ["left"], ["right"]],
    2: [["top", "bottom"], ["left", "right"], ["top", "right"], ["top", "left"], ["bottom", "left"], ["bottom", "right"]],
    3: [["top", "bottom", "left"], ["top", "bottom", "right"], ["top", "left", "right"], ["bottom", "left", "right"]],
}


class Solver:
    def __init__(self, grid):
        self.grid = grid

    def remove_number(self):
        pass

    def solve(self):
        for row in self.grid.cells:
            for cell in row:
                combinations = VALID_COMBINATIONS[cell.number]
                for combination in combinations:
                    self.set_boarders_and_crosses(combination, cell)
                    if not self.check_valid_cell(cell):
                        #do some backtracking
                        pass

    def check_valid_cell(self, cell):
        for key, value in cell.boarders.items():
            if value:
                r = cell.row
                c = cell.col
                positions = None
                match key:
                    case "top":
                        positions = {
                                (r-1, c): ("left", "right"),
                                (r, c-1): ("top", "right"),
                                (r, c+1): ("top", "left"),
                                (r, c): ("right", "left")
                            }
                        pass
                    case "left":
                        positions = {
                            (r-1, c): ("left", "bottom"),
                            (r, c-1): ("top", "bottom"),
                            (r+1, c): ("top", "left"),
                            (r, c): ("top", "bottom")
                        }

                    case "bottom":
                        positions = {
                            (r, c): ("left", "right"),
                            (r, c-1): ("right", "bottom"),
                            (r, c+1): ("bottom", "left"),
                            (r-1, c): ("left", "right")
                        }
                    case "right":
                        positions = {
                            (r-1, c): ("right", "bottom"),
                            (r, c+1): ("top", "bottom"),
                            (r+1, c): ("top", "right"),
                            (r, c): ("top", "bottom")
                        }

                return self.has_possible_boarder(cell, positions)

    def has_possible_boarder(self, cell, positions):
        for key, value in positions.items():
            if self.grid.is_next_cell_valid(cell, key):
                next_cell = self.grid.cells[key[0]][key[1]]
                for pos in value:
                    if next_cell.boarders[pos] != False:
                        return True
        return False

    def set_boarders_and_crosses(self, combination, cell):
        for pos in combination:
            cell.borders[pos] = True
            for boarder in cell.borders:
                if not cell.borders[boarder]:
                    cell.borders[boarder] = False




