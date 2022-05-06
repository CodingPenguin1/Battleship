import itertools
from random import choice, randint

from colorama import Back, Fore, Style


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

    def get_ship_length(self, ship_name):
        return sum(self.grid[row][col]['ship'] == ship_name for row, col in itertools.product(range(self.height), range(self.width)))

    def check_if_ship_is_sunk(self, ship_name):
        # Returns boolean True/False if ship_name is sunk
        for row, col in itertools.product(range(self.height), range(self.width)):
            if self.grid[row][col]['ship'] == ship_name and not self.grid[row][col]['shot']:
                return False
        return True

    def shoot(self, row: int, col: int):
        # Returns `False` if shot is invalid
        # Returns 'miss' if shot is a miss
        # Returns 'hit' if shot is a hit, but does not sink a ship
        # Returns (ship_name, ship_length) if shot is a hit and sinks a ship

        if self.grid[row][col]['shot']:
            return False
        self.grid[row][col]['shot'] = True
        if self.grid[row][col]['ship'] is not None:
            # If ship was sunk, return (ship name, length)
            ship_name = self.grid[row][col]['ship']
            if self.check_if_ship_is_sunk(ship_name):
                return ship_name, self.get_ship_length(self.grid[row][col]['ship'])
            # If ship was not sunk, return 'hit'
            return 'hit'
        return 'miss'

    def game_over(self):
        for row, col in itertools.product(range(self.height), range(self.width)):
            if self.grid[row][col]['ship'] is not None and not self.grid[row][col]['shot']:
                return False
        return True

    def get_num_turns(self):
        # Returns the number of turns the game has taken so far
        return sum(self.grid[row][col]['shot'] for row, col in itertools.product(range(self.height), range(self.width)))

    def reset(self):
        self.grid = [[{'shot': False, 'ship': None} for _ in range(self.width)] for _ in range(self.height)]

    def print(self, ships=True, misses=True, hits=True, ship_names=False, turn_number=False):
        name_list = []
        for row, col in itertools.product(range(self.height), range(self.width)):
            ship_name = self.grid[row][col]['ship']
            if ship_name is not None and ship_name not in name_list:
                name_list.append(ship_name)

        if turn_number:
            print(f'Turn {self.get_num_turns()}')

        for row in range(self.height):
            for col in range(self.width):
                cur_space = self.grid[row][col]
                print_char, color = '.', Fore.BLACK

                # Miss
                if misses and cur_space['shot'] and cur_space['ship'] is None:
                    print_char = 'O'
                    color = Fore.WHITE

                # Ships & hits
                if cur_space['ship'] is not None:
                    if ships:
                        print_char = str(name_list.index(cur_space['ship']) + 1)
                    if hits and cur_space['shot']:
                        print_char = 'X'
                        color = Fore.RED

                print(color + print_char, end=' ')
            print(Fore.RESET)

        if ship_names:
            for ship_id, ship_name in enumerate(name_list):
                if not self.check_if_ship_is_sunk(ship_name):
                    print(f'{Back.GREEN}{Fore.BLACK}Ship {ship_id + 1}: {ship_name}{Back.RESET}{Fore.RESET}')
                else:
                    print(f'{Back.RED}Ship {ship_id + 1}: {ship_name}{Back.RESET}')


if __name__ == '__main__':
    board = Board()
    board.place_ship(0, 0, 'r', 5, 'carrier')
    print(board.shoot(0, 0))
    print(board.shoot(0, 1))
    print(board.shoot(0, 2))
    print(board.shoot(0, 3))
    print(board.shoot(0, 4))

    board.print(ships=True, misses=True, hits=True, ship_names=True)
