#!/usr/bin/env python
from concurrent.futures import ProcessPoolExecutor
from copy import deepcopy
from time import time
from os import cpu_count

import matplotlib.pyplot as plt

from AIs import *
from Board import Board


def simulate_games(num_games=100000, ai=RandomAI(), num_threads=cpu_count(), show_histogram=False):
    ais = [deepcopy(ai) for _ in range(num_threads)]
    game_list = [num_games // num_threads for _ in range(num_threads)]
    print(f'Running {"{:,}".format(num_games)} games on {num_threads} threads with AI {ai.__class__.__name__}')

    turn_counts = []
    t_start = time()
    with ProcessPoolExecutor(num_threads) as executor:
        results = executor.map(simulate_games_thread, ais, game_list)
        for result in results:
            turn_counts.extend(result)
    t_end = time()
    print(f'Time taken: {round(t_end - t_start, 2)}s')

    if show_histogram:
        plt.hist(turn_counts)
        plt.show()


def simulate_games_thread(ai, count):
    # Run `count` games with `ai`, return list of how many turns each game took
    board = Board()
    turn_counts = []

    for _ in range(count):
        board.reset()
        board.place_ships_randomly()

        turns = 0
        while not board.game_over():
            board = ai.play(board)
            turns += 1
        turn_counts.append(turns)

    return turn_counts


def demo_game(ai=RandomAI()):
    board = Board()
    board.place_ships_randomly()
    board.print(ship_names=True)
    print()

    while not board.game_over():
        input()
        board = ai.play(board)
        board.print(ship_names=True, turn_number=True)

    board.print(ship_names=True, turn_number=True)
    print(f'Game took {board.get_num_turns()} turns')


if __name__ == '__main__':
    demo_game(ai=RandomAI())
