from argparse import ArgumentParser

from networkx import Graph

FILEPATH = '../data/day_18_1.txt'


class CountSides:
    def __init__(self, data):
        self.graph = Graph()
        self.data = data

    def parse(self):
        for line in self.data:
            numbers = tuple(int(n) for n in line.split(','))
            self.graph.add_node(numbers)

    def walk_graph(self):
        all_nodes = list(self.graph.nodes())
        for i in range(0, (len(all_nodes) - 1)):
            current_node = all_nodes[i]
            for target_node in all_nodes[i + 1:]:
                c = 0
                for j in range(0, 3):
                    match = 1 if target_node[j] == current_node[j] else 0
                    if match == 0 and abs(target_node[j] - current_node[j]) == 1:
                        c += match
                    elif match == 0:
                        c += 100
                    else:
                        c += match

                if c == 2:
                    self.graph.add_edge(current_node, target_node)

    def count_sides(self):
        total = 0
        for node in self.graph.nodes():
            total += (6 - len(list(self.graph.neighbors(node))))
        return total


def solve(data):
    count_sides = CountSides(data)
    count_sides.parse()
    count_sides.walk_graph()
    total = count_sides.count_sides()
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
