from argparse import ArgumentParser
from copy import deepcopy

import numpy as np

FILEPATH = '../data/day_8_1.txt'


class VisibleTreeCounter:
    def __init__(self, grid: np.array):
        self.grid = grid
        self.counter_grid = np.zeros(self.grid.shape)
        self.scenic_grid = np.zeros(self.grid.shape)

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

    def walk_neighbours(self, line, i):
        tmp_score = 0
        neighbour = i - 1
        while neighbour >= 0:
            if line[neighbour] < line[i]:
                tmp_score += 1
            elif line[neighbour] >= line[i]:
                tmp_score += 1
                break
            neighbour -= 1
        return tmp_score

    def scenic_score(self, line):
        visible = self.visible(line)
        scores = np.zeros(len(line))
        for i in range(0, len(line)):
            if visible[i]:
                scores[i] = self.walk_neighbours(line, i)
                flipped_line = np.flip(line)
                scores[i] *= self.walk_neighbours(flipped_line, (len(line) - i - 1))
        return scores

    def calculate_scenic_score(self):
        for i, row in enumerate(self.grid):
            self.scenic_grid[i] = self.scenic_score(row)
        for i, column in enumerate(self.grid.transpose()):
            self.scenic_grid = self.scenic_grid.transpose()
            self.scenic_grid[i] *= self.scenic_score(column)
            self.scenic_grid = self.scenic_grid.transpose()

        print(self.scenic_grid)


def solve(data):
    grid = np.array(data)
    print(grid)
    tree_counter = VisibleTreeCounter(grid)
    tree_counter.calculate_scenic_score()

    return tree_counter.scenic_grid.max()


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
