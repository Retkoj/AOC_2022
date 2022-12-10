from argparse import ArgumentParser

FILEPATH = '../data/day_10_1.txt'


class CPU:
    def __init__(self):
        self.current_cycle = 0
        self.current_crt_position = 0
        self.current_line = 0
        self.x = 1
        self.current_signal_strength = 0
        self.sprite = [0, 1, 2]
        self.visual_output = {}

    def noop(self):
        self.current_cycle += 1
        self.draw_pixel()

    def addx(self, amount):
        self.current_cycle += 1
        self.draw_pixel()

        self.current_cycle += 1
        self.draw_pixel()
        self.x += amount
        self.set_sprite()

    def set_sprite(self):
        self.sprite = [self.x - 1, self.x, self.x + 1]

    def draw_pixel(self):
        self.visual_output[self.current_line] = self.visual_output.get(self.current_line, [])
        if self.current_crt_position in self.sprite:
            self.visual_output[self.current_line].append('#')
        else:
            self.visual_output[self.current_line].append('.')
        self.current_crt_position += 1

        if self.current_crt_position == 40:
            self.current_crt_position = 0
            self.current_line += 1

    def print_output(self):
        for line, values in self.visual_output.items():
            print(values)


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
    cpu.print_output()
    return 0


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
