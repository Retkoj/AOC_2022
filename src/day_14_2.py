from argparse import ArgumentParser

from matplotlib import pyplot as plt

import numpy as np

FILEPATH = '../data/day_14_1.txt'


class Cave:
    def __init__(self):
        self.cave = []
        self.granes = []
        self.left_bound = None
        self.right_bound = None
        self.upper_bound = None
        self.lower_bound = None

        self.start = (500, 500)
        self.total_granes = 0
        self.infinite_drop = False

    def determine_bounds(self, row, col):
        if self.left_bound is not None:
            if col < self.left_bound:
                self.left_bound = col
        else:
            self.left_bound = col
        if self.right_bound is not None:
            if col > self.right_bound:
                self.right_bound = col
        else:
            self.right_bound = col

        if self.upper_bound is not None:
            if row > self.upper_bound:
                self.upper_bound = row
        else:
            self.upper_bound = row
        if self.lower_bound is not None:
            if row < self.lower_bound:
                self.lower_bound = row
        else:
            self.lower_bound = row

    def parse_cave(self, line):
        prev_point = None
        for point in line.split(' -> '):
            col, row = [int(n) for n in point.split(',')]
            self.determine_bounds(row, col)
            if prev_point is not None:
                prev_row, prev_col = prev_point
                if row == prev_row:
                    for c in range(min(col, prev_col), max(col, prev_col) + 1):
                        self.cave.append((row, c))
                elif col == prev_col:
                    for r in range(min(row, prev_row), max(row, prev_row) + 1):
                        self.cave.append((r, col))
            prev_point = (row, col)
        self.cave = list(set(self.cave))

    def drop_granes(self):
        while not self.infinite_drop:
            bottom_index = self.drop_straight_line()

            next_option = self.side(bottom_index)
            if next_option is not None:
                self.granes.append(next_option)
                self.total_granes += 1
                if self.total_granes % 100 == 0:
                    print(self.total_granes)
                continue

            if next_option is None and bottom_index[0] == 0:
                self.granes.append(bottom_index)
                self.total_granes += 1
                self.infinite_drop = True
                break
            self.granes.append(bottom_index)
            self.total_granes += 1

            if self.total_granes % 100 == 0:
                print(self.total_granes)

    def drop_straight_line(self, col=500):
        # rows at start col; 500
        grane_rows = [i[0] for i in self.granes if i[1] == col]
        if len(grane_rows) > 0:
            bottom_index = (min(grane_rows) - 1, col)
        else:
            rows = [i[0] for i in self.cave if i[1] == col]
            bottom_index = (min(rows) - 1, col)
        # if bottom_index[0] < 0:
            # self.infinite_drop = True
            # return None
        return bottom_index

    def is_blocked(self, index):
        return (index in self.cave or index in self.granes) or index[0] == (self.upper_bound + 2)

    def side(self, bottom_index):
        new_index = None
        # first left
        diag_index = (bottom_index[0] + 1, bottom_index[1] - 1)
        if self.is_blocked(diag_index):
            # then try right
            diag_index = (bottom_index[0] + 1, bottom_index[1] + 1)

        if not self.is_blocked(diag_index):
            tmp_list = self.granes + self.cave

            lower_option = [i[0] for i in tmp_list if i[1] == diag_index[1] and i[0] > diag_index[0]]
            if len(lower_option) == 0 and not (self.right_bound > diag_index[1] > self.left_bound):
                if (self.upper_bound + 1, diag_index[1]) not in tmp_list:
                    lower_option = [self.upper_bound + 2]
            if len(lower_option) > 0:
                new_index = (min(lower_option) - 1, diag_index[1])
            else:
                new_index = diag_index

            if new_index is not None:
                tmp = self.side(new_index)
                if tmp is not None:
                    new_index = tmp

        return new_index

    def plot_cave(self, i=0):
        canvas = np.zeros((self.upper_bound + 3, self.right_bound - 380))
        for p in self.cave:
            canvas[p[0], p[1] - 400] = 1
        for p in self.granes:
            canvas[p[0], p[1] - 400] = 2
        canvas[0, 500 - 400] = 3
        plt.matshow(canvas, cmap='inferno')
        plt.axis('off')
        plt.savefig(f'..\images\cave\plot_{i}', bbox_inches='tight')
        plt.close()


def solve(data):
    cave = Cave()
    for line in data:
        cave.parse_cave(line)
    cave.drop_granes()
    print(cave.total_granes)
    # cave.plot_cave()

    print(cave.granes)
    return cave.total_granes


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
    with open('../result_day14_2.txt', 'w') as f:
        f.write(str(result))
