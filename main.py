from time import sleep

import Players
from Board import Board


if __name__ == '__main__':
    p1_board = Board(10, 10)
    p2_board = Board(10, 10)
    p1_board.place_ships_randomly()
    p2_board.place_ships_randomly()
    p1 = Players.HumanPlayer('Human')
    p2 = Players.RandomPlayer('Ranom AI')

    p2_board_params = {'show_ships_on_board': False, 'show_shots_on_board': True, 'show_turn_number': True, 'show_ship_list': True, 'show_damage': False, 'color': True}
    p1_board_params = {'show_ships_on_board': True, 'show_shots_on_board': True, 'show_turn_number': False, 'show_ship_list': True, 'show_damage': True, 'color': True}

    while True:
        print(p2_board.draw_board_next_to(p1_board, p2_board_params, p1_board_params, first_board_name=p2.name, second_board_name=p1.name))
        p1.shoot(p2_board)

        if p2_board.all_ships_sunk():
            winner = p1
            break

        print(p2_board.draw_board_next_to(p1_board, p2_board_params, p1_board_params, first_board_name=p2.name, second_board_name=p1.name))
        p2.shoot(p1_board)

        if p1_board.all_ships_sunk():
            winner = p2
            break

        sleep(0.5)

    end_game_print_options = {
        'show_ships_on_board': True,
        'show_shots_on_board': True,
        'show_turn_number': True,
        'show_ship_list': True,
        'show_damage': True,
        'color': True,
    }
    print(p2_board.draw_board_next_to(p1_board, end_game_print_options, end_game_print_options, first_board_name=p2.name, second_board_name=p1.name))
    print(f'{winner.name} won!')