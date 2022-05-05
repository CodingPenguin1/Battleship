#!/usr/bin/env python
import numpy as np


class Board:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.grid = np.zeros((width, height), dtype=int)  # -2 hit, -1 miss, 0 empty, 1+ different ships
        self.ship_names = ['NULL']  # Ship names, keyed by index (ship ID)

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
        else:
            raise ValueError(f'Invalid orientation when placing ship: {orientation}')

        # Check to see if placement is valid
        valid = True

        # If the ship will be placed off the board, invalid
        if orientation == 'r' and col + length > self.width:
            return False
        elif orientation == 'l' and col - length < 0:
            return False
        elif orientation == 'u' and row - length < 0:
            return False
        elif orientation == 'd' and row + length > self.height:
            return False

        # If overlapping another ship, invalid
        cur_row, cur_col = row, col
        while abs(cur_row - row) < length and abs(cur_col - col) < length:
            if self.grid[cur_row][cur_col] != 0:
                return False
            cur_row += row_increment
            cur_col += col_increment

        # If valid, place ship
        ship_id = np.max(self.grid) + 1
        cur_row, cur_col = row, col
        while abs(cur_row - row) < length and abs(cur_col - col) < length:
            self.grid[cur_row][cur_col] = ship_id
            cur_row += row_increment
            cur_col += col_increment
        self.ship_names.append(ship_name)
        return True

    def randomly_place_ships(self, ships=None):
        # `ships` is a dictionary of ship lengths, keyed by ship name
        if ships is None:
            ships = {'carrier': 5, 'battleship': 4, 'cruiser': 3, 'submarine': 3, 'destroyer': 2}

        for ship_name, length in ships.items():
            placed = False
            while not placed:
                row = np.random.randint(0, self.height)
                col = np.random.randint(0, self.width)
                orientation = np.random.choice(['r', 'l', 'u', 'd'])
                placed = self.place_ship(row, col, orientation, length, ship_name)

    def print(self, ships=True, misses=True, hits=True, ship_names=False):
        for row in range(self.height):
            for col in range(self.width):
                if ships and self.grid[row][col] > 0:
                    print(int(self.grid[row][col]), end=' ')
                elif hits and self.grid[row][col] < 0:
                    print('X', end=' ')
                elif misses and self.grid[row][col] == -1:
                    print('O', end=' ')
                else:
                    print('.', end=' ')
            print()

        if ship_names:
            for ship_id in range(1, len(self.ship_names)):
                print(f'Ship {ship_id}: {self.ship_names[ship_id]}')


if __name__ == '__main__':
    board = Board()
    board.randomly_place_ships()
    board.print(ship_names=True)
