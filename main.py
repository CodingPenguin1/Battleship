from time import sleep

import colorama

import Players
from Board import Board


def draw_player_boards(player_board, opponent_board):
    player_board_string = player_board.draw(
        show_ships_on_board=True,
        show_shots_on_board=True,
        show_turn_number=True,
        show_ship_list=True,
        show_damage=True,
        color=False)
    opponent_board_string = opponent_board.draw(
        show_ships_on_board=False,
        show_shots_on_board=True,
        show_turn_number=False,
        show_ship_list=True,
        show_damage=False,
        color=False)

    player_board_list = player_board_string.split('\n')
    opponent_board_list = [''] + opponent_board_string.split('\n')

    max_height = max(len(player_board_list), len(opponent_board_list))
    max_length_player = max(len(line) for line in player_board_list)

    combined_board_string = ''
    for i in range(max_height):
        if i < len(player_board_list):
            combined_board_string += player_board_list[i]
        else:
            combined_board_string += ' ' * max_length_player

        # Make sure the boards and ship lists are aligned
        combined_board_string += ' ' * (max_length_player - len(player_board_list[i]))
        if len(player_board_list[i]) == 18:
            for c in range(18):
                print(player_board_list[i][c], end='')
        combined_board_string += '    '

        if i < len(opponent_board_list):
            combined_board_string += opponent_board_list[i]
        combined_board_string += '\n'

    # Add colors back in
    combined_board_string = combined_board_string.replace('X', f'{colorama.Fore.RED}X{colorama.Style.RESET_ALL}')
    combined_board_string = combined_board_string.replace('O', f'{colorama.Fore.BLUE}O{colorama.Style.RESET_ALL}')

    for ship in player_board.ships:
        # Get index of ship name or 2nd index if it appears twice
        ship_index = [i for i, x in enumerate(player_board_string.split('\n')[0]) if x == ship.name][1]




    print(combined_board_string)


if __name__ == '__main__':
    p1_board = Board(10, 10)
    p2_board = Board(10, 10)
    p1_board.place_ships_randomly()
    p2_board.place_ships_randomly()
    p1 = Players.RandomPlayer('Player 1')
    p2 = Players.RandomPlayer('Player 2')

    p2_board_params = {'show_ships_on_board': False, 'show_shots_on_board': True, 'show_turn_number': True, 'show_ship_list': True, 'show_damage': False, 'color': True}
    p1_board_params = {'show_ships_on_board': True, 'show_shots_on_board': True, 'show_turn_number': True, 'show_ship_list': True, 'show_damage': True, 'color': True}

    while True:
        print(p2_board.draw_board_next_to(p1_board, p2_board_params, p1_board_params))
        p1.shoot(p2_board)

        if p2_board.all_ships_sunk():
            winner = p1
            break

        print(p2_board.draw_board_next_to(p1_board, p2_board_params, p1_board_params))
        p2.shoot(p1_board)

        if p1_board.all_ships_sunk():
            winner = p2
            break

        # sleep(0.5)

    end_game_print_options = {
        'show_ships_on_board': True,
        'show_shots_on_board': True,
        'show_turn_number': True,
        'show_ship_list': True,
        'show_damage': True,
        'color': True,
    }
    print(p2_board.draw_board_next_to(p1_board, end_game_print_options, end_game_print_options))
    print(f'{winner.name} won!')