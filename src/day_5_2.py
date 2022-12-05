import re
from argparse import ArgumentParser

FILEPATH = '../data/day_5_1.txt'


class CrateStacks:
    def __init__(self):
        self.stacks = {}

    def add_crate(self, stack, crate):
        if stack in self.stacks.keys():
            # insert at beginning
            self.stacks[stack].insert(0, crate)
        else:
            self.stacks[stack] = [crate]

    def move_crate(self, move_from, move_to, n=1):
        # get crates at once, now returns list:
        crates = self.stacks[move_from][-1 * n:]
        for _ in range(0, n):
            # pop from stack
            self.get_crate_from_stack(move_from)

        if move_to in self.stacks.keys():
            # when in play, add to end
            self.stacks[move_to] += crates
        else:
            self.stacks[move_to] = crates

    def get_crate_from_stack(self, stack):
        return self.stacks[stack].pop()

    def print_stack(self):
        for i in range(0, len(self.stacks.keys())):
            print(f'{i + 1}: {self.stacks[i + 1]}')


def parse_crate_line(line: str, crate_stacks):
    crates = re.findall(r'\[(\w+)\]', line)
    for start, crate in enumerate(crates):
        sub_line = line[start * 4:]  # Account for multiple same lettered crates
        stack = int(((sub_line.index(crate) + (start * 4) - 1) / 4) + 1)
        crate_stacks.add_crate(stack, crate)


def make_move(move_line, crate_stacks: CrateStacks):
    move = re.findall(r'(\d+)', move_line)
    crate_stacks.move_crate(int(move[1]), int(move[2]), n=int(move[0]))


def solve(data):
    crate_stacks = CrateStacks()
    i = 0
    line = data[i]
    while '1   2   3   4   5   6   7   8   9' not in line:
        parse_crate_line(line, crate_stacks)
        i += 1
        line = data[i]
    crate_stacks.print_stack()
    i += 2
    while i < len(data):
        line = data[i]
        make_move(line, crate_stacks)
        print(line)
        crate_stacks.print_stack()
        i += 1

    answer = ''
    for i in range(1, 10):
        answer += crate_stacks.get_crate_from_stack(i)
    return answer


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
