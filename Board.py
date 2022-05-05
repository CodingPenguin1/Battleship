import itertools
from random import choice, randint


class Board:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.grid = [[{'shot': False, 'ship': None} for _ in range(width)] for _ in range(height)]

    def place_ship(self, row: int, col: int, orientation: str, length: int, ship_name: str):
        # Figure out how to itarate through row or col depending on what orientation is
        row_increment, col_increment = 0, 0
        if orientation.lower() == 'r':
            col_increment = 1
        elif orientation.lower() == 'l':
            col_increment = -1
        elif orientation.lower() == 'u':
            row_increment = -1
        elif orientation.lower() == 'd':
            row_increment = 1

        # Check to see if placement is valid
        valid = True

        # If the ship will be placed off the board, invalid
        if orientation == 'r' and col + length > self.width:
            return False
        elif orientation == 'l' and col - length < -1:
            return False
        elif orientation == 'u' and row - length < -1:
            return False
        elif orientation == 'd' and row + length > self.height:
            return False

        # If overlapping another ship, invalid
        cur_row, cur_col = row, col
        while abs(cur_row - row) < length and abs(cur_col - col) < length:
            if self.grid[cur_row][cur_col]['ship'] is not None:
                return False
            cur_row += row_increment
            cur_col += col_increment

        # If valid, place ship
        cur_row, cur_col = row, col
        while abs(cur_row - row) < length and abs(cur_col - col) < length:
            self.grid[cur_row][cur_col]['ship'] = ship_name
            cur_row += row_increment
            cur_col += col_increment
        return True

    def place_ships_randomly(self, ships=None):
        if ships is None:
            ships = {'carrier': 5, 'battleship': 4, 'cruiser': 3, 'submarine': 3, 'destroyer': 2}

        for ship_name, length in ships.items():
            while True:
                orientation = choice(['r', 'l', 'u', 'd'])
                row = randint(0, self.height - 1)
                col = randint(0, self.width - 1)
                if self.place_ship(row, col, orientation, length, ship_name):
                    break

    def shoot(self, row: int, col: int):
        if self.grid[row][col]['shot']:
            return False
        self.grid[row][col]['shot'] = True
        if self.grid[row][col]['ship'] is not None:
            return 'hit'
        return 'miss'

    def print(self, ships=True, misses=True, hits=True, ship_names=False):
        name_list = []
        for row, col in itertools.product(range(self.height), range(self.width)):
            ship_name = self.grid[row][col]['ship']
            if ship_name is not None and ship_name not in name_list:
                name_list.append(ship_name)

        for row in range(self.height):
            for col in range(self.width):
                cur_space = self.grid[row][col]

                print_char = '.'

                # Miss
                if misses and cur_space['shot'] and cur_space['ship'] is None:
                    print_char = 'O'

                # Ships & hits
                if cur_space['ship'] is not None:
                    if ships:
                        print_char = str(name_list.index(cur_space['ship']) + 1)
                    if hits and cur_space['shot']:
                        print_char = 'X'

                print(print_char, end=' ')
            print()

        if ship_names:
            for ship_id, ship_name in enumerate(name_list):
                print(f'Ship {ship_id + 1}: {ship_name}')


if __name__ == '__main__':
    board = Board()
    board.place_ships_randomly()

    board.print(ships=True, misses=True, hits=True, ship_names=True)
    for i in range(10):
        board.shoot(i, i)
    print()
    board.print(ships=False, misses=False, hits=False, ship_names=False)
    print()
    board.print(ships=True, misses=False, hits=False, ship_names=False)
    print()
    board.print(ships=False, misses=True, hits=True, ship_names=False)
    print()
    board.print(ships=True, misses=True, hits=True, ship_names=False)
    print()
    print()
    board.print(ships=False, misses=False, hits=True, ship_names=False)
    print()
    board.print(ships=False, misses=True, hits=False, ship_names=False)
    print()
    board.print(ships=True, misses=False, hits=True, ship_names=False)
    print()
    board.print(ships=True, misses=True, hits=False, ship_names=False)
