from argparse import ArgumentParser
from collections import Counter

from matplotlib import pyplot as plt
import numpy as np

FILEPATH = '../data/day_23_1.txt'


class MoveElves:
    def __init__(self, original_elves_positions):
        self.elves_positions = original_elves_positions
        self.planned_moves = {}
        self.move_order = ['N', 'S', 'W', 'E']
        self.plot_index = 0
        self.moving_elves = []

    def get_surrounding_indices(self, position):
        """Up is row -1, down is row + 1, left is col -1, right is col + 1"""
        row, col = position
        surrounding = {
            "NW": (row - 1, col - 1),
            "N": (row - 1, col),
            "NE": (row - 1, col + 1),
            "E": (row, col + 1),
            "SE": (row + 1, col + 1),
            "S": (row + 1, col),
            "SW": (row + 1, col - 1),
            "W": (row, col - 1),
        }
        return surrounding

    def plan_moves(self):
        self.planned_moves = {}
        for elf in self.elves_positions:
            surrounding = self.get_surrounding_indices(elf)
            if any([True if p in self.elves_positions else False for p in surrounding.values()]):
                for m in self.move_order:
                    if m == 'N':
                        if not any([True if p in self.elves_positions else False
                                    for p in [surrounding['NW'], surrounding['N'], surrounding['NE']]]):
                            self.planned_moves[elf] = surrounding['N']
                            break
                    elif m == 'S':
                        if not any([True if p in self.elves_positions else False
                                    for p in [surrounding['SW'], surrounding['S'], surrounding['SE']]]):
                            self.planned_moves[elf] = surrounding['S']
                            break
                    elif m == 'W':
                        if not any([True if p in self.elves_positions else False
                                    for p in [surrounding['NW'], surrounding['W'], surrounding['SW']]]):
                            self.planned_moves[elf] = surrounding['W']
                            break
                    elif m == 'E':
                        if not any([True if p in self.elves_positions else False
                                    for p in [surrounding['NE'], surrounding['E'], surrounding['SE']]]):
                            self.planned_moves[elf] = surrounding['E']
                            break

    def make_moves(self):
        new_positions = []

        self.moving_elves = []
        move_counts = Counter(self.planned_moves.values())
        for elf, move in self.planned_moves.items():
            if move_counts[move] == 1:
                self.moving_elves.append(elf)
                new_positions.append(move)

        not_moving_elves = [elf for elf in self.elves_positions if elf not in self.moving_elves]
        new_positions += not_moving_elves

        self.elves_positions = new_positions

    def move_round(self):
        self.plan_moves()
        self.make_moves()

        # Move current direction to back of list
        current_move = self.move_order.pop(0)
        self.move_order.append(current_move)
        return self.moving_elves

    def get_outerbounds(self):
        lr_values = [p[1] for p in self.elves_positions]
        ud_values = [p[0] for p in self.elves_positions]

        left = min(lr_values)
        right = max(lr_values)
        up = min(ud_values)
        down = max(ud_values)

        return left, right, up, down

    def calculate_empty_tiles(self):
        left, right, up, down = self.get_outerbounds()
        left = left - 1 if left < 0 else left
        up = up - 1 if up < 0 else up
        surface = abs(right - left) * abs(down - up)

        return surface - len(self.elves_positions)

    def print_board(self):
        left, right, up, down = self.get_outerbounds()
        col_shift = 0
        if left < 0:
            col_shift = (-1 * left)
        row_shift = 0
        if up < 0:
            row_shift = (-1 * up)

        grid = np.zeros((down + row_shift + 1, right + col_shift + 1))
        for elf in self.elves_positions:
            grid[elf[0] + row_shift, elf[1] + col_shift] = 1
        plt.matshow(grid, cmap='inferno')
        plt.axis('off')
        plt.savefig(f'..\images\elves\plot_{self.plot_index}', bbox_inches='tight')
        plt.close()
        self.plot_index += 1


def parse(data):
    elves = []
    for row, line in enumerate(data):
        for col, char in enumerate(list(line)):
            if char == '#':
                elves.append((row, col))
    return elves


def solve(data):
    elves = parse(data)
    move_elves = MoveElves(elves)
    # move_elves.print_board()
    round = 1
    while True:
        moving_elves = move_elves.move_round()
        # move_elves.print_board()
        if len(moving_elves) == 0:
            break
        round += 1
        if round % 10 == 0:
            print(f"round: {round}")
    # total = move_elves.calculate_empty_tiles()
    return round


def read_file(file_path):
    with open(file_path) as file:
        data = [i.strip('\n') for i in file.readlines()]

    print(f"INPUT DATA:\n{data}\n")
    return data


if __name__ == '__main__':
    argparser = ArgumentParser()
    argparser.add_argument('--input-file', type=str, required=False,
                           help="Path to the input file to process. Overwrites the filepath in the script.")
    args = argparser.parse_args()
    if args.input_file:
        FILEPATH = args.input_file

    input_data = read_file(FILEPATH)
    result = solve(input_data)
    print(f"{'-' * 100}\nOUTPUT: {result}")
