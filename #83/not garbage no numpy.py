EMPTY = '.'
# How many in succession it takes to win.
WIN_CONDITION = 3


def get_column(array: list, col_index: int) -> list:
    col = []
    for r in range(len(array)):
        col.append(array[r][col_index])
    return col


def get_diagonal(square_array: list):
    """ Grabs the diagonal of a square matrix """
    assert len(square_array) == len(square_array[0]), "Matrix length != matrix width!"
    di = []
    for r in range(len(square_array)):
        di.append(square_array[r][r])
    return di


def get_anti_diagonal(square_array: list):
    """ Grabs the anti-diagonal of a square matrix """
    assert len(square_array) == len(square_array[0]), "Matrix length != matrix width!"
    a_di = []
    s = len(square_array)
    for r in range(len(square_array)):
        a_di.append(square_array[r][s - 1 - r])
    return a_di


class Grid:
    def __init__(self):
        self.rows = 3
        self.cols = 3
        self.symbols = [[EMPTY for _ in range(self.cols)] for _ in range(self.rows)]

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
        if self.symbol * WIN_CONDITION == "".join(self.grid.symbols[self.played_row]):
            return True
        # vertical
        if self.symbol * WIN_CONDITION == "".join(get_column(self.grid.symbols, self.played_col)):
            return True
        # diagonal
        if self.symbol * WIN_CONDITION == "".join(get_diagonal(self.grid.symbols)):
            return True
        # anti-diagonal
        if self.symbol * WIN_CONDITION == "".join(get_anti_diagonal(self.grid.symbols)):
            return True
        return False

    def play(self, row_entered, col_entered):
        row_entered -= 1
        col_entered -= 1
        if not (0 <= row_entered < self.grid.rows) or not (0 <= col_entered < self.grid.cols):
            return False
        if grid.symbols[row_entered][col_entered] != EMPTY:
            return False
        self.grid.symbols[row_entered][col_entered] = self.symbol
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
            # restarts the game by re-initializing the objects.
            grid = Grid()
            player1 = Player('x', grid, 'player1')
            player2 = Player('o', grid, 'player2')
            print("Let's go again!")
            print(grid.draw_grid())
            # break: so that if player 1 wins, we don't ask player 2 for input when the game's over.
            break
