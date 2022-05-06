#!/usr/bin/env python

from random import randint


class RandomAI:
    def __init__(self):
        pass

    def play(self, board):
        row, col = randint(0, board.height - 1), randint(0, board.width - 1)
        while not board.shoot(row, col):
            row, col = randint(0, board.height - 1), randint(0, board.width - 1)
        return board


class HuntAI:
    def __init__(self):
        self.mode = 'search'  # Random search, semi-intelligent hunt after a hit

    def play(self, board):
        row, col = 0, 0
        while not board.shoot(row, col):
            row, col = randint(0, board.height - 1), randint(0, board.width - 1)
        return board
