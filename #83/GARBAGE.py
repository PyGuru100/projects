class Player:
    def __init__(self, symbol):
        self.symbol = symbol
        self.positions = []
        self.grid = None

    def check_win(self):
        # horizontal line
        for row in range(3):
            winning_row = True
            for col in range(3):
                if f'({row}, {col})' not in self.positions:
                    winning_row = False
                    break
            if winning_row:
                return True
        # vertical line
        for col in range(3):
            winning_col = True
            for row in range(3):
                if f'({row}, {col})' not in self.positions:
                    winning_col = False
                    break
            if winning_col:
                return True
        # diagonal line 0, 0 | 1, 1 | 2, 2
        winning = True
        for i in range(3):
            if f'({i}, {i})' not in self.positions:
                winning = False
                break
        if winning:
            return True
        # diagonal line 0, 2 | 1, 1 | 2, 1
        winning = True
        for j in range(3):
            if f'({j}, {2 - j})' not in self.positions:
                winning = False
                break
        if winning:
            return True
        return False


class Grid:
    def __init__(self):
        self.rows = 3
        self.cols = 3
        self.symbols = [['' for _ in range(self.cols)] for _ in range(self.rows)]

    def draw_grid(self):
        string = ""
        for r in range(self.rows):
            for c in range(self.cols):
                string += self.symbols[r][c] + " | "
            string = string[:-3]
            string += ".\n"
        return string[:-1]


grid = Grid()
print(grid.symbols)
print(grid.draw_grid())
player1 = Player('x')
player1.positions += ['(1, 0)', '(1, 1)', '(1, 2)']
print(player1.check_win())
