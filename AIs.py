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
        self.ships = {}

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
            # Try shooting up first
            # If successful shot (remember that shoot returns `False` if shot is invalid)
            if result := board.shoot(tar_row - 1, tar_col):
                self.process_first_hunt_shot(board, result, tar_row - 1, tar_col, 'vertical')
            # Try shooting right next
            elif result := board.shoot(tar_row, tar_col + 1):
                self.process_first_hunt_shot(board, result, tar_row, tar_col + 1, 'horizontal')
            # Try shooting down next
            elif result := board.shoot(tar_row + 1, tar_col):
                self.process_first_hunt_shot(board, result, tar_row + 1, tar_col, 'vertical')
            # Finally, try shooting to the left
            elif result := board.shoot(tar_row, tar_col - 1):
                self.process_first_hunt_shot(board, result, tar_row, tar_col - 1, 'horizontal')

    def process_first_hunt_shot(self, board, result, row, col, direction):
        if result == 'miss':
            return board
        elif result == 'hit':
            self.hunting_ship_coords.append((row, col))
            self.hunting_ship_direction = direction
        elif type(result) == tuple:
            # TODO this could be improved
            # TODO ex edge case: two ships, both horizontal in the same row. First shot hits right ship, but not the right of the right ship
            self.hunting_ship_coords = []
            self.hunting_ship_direction = ''
