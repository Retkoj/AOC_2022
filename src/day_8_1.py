from argparse import ArgumentParser
from copy import deepcopy

import numpy as np

FILEPATH = '../data/day_8_1.txt'


class VisibleTreeCounter:
    def __init__(self, grid: np.matrix):
        self.grid = grid
        self.counter_grid = np.zeros(self.grid.shape)
        self.visible_trees = 0

    def count(self):
        return self.counter_grid.sum()

    def walk_grid(self):
        for i, row in enumerate(self.grid):
            self.counter_grid[i] = self.visible(row)
        for i, column in enumerate(self.grid.transpose()):
            visible_column = self.visible(column)
            self.counter_grid = self.counter_grid.transpose()
            # Don't overwrite 1's
            visible_trees = [max(z) for z in zip(visible_column, self.counter_grid[i])]
            self.counter_grid[i] = visible_trees
            self.counter_grid = self.counter_grid.transpose()

        print(self.counter_grid)

    def visible(self, line):
        visible_trees = [1 if ((line[i] > max(line[0: i])) or (line[i] > max(line[i + 1:]))) else 0
                         for i in range(1, len(line) - 1)]
        visible_trees.insert(0, 1)
        visible_trees.append(1)
        return visible_trees


def solve(data):
    grid = np.array(data)
    print(grid)
    tree_counter = VisibleTreeCounter(grid)
    tree_counter.walk_grid()

    return tree_counter.count()


def read_file(file_path):
    with open(file_path) as file:
        data = [[int(j) for j in list(i.strip('\n'))] for i in file.readlines()]

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
