import numpy as np


EMPTY = '.'


def anti_diagonal(array: np.array):
    return np.fliplr(array).diagonal()


class Grid:
    def __init__(self):
        self.rows = 3
        self.cols = 3
        self.symbols = [[EMPTY for _ in range(self.cols)] for _ in range(self.rows)]
        self.symbols = np.array(self.symbols)

    def draw_grid(self):
        string = ""
        for r in range(self.rows):
            for c in range(self.cols):
                string += self.symbols[r][c] + " | "
            string = string[:-3]
            string += "\n"
        return string[:-1]


class Player:
    def __init__(self, symbol: chr, playing_grid: Grid, name: str):
        self.symbol = symbol
        self.grid = playing_grid
        self.name = name
        self.played_row = -1
        self.played_col = -1

    def check_win(self):
        # horizontal
        if self.symbol * 3 == "".join(self.grid.symbols[self.played_row]):
            return True
        # vertical
        if self.symbol * 3 == "".join(self.grid.symbols[:, self.played_col]):
            return True
        # diagonal
        if self.symbol * 3 == "".join(self.grid.symbols.diagonal()):
            return True
        # anti-diagonal
        if self.symbol * 3 == "".join(anti_diagonal(self.grid.symbols)):
            return True
        return False

    def play(self, row_entered, col_entered):
        row_entered -= 1
        col_entered -= 1
        if not (0 <= row_entered < self.grid.rows) or not (0 <= col_entered < self.grid.cols):
            return False
        if grid.symbols[row_entered, col_entered] != EMPTY:
            return False
        self.grid.symbols[row_entered, col_entered] = self.symbol
        self.played_row = row_entered
        self.played_col = col_entered
        return True


# noinspection PyShadowingNames
def take_player_input(player: Player):
    row = input(f"Give me a row, {player.name}! ")
    column = input(f"Give me a column, {player.name}! ")
    row, column = int(row), int(column)
    if not player.play(row, column):
        print("Invalid input. Try again! ")
        take_player_input(player)
    else:
        print("Outstanding move.")


grid = Grid()
player1 = Player('x', grid, 'player1')
player2 = Player('o', grid, 'player2')

print(grid.draw_grid())
while True:
    for player in [player1, player2]:
        take_player_input(player)
        print(grid.draw_grid())
        if player.check_win():
            print("We have a winner! ")
            grid = Grid()
            player1 = Player('x', grid, 'player1')
            player2 = Player('o', grid, 'player2')
            print("Let's go again!")
            print(grid.draw_grid())
            # break: so that if player 1 wins, we don't ask player 2 for input when the game's over.
            break
