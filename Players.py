import contextlib
import random

import numpy as np
from colorama import Fore

from Board import Board


class Player:
    def __init__(self, name):
        self.name = name

    def shoot(self, board):
        raise NotImplementedError('You need to implement this method in a subclass')

    def __repr__(self):
        return f'Player({self.name!r})'


class HumanPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    def shoot(self, board):
        error_printed = False
        while True:
            cell = input(f'{self.name}, enter a cell to shoot (e.g. A5): ')
            valid_format = True
            if not cell[0].isalpha():
                valid_format = False
            if not cell[1:].isdigit():
                valid_format = False

            if valid_format:
                row, col = board.cell_to_row_col(cell)
                board.shoot(row, col)
                break
            else:
                if not error_printed:
                    print(f'{Fore.RED}Invalid format. Please enter a cell in the format A5{Fore.RESET}')
                    error_printed = True


class RandomPlayer(Player):
    def __init__(self, name=None):
        if name is None:
            name = 'Random Player'
        super().__init__(name)

    def shoot(self, board):
        while True:
            row = random.randrange(board.height)
            col = random.randrange(board.width)
            with contextlib.suppress(ValueError):
                board.shoot(row, col)
                break


class ProbabilisticPlayer(Player):
    def __init__(self, name=None):
        if name is None:
            name = 'Probabilistic Player'
        super().__init__(name)

        self.mode = 'search'

    def shoot(self, board):
        ship_states = board.get_ship_states()
        if 'damaged' in ship_states.values():
            self.target(board)
        else:
            self.search(board)

    def search(self, board):
        heatmap = np.zeros((board.height, board.width), dtype=int)

        # Mark spots that are already shot at as -1
        for r, c in board.shots:
            heatmap[r][c] = -1

        # Attempt to place a ship in every possible position
        ship_names = list(board.ships.keys())
        ship_lengths = [len(board.ships[ship_name]) for ship_name in ship_names]

        dummy_board = Board(board.height, board.width)
        dummy_board.shots = board.shots.copy()

        for ship_length in ship_lengths:
            for r in range(dummy_board.height):
                for c in range(dummy_board.width):
                    for direction in ['d', 'r']:
                        if dummy_board.can_place_ship(ship_length, r, c, direction):
                            for i in range(ship_length):
                                if direction == 'd':
                                    heatmap[r + i][c] += 1
                                elif direction == 'r':
                                    heatmap[r][c + i] += 1

        # Find the maximum value in the heatmap
        max_value = np.max(heatmap)
        row, col = np.where(heatmap == max_value)
        board.shoot(row[0], col[0])

    def target(self, board):
        # Get the name and length of the damaged ship
        ship_states = board.get_ship_states()
        damaged_ship_name = None
        for ship_name, ship_state in ship_states.items():
            if ship_state == 'damaged':
                damaged_ship_name = ship_name
                break
        damaged_ship_length = len(board.ships[damaged_ship_name])

        # Get coordinates of the damaged ship that have already been shot
        damaged_ship_hits = []
        for r, c in board.shots:
            for ship_cell in board.ships[damaged_ship_name]:
                if r == ship_cell[0] and c == ship_cell[1]:
                    damaged_ship_hits.append((r, c))

        # Get the direction of the damaged ship
        damaged_ship_direction = None
        if len(damaged_ship_hits) == 1:
            damaged_ship_direction = 'unknown'
        elif damaged_ship_hits[0][0] == damaged_ship_hits[1][0]:
            damaged_ship_direction = 'h'
        elif damaged_ship_hits[0][1] == damaged_ship_hits[1][1]:
            damaged_ship_direction = 'v'

        # If direction is known, shoot in that direction
        print(f'Direction: {damaged_ship_direction}')
        if damaged_ship_direction == 'h':
            dirs_to_try = ['r', 'l']
            for i in range(1, damaged_ship_length):
                for dir in dirs_to_try:
                    with contextlib.suppress(ValueError):
                        if dir == 'r':
                            result = board.shoot(damaged_ship_hits[0][0], damaged_ship_hits[0][1] + i)
                        elif dir == 'l':
                            result = board.shoot(damaged_ship_hits[0][0], damaged_ship_hits[0][1] - i)
                        if result == 'miss':
                            dirs_to_try.remove(dir)
                        else:
                            return

        elif damaged_ship_direction == 'v':
            dirs_to_try = ['u', 'd']
            for i in range(1, damaged_ship_length):
                for dir in dirs_to_try:
                    with contextlib.suppress(ValueError):
                        if dir == 'u':
                            result = board.shoot(damaged_ship_hits[0][0] - i, damaged_ship_hits[0][1])
                        elif dir == 'd':
                            result = board.shoot(damaged_ship_hits[0][0] + i, damaged_ship_hits[0][1])
                        if result == 'miss':
                            dirs_to_try.remove(dir)
                        else:
                            return

        # If direction is not known, pick the more likely direction, based on a heatmap
        else:
            heatmap = np.zeros((board.height, board.width), dtype=int)

            # Mark spots that are already shot at as -1
            for r, c in damaged_ship_hits:
                heatmap[r][c] = -1

            # Attempt to place a ship in every possible position overlapping the hits
            dummy_board = Board(board.height, board.width)
            dummy_board.shots = board.shots.copy()

            # Remove hit from board
            dummy_board.shots.remove(damaged_ship_hits[0])

            hit_r, hit_c = damaged_ship_hits[0]
            # Attempt to place ship horizontally
            for c in range(hit_c - damaged_ship_length + 1, hit_c + 1):
                if dummy_board.can_place_ship(damaged_ship_length, hit_r, c, 'r'):
                    for i in range(damaged_ship_length):
                        heatmap[hit_r][c + i] += 1
            # Attempt to place ship vertically
            for r in range(hit_r - damaged_ship_length + 1, hit_r + 1):
                if dummy_board.can_place_ship(damaged_ship_length, r, hit_c, 'd'):
                    for i in range(damaged_ship_length):
                        heatmap[r + i][hit_c] += 1

            # Add the hit back in by setting the heatmap value to 0
            heatmap[hit_r][hit_c] = 0

            # Find the maximum value in the heatmap
            max_value = np.max(heatmap)
            row, col = np.where(heatmap == max_value)
            board.shoot(row[0], col[0])


if __name__ == '__main__':
    board = Board()
    board.place_ships_randomly()
    player = ProbabilisticPlayer()

    # print(board.draw(show_ships_on_board=True, show_ship_list=False, show_turn_number=False, show_shots_on_board=True))
    # player.shoot(board)
    # player.shoot(board)

    while not board.all_ships_sunk():
        player.shoot(board)
        print(board.draw(show_ships_on_board=True, show_ship_list=False, show_turn_number=False, show_shots_on_board=True))
        input()