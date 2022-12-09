from argparse import ArgumentParser

from matplotlib import pyplot as plt
import numpy as np

FILEPATH = '../data/day_9_1.txt'


class HeadTail:
    def __init__(self, n_knots=9):
        self.head = (0, 0)
        self.tail = (0, 0)
        self.tail_locations = [(0, 0)]
        self.last_move = None
        self.n_knots = n_knots
        self.knots = {i: (0, 0) for i in range(1, self.n_knots + 1)}
        self.plot_indices = {}
        self.plot_index = 0
        self.grid = np.zeros((60, 60))

    def is_adjacent(self, prev_knot_loc, knot_loc):
        head_y, head_x = prev_knot_loc
        tail_y, tail_x = knot_loc
        return (abs(head_x - tail_x) < 2) and abs(head_y - tail_y) < 2

    def is_diagonal_jump(self, prev_knot_loc, knot_loc):
        head_y, head_x = prev_knot_loc
        tail_y, tail_x = knot_loc
        return ((abs(head_x - tail_x) == 2) and abs(head_y - tail_y) == 1) or \
            ((abs(head_x - tail_x) == 1) and abs(head_y - tail_y) == 2)

    def move_head(self, move):
        direction, steps = move.split(' ')
        steps = int(steps)
        head_moves = []
        head_y, head_x = self.head
        if direction == 'L':
            head_moves = list(zip([head_y] * (steps + 1), range(head_x, head_x - steps - 1, -1)))
        if direction == 'R':
            head_moves = list(zip([head_y] * (steps + 1), range(head_x, head_x + steps + 1)))
        if direction == 'U':
            head_moves = list(zip(range(head_y, head_y + steps + 1), [head_x] * (steps + 1)))
        if direction == 'D':
            head_moves = list(zip(range(head_y, head_y - steps - 1, -1), [head_x] * (steps + 1)))
        self.head = head_moves[-1]
        return head_moves

    def single_move(self, prev_knot_move, knot):
        current_loc = self.knots[knot]
        if not self.is_adjacent(prev_knot_move, current_loc):
            # If knots don't touch anymore
            if self.is_diagonal_jump(prev_knot_move, current_loc):
                # If other knot requires a diagonal jump
                y = 1 if prev_knot_move[0] > current_loc[0] else -1
                x = 1 if prev_knot_move[1] > current_loc[1] else -1

            else:
                # Otherwise, close gap between other knot
                if prev_knot_move[0] != current_loc[0]:
                    y = 1 if prev_knot_move[0] > current_loc[0] else -1
                else:
                    y = 0
                if prev_knot_move[1] != current_loc[1]:
                    x = 1 if prev_knot_move[1] > current_loc[1] else -1
                else:
                    x = 0

            next_move = (current_loc[0] + y, current_loc[1] + x)
            self.knots[knot] = next_move

            if knot == self.n_knots:
                self.tail_locations.append(next_move)

        self.write_to_grid(self.knots[knot])
        return self.knots[knot]

    def move_knot(self, prev_knot_moves, knot):
        current_knot_moves = []
        for step in range(0, len(prev_knot_moves)):
            current_loc = self.knots[knot]
            prev_knot_move = prev_knot_moves[step]
            if not self.is_adjacent(prev_knot_move, current_loc):
                # If knots don't touch anymore
                if self.is_diagonal_jump(prev_knot_move, current_loc):
                    # If other knot requires a diagonal jump
                    y = 1 if prev_knot_move[0] > current_loc[0] else -1
                    x = 1 if prev_knot_move[1] > current_loc[1] else -1

                else:
                    # Otherwise, close gap between other knot
                    if prev_knot_move[0] != current_loc[0]:
                        y = 1 if prev_knot_move[0] > current_loc[0] else -1
                    else:
                        y = 0
                    if prev_knot_move[1] != current_loc[1]:
                        x = 1 if prev_knot_move[1] > current_loc[1] else -1
                    else:
                        x = 0

                next_move = (current_loc[0] + y, current_loc[1] + x)
                self.knots[knot] = next_move
                current_knot_moves.append(next_move)

                if knot == self.n_knots:
                    self.tail_locations.append(next_move)
            self.plot_indices[knot].append(self.knots[knot])
        return current_knot_moves

    def make_single_moves(self, move):
        prev_knot_moves = self.move_head(move)
        for prev_knot_move in prev_knot_moves:
            self.grid = np.zeros((60, 60))
            self.write_to_grid(prev_knot_move)
            for knot in range(1, self.n_knots + 1):
                prev_knot_move = self.single_move(prev_knot_move, knot)

            self.plot_moves()

    def make_move(self, move: str):
        prev_knot_moves = self.move_head(move)
        for knot in range(1, self.n_knots + 1):
            if len(prev_knot_moves) > 0:
                prev_knot_moves = self.move_knot(prev_knot_moves, knot)
            else:
                break
            print(move)
            self.print_locations()

    def count_locations(self):
        # return count of unique locations
        return len(list(set(self.tail_locations)))

    def print_locations(self):
        print(f"Head: {self.head}")
        for knot, location in self.knots.items():
            print(f"{knot}: {location}")

    def _get_move(self, knot):
        moves = self.plot_indices.get(knot, [])
        if len(moves) > 0:
            return moves.pop(0)
        else:
            return self.knots[knot]

    def write_to_grid(self, knot_location):
        reindex_factor = 30
        self.grid[-1 * (knot_location[0] + reindex_factor), knot_location[1] + reindex_factor] = 1

    def plot_moves(self):
        plt.matshow(self.grid, cmap='inferno')
        plt.axis('off')
        plt.savefig(f'..\images\snake\plot_{self.plot_index}', bbox_inches='tight')
        plt.close()
        self.plot_index += 1


def solve(data):
    head_tail = HeadTail(n_knots=9)
    for move in data:
        head_tail.make_single_moves(move)
    total = head_tail.count_locations()
    return total


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
