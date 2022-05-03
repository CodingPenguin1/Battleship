#!/usr/bin/env python
import numpy as np


class Board:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.grid = np.array((width, height), dtype=int)  # -2 hit, -1 miss, 0 empty, 1+ different ships

    def place_ship(self, row: int, col: int, orientation: str, length: int, ship_name: str):
        # sourcery skip: assign-if-exp, boolean-if-exp-identity, introduce-default-else, merge-duplicate-blocks, remove-unnecessary-cast, switch
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
        cur_row, cur_col = row, col
        valid = True

        # If the ship will be placed off the board, invalid
        if orientation == 'r' and col + length > self.width or orientation == 'l' and col - length < 0:
            valid = False
        elif orientation == 'u' and row - length < 0 or orientation == 'd' and row + length > self.height:
            valid = False

        # If overlapping another ship, invalid
        # Skip check if already not valid
        if valid:
            pass

        # If valid, place ship
        ship_id = np.max(self.grid) + 1
