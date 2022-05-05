#!/usr/bin/env python
from Board import Board
from AIs import RandomAI
import matplotlib.pyplot as plt


if __name__ == '__main__':
    board = Board()
    board.place_ships_randomly()
    ai = RandomAI()

    turn_counts = []
    for _ in range(100000):
        turns = 0
        while not board.game_over():
            board = ai.shoot(board)
            turns += 1

        turn_counts.append(turns)

        board.reset()
        board.place_ships_randomly()

    plt.hist(turn_counts)
    plt.show()
