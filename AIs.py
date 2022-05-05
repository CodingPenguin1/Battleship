#!/usr/bin/env python

from random import randint


class RandomAI:
    def __init__(self):
        pass

    def shoot(self, board):
        row, col = randint(0, board.height - 1), randint(0, board.width - 1)
        while not board.check_valid_shot(row, col):
            row, col = randint(0, board.height - 1), randint(0, board.width - 1)
        board.shoot(row, col)
        return board
