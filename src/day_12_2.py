from argparse import ArgumentParser
from copy import deepcopy
from string import ascii_lowercase
from enum import Enum

FILEPATH = '../data/day_12_1.txt'


class TraverseStates(Enum):
    """Helper class for node states during graph traversal"""
    VISITED = 'grey'
    ALL_NEIGHBOURS_VISITED = 'black'
    NOT_VISITED = 'white'


class SearchGrid:
    def __init__(self, grid, start):
        self.grid = grid
        self.start = start
        self.end = None
        self.find_end()
        self.letters = ascii_lowercase
        self.paths = []

        self.predecessor = {}
        self.distances = {}
        self.traversed = {}
        self.queue = []

    def find_end(self):
        for key, value in self.grid.items():
            if value == 'E':
                self.end = key

    def index_of_letter(self, l):
        if self.grid[l] == 'S':
            return 0
        elif self.grid[l] == 'E':
            return 25
        else:
            return self.letters.index(self.grid[l])

    def get_surrounding_locations(self, location):
        left = (location[0], location[1] - 1)
        right = (location[0], location[1] + 1)
        up = (location[0] - 1, location[1])
        down = (location[0] + 1, location[1])

        valid_locations = []
        current_location_index = self.index_of_letter(location)

        for neighbour in [left, right, up, down]:
            if neighbour in self.grid.keys() and \
                    (self.index_of_letter(neighbour) - 1) <= current_location_index:
                valid_locations.append(neighbour)
        return valid_locations

    def traverse_graph(self):
        for node in self.grid.keys():
            self.predecessor[node] = -1
            self.distances[node] = float("inf")
            self.traversed[node] = TraverseStates.NOT_VISITED

        self.traversed[self.start] = TraverseStates.VISITED
        self.distances[self.start] = 0

        self.queue = []
        self.queue.insert(0, self.start)

        while len(self.queue) > 0:
            current_node = self.queue.pop()
            for neighbor in self.get_surrounding_locations(current_node):
                if self.traversed[neighbor] == TraverseStates.NOT_VISITED:
                    self.predecessor[neighbor] = current_node
                    self.distances[neighbor] = self.distances[current_node] + 1
                    self.traversed[neighbor] = TraverseStates.VISITED

                    self.queue.insert(0, neighbor)

            self.traversed[current_node] = TraverseStates.ALL_NEIGHBOURS_VISITED

    def find_path_to_node(self, target_node, start_node=None):
        """
        Given a target node, find the path from the start node to that target node.
        Works by recursively looking up the predecessor nodes, starting at the target node and stopping when
        the start node is reached. The returned list contains the starting node and the nodes that need to be
        passed to get to the target node.

        :param target_node: str, The end node
        :param start_node: str, Root node, defaults to self.start_node
        :return: list, [start_node, node_1, node_2, ..., node_n, target_node]
        """
        start_found = False
        start_node = start_node if start_node else self.start
        path = []
        current_node = target_node
        while not start_found:
            path.append(current_node)
            if current_node == -1:
                return []
            current_node = self.predecessor[current_node]
            if current_node == start_node:
                start_found = True
                path.append(current_node)
        path.reverse()
        return path


def find_a_points(grid):
    a_points = []
    for key, value in grid.items():
        if value in ['a', 'S']:
            a_points.append(key)
    return a_points


def solve(data):
    a_points = find_a_points(data)
    path_lengths = []
    for a_point in a_points:
        search_grid = SearchGrid(data, a_point)
        search_grid.traverse_graph()
        path = search_grid.find_path_to_node(search_grid.end, a_point)
        if path:
            path_lengths.append(len(path) - 1)
    return min(path_lengths)


def make_grid(data):
    grid = {}
    for i, line in enumerate(data):
        for j, letter in enumerate(list(line)):
            location = (i, j)
            grid[location] = letter
    return grid


def read_file(file_path):
    with open(file_path) as file:
        data = [i.strip('\n') for i in file.readlines()]
    data = make_grid(data)
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
