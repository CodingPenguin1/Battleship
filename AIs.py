#!/usr/bin/env python

from random import randint


class RandomAI:
    def __init__(self):
        pass

    def shoot(self, board):
        row, col = randint(0, board.height - 1), randint(0, board.width - 1)
        while not board.shoot(row, col):
            row, col = randint(0, board.height - 1), randint(0, board.width - 1)
        return board


class HuntAI:
    def __init__(self):
        self.mode = 'search'  # Random search, semi-intelligent hunt after a hit
        self.hunting_ship_coords = []
        self.hunting_ship_direction = ''

    def shoot(self, board):
        # If search mode, randomly shoot
        if self.mode == 'search':
            row, col = randint(0, board.height - 1), randint(0, board.width - 1)
            result = board.shoot(row, col)
            while not result:
                row, col = randint(0, board.height - 1), randint(0, board.width - 1)
                result = board.shoot(row, col)
            if result == 'hit':  # If hit and not sunk, switch to hunt mode
                self.mode = 'hunt'
                self.hunting_ship_coords.append((row, col))
            return board

        # If in hunt mode
        tar_row, tar_col = self.hunting_ship_coords[0]
        # If only 1 hit so far, try to figure out the direction of the ship
        if len(self.hunting_ship_coords) == 1:
            result = board.shoot(tar_row - 1, tar_col)
            # TODO: Take some time to think through this. It's more complicated than it seems on the surface
            if type(result) == tuple:
                pass
            if result == 'hit':
                self.hunting_ship_coords.append((tar_row - 1, tar_col))
                self.hunting_ship_direction == 'vertical'
