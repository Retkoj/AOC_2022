from argparse import ArgumentParser

FILEPATH = '../data/day_10_1.txt'


class CPU:
    def __init__(self):
        self.current_cycle = 0
        self.x = 1
        self.current_signal_strength = 0
        self.total = 0

    def noop(self):
        self.current_cycle += 1
        self.set_signal_strength()

    def addx(self, amount):
        self.current_cycle += 1
        self.set_signal_strength()
        self.current_cycle += 1
        self.set_signal_strength()
        self.x += amount

    def set_signal_strength(self):
        self.current_signal_strength = self.current_cycle * self.x
        if self.current_cycle in [20, 60, 100, 140, 180, 220]:
            self.total += self.current_signal_strength


def solve(data):
    cpu = CPU()
    for line in data:
        if line == 'noop':
            cpu.noop()
        else:
            action = line.split(' ')[0]
            if action == 'addx':
                amount = int(line.split(' ')[1])
                cpu.addx(amount)

    return cpu.total


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
