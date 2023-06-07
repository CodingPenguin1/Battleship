import contextlib
from random import choice, randint
from colorama import Back, Fore, Style

class Board:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        assert 5 < width <= 26, 'Width must be between 5 and 26'
        assert 5 < height <= 26, 'Height must be between 5 and 26'

        self.shots = []  # [(r, c), (r, c), ...]  list of spaces shot
        self.ships = {}  # {ship: [(r, c), (r, c), ...], ...}

    def can_place_ship(self, ship_length, row, col, orientation):
        # Check if ship is out of bounds
        if orientation == 'l' and col - ship_length < 0:
            return False
        elif orientation == 'r' and col + ship_length > self.width:
            return False
        elif orientation == 'u' and row - ship_length < 0:
            return False
        elif orientation == 'd' and row + ship_length > self.height:
            return False

        # Check if ship overlaps another ship
        new_ship_coords = []
        for i in range(ship_length):
            if orientation == 'l':
                new_ship_coords.append((row, col - i))
            elif orientation == 'r':
                new_ship_coords.append((row, col + i))
            elif orientation == 'u':
                new_ship_coords.append((row - i, col))
            elif orientation == 'd':
                new_ship_coords.append((row + i, col))
        for ship_coords in self.ships.values():
            for coord in new_ship_coords:
                if coord in ship_coords:
                    return False

        # Check if ship overlaps a space that's been shot
        for coord in new_ship_coords:
            if coord in self.shots:
                return False

        return True


    def add_ship(self, ship_name, ship_length, row, col, orientation):
        if not self.can_place_ship(ship_length, row, col, orientation):
            return False

        # If ship is in bounds, add it to the board
        if orientation == 'l':
            self.ships[ship_name] = [(row, col - i) for i in range(ship_length)]
        elif orientation == 'r':
            self.ships[ship_name] = [(row, col + i) for i in range(ship_length)]
        elif orientation == 'u':
            self.ships[ship_name] = [(row - i, col) for i in range(ship_length)]
        elif orientation == 'd':
            self.ships[ship_name] = [(row + i, col) for i in range(ship_length)]
        return True

    def place_ships_randomly(self, ships=None):
        if ships is None:
            ships = {'Carrier': 5, 'Battleship': 4, 'Cruiser': 3, 'Submarine': 3, 'Destroyer': 2}
        for ship_name, ship_length in ships.items():
            while True:
                orientation = choice(['u', 'd', 'l', 'r'])
                row = randint(0, self.height - 1)
                col = randint(0, self.width - 1)
                if self.add_ship(ship_name, ship_length, row, col, orientation):
                    break

    def shoot(self, row, col):
        # Check if shot is out of bounds
        if row < 0 or row >= self.height or col < 0 or col >= self.width:
            raise ValueError('Shot out of bounds')

        # Check if shot has already been taken
        if (row, col) in self.shots:
            raise ValueError('Shot already taken')

        # If shot is in bounds, mark it on the board
        self.shots.append((row, col))

        # Return miss, hit, or sunk
        for ship_name in self.ships:
            if (row, col) in self.ships[ship_name]:
                if self.is_sunk(ship_name):
                    return 'sunk'
                else:
                    return 'hit'
        return 'miss'

    def is_sunk(self, ship_name):
        return all(space in self.shots for space in self.ships[ship_name])

    def all_ships_sunk(self):
        return all(self.is_sunk(ship_name) for ship_name in self.ships)

    def get_ship_states(self):
        # Return a dictionary of {ship_name: "healthy", "damaged", or "sunk"}
        ship_states = {}
        for ship_name in self.ships:
            if self.is_sunk(ship_name):
                ship_states[ship_name] = 'sunk'
            else:
                for row, col in self.ships[ship_name]:
                    if (row, col) in self.shots:
                        ship_states[ship_name] = 'damaged'
                        break
                else:
                    ship_states[ship_name] = 'healthy'
        return ship_states

    def get_num_turns(self):
        return len(self.shots)

    def cell_to_row_col(self, cell):
        row = int(cell[1:])
        col = ord(cell[0].upper()) - 65
        return row, col

    def reset(self):
        self.shots = []
        self.ships = {}

    def draw(self, show_ships_on_board=False, show_shots_on_board=True, show_turn_number=True, show_ship_list=True, show_damage=False, color=True):
        board_string = ''

        # Draw the turn number
        if show_turn_number:
            board_string += f'Turn: {len(self.shots)}\n'

        # Draw the column letters
        board_string += '   '
        for col in range(self.width):
            board_string += f'{chr(col + 65)} '
        board_string += '\n'

        # Draw the top border
        board_string += '  '
        for _ in range(self.width):
            board_string += '+-'
        board_string += '+\n'

        # Draw the board, including ships if applicable
        board = [['.' for _ in range(self.width)] for _ in range(self.height)]
        if show_ships_on_board:
            for ship_name, ship_coords in self.ships.items():
                for row, col in ship_coords:
                    board[row][col] = ship_name[0].upper()
        if show_shots_on_board:
            for row, col in self.shots:
                shot_type = 'miss'
                for ship_name in self.ships:
                    if (row, col) in self.ships[ship_name]:
                        shot_type = 'sunk' if self.is_sunk(ship_name) else 'hit'
                if shot_type == 'hit' and show_damage:
                    board[row][col] = f'{Fore.YELLOW}X{Style.RESET_ALL}' if color else 'X'
                elif shot_type == 'miss':
                    board[row][col] = f'{Fore.CYAN}O{Style.RESET_ALL}' if color else 'O'
                elif shot_type == 'sunk' or (not show_damage and shot_type == 'hit'):
                    board[row][col] = f'{Fore.RED}X{Style.RESET_ALL}' if color else 'X'
        for row in range(self.height):
            board_string += f'{row:2d}|'
            for col in range(self.width):
                board_string += f'{board[row][col]} '
            board_string = board_string[:-1] + '|\n'

        # Draw the bottom border
        board_string += '  '
        for _ in range(self.width):
            board_string += '+-'
        board_string += '+\n'

        # Draw the ship list
        if show_ship_list:
            board_string += 'Ships:\n'
            ship_states = self.get_ship_states()
            for ship_name in ship_states.keys():
                if (
                    ship_states[ship_name] != 'sunk'
                    and ship_states[ship_name] == 'damaged'
                    and show_damage
                    and color
                ):
                    board_string += f'  {Back.YELLOW}{ship_name}{Style.RESET_ALL}\n'
                elif (
                    ship_states[ship_name] != 'sunk'
                    and ship_states[ship_name] == 'damaged'
                    and show_damage
                    or ship_states[ship_name] != 'sunk'
                    and not color
                ):
                    board_string += f'  {ship_name}\n'
                elif ship_states[ship_name] != 'sunk':
                    board_string += f'  {Back.GREEN}{ship_name}{Style.RESET_ALL}\n'
                else:
                    board_string += (
                        f'  {Back.RED}{ship_name}{Style.RESET_ALL}\n'
                        if color
                        else f'  {ship_name}\n'
                    )
        return board_string

    def draw_board_next_to(self, board, first_board_draw_parameters, second_board_draw_parameters, first_board_name=None, second_board_name=None, gap=3):
        MAX_WIDTH = self.width * 2 + 3
        string = ''

        # Draw the turn number
        if first_board_draw_parameters['show_turn_number']:
            string += f'Turn: {len(self.shots)}'
            string += ' ' * (MAX_WIDTH - len(string))
        string += ' ' * gap
        if second_board_draw_parameters['show_turn_number']:
            string += f'Turn: {len(board.shots)}'
        string += '\n'

        # Draw the board names
        if first_board_name is not None:
            string += f'{first_board_name}'
            string += ' ' * (MAX_WIDTH - len(first_board_name))
        string += ' ' * gap
        if second_board_name is not None:
            string += f'{second_board_name}'
        string += '\n'

        # Draw the column letters
        string += '   '
        for col in range(self.width):
            string += f'{chr(col + 65)} '
        string += ' ' * gap
        string += '   '
        for col in range(board.width):
            string += f'{chr(col + 65)} '
        string += '\n'

        # Draw the top border
        string += '  '
        for _ in range(self.width):
            string += '+-'
        string += '+'
        string += ' ' * gap
        string += '  '
        for _ in range(board.width):
            string += '+-'
        string += '+\n'

        # Draw the board, including ships if applicable
        board1 = [['.' for _ in range(self.width)] for _ in range(self.height)]
        board2 = [['.' for _ in range(board.width)] for _ in range(board.height)]
        if first_board_draw_parameters['show_ships_on_board']:
            for ship_name, ship_coords in self.ships.items():
                for row, col in ship_coords:
                    board1[row][col] = ship_name[0].upper()
        if first_board_draw_parameters['show_shots_on_board']:
            for row, col in self.shots:
                shot_type = 'miss'
                for ship_name in self.ships:
                    if (row, col) in self.ships[ship_name]:
                        shot_type = 'sunk' if self.is_sunk(ship_name) else 'hit'
                if shot_type == 'hit' and first_board_draw_parameters['show_damage']:
                    board1[row][col] = f'{Fore.YELLOW}X{Style.RESET_ALL}' if first_board_draw_parameters['color'] else 'X'
                elif shot_type == 'miss':
                    board1[row][col] = f'{Fore.CYAN}O{Style.RESET_ALL}' if first_board_draw_parameters['color'] else 'O'
                elif shot_type == 'sunk' or (not first_board_draw_parameters['show_damage'] and shot_type == 'hit'):
                    board1[row][col] = f'{Fore.RED}X{Style.RESET_ALL}' if first_board_draw_parameters['color'] else 'X'
        if second_board_draw_parameters['show_ships_on_board']:
            for ship_name, ship_coords in board.ships.items():
                for row, col in ship_coords:
                    board2[row][col] = ship_name[0].upper()
        if second_board_draw_parameters['show_shots_on_board']:
            for row, col in board.shots:
                shot_type = 'miss'
                for ship_name in board.ships:
                    if (row, col) in board.ships[ship_name]:
                        shot_type = 'sunk' if board.is_sunk(ship_name) else 'hit'
                if shot_type == 'hit' and second_board_draw_parameters['show_damage']:
                    board2[row][col] = f'{Fore.YELLOW}X{Style.RESET_ALL}' if second_board_draw_parameters['color'] else 'X'
                elif shot_type == 'miss':
                    board2[row][col] = f'{Fore.CYAN}O{Style.RESET_ALL}' if second_board_draw_parameters['color'] else 'O'
                elif shot_type == 'sunk' or (not second_board_draw_parameters['show_damage'] and shot_type == 'hit'):
                    board2[row][col] = f'{Fore.RED}X{Style.RESET_ALL}' if second_board_draw_parameters['color'] else 'X'
        for row in range(self.height):
            string += f' {row}|'
            for col in range(self.width):
                string += f'{board1[row][col]} '
            string += '\b|'
            string += ' ' * gap
            string += f' {row}|'
            for col in range(board.width):
                string += f'{board2[row][col]} '
            string += '\b|\n'

        # Draw the bottom border
        string += '  '
        for _ in range(self.width):
            string += '+-'
        string += '+'
        string += ' ' * gap
        string += '  '
        for _ in range(board.width):
            string += '+-'
        string += '+\n'

        # Draw the ship list
        health_colors = {'healthy': Back.GREEN, 'damaged': Back.YELLOW, 'sunk': Back.RED}
        my_ship_strings = []
        if first_board_draw_parameters['show_ship_list']:
            for i in range(len(self.ships)):
                ship_states = self.get_ship_states()
                ship_name = list(ship_states.keys())[i]
                if first_board_draw_parameters['color']:
                    my_ship_strings.append(f'{health_colors[ship_states[ship_name]]}{ship_name}{Style.RESET_ALL}' + ' ' * (MAX_WIDTH - len(ship_name)))
                else:
                    my_ship_strings.append(f'{ship_name}' + ' ' * (MAX_WIDTH - len(ship_name)))
        opponent_ship_strings = []
        if second_board_draw_parameters['show_ship_list']:
            for i in range(len(board.ships)):
                ship_states = board.get_ship_states()
                ship_name = list(ship_states.keys())[i]
                if second_board_draw_parameters['color']:
                    opponent_ship_strings.append(f'{health_colors[ship_states[ship_name]]}{ship_name}{Style.RESET_ALL}' + ' ' * (MAX_WIDTH - len(ship_name)))
                else:
                    opponent_ship_strings.append(f'{ship_name}')

        if first_board_draw_parameters['show_ship_list'] and second_board_draw_parameters['show_ship_list']:
            string += 'Ships:'.ljust(self.width * 2 + 3 + gap) + 'Ships:\n'
            for i in range(len(my_ship_strings)):
                string += f'  {my_ship_strings[i]}'
                string += gap * ' '
                string += opponent_ship_strings[i] + '\n'
        elif first_board_draw_parameters['show_ship_list']:
            string += 'Ships:\n'
            for i in range(len(self.ships)):
                string += f'  {my_ship_strings[i]}' + '\n'
        elif second_board_draw_parameters['show_ship_list']:
            string += ' ' * (self.width * 2 + 3 + gap) + 'Ships:\n'
            for i in range(len(board.ships)):
                string += ' ' * (self.width * 2 + 3 + gap) + '  ' + opponent_ship_strings[i] + '\n'

        return string


if __name__ == '__main__':
    p = Board()
    e = Board()
    p.place_ships_randomly()
    e.place_ships_randomly()

    player_print_options = {
        'show_ships_on_board': True,
        'show_shots_on_board': True,
        'show_turn_number': True,
        'show_ship_list': True,
        'show_damage': True,
        'color': True,
    }
    enemy_print_options = {
        'show_ships_on_board': True,
        'show_shots_on_board': True,
        'show_turn_number': True,
        'show_ship_list': True,
        'show_damage': True,
        'color': True,
    }

    p.shoot(0, 0)
    e.shoot(1, 2)

    print(p.draw_board_next_to(e, player_print_options, enemy_print_options))
