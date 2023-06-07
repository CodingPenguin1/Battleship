import contextlib
import random


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
        while True:
            try:
                cell = input(f'{self.name}, enter a cell to shoot (e.g. A5): ')
                # TODO: account for larger boards
                if len(cell) != 2 or not cell[0].isalpha() or not cell[1].isdigit():
                    raise ValueError('Invalid cell')  # TODO: Make this not error
                row, col = board.cell_to_row_col(cell)
                print(row, col)
                board.shoot(row, col)
                break
            except ValueError as err:
                print(err)


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

