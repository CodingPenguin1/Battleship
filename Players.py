import contextlib
import random

from colorama import Fore


class Player:
    def __init__(self, name):
        self.name = name

    def shoot(self, board):
        raise NotImplementedError('You need to implement this method in a subclass')

    def __repr__(self):
        return f'Player({self.name!r})'


class HumanPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    def shoot(self, board):
        error_printed = False
        while True:
            cell = input(f'{self.name}, enter a cell to shoot (e.g. A5): ')
            valid_format = True
            if not cell[0].isalpha():
                valid_format = False
            if not cell[1:].isdigit():
                valid_format = False

            if valid_format:
                row, col = board.cell_to_row_col(cell)
                board.shoot(row, col)
                break
            else:
                if not error_printed:
                    print(f'{Fore.RED}Invalid format. Please enter a cell in the format A5{Fore.RESET}')
                    error_printed = True


class RandomPlayer(Player):
    def __init__(self, name=None):
        if name is None:
            name = 'Random Player'
        super().__init__(name)

    def shoot(self, board):
        while True:
            row = random.randrange(board.height)
            col = random.randrange(board.width)
            with contextlib.suppress(ValueError):
                board.shoot(row, col)
                break

