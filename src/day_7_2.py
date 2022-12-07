from argparse import ArgumentParser
from pathlib import Path

FILEPATH = '../data/day_7_1.txt'


class DirParser:
    def __init__(self):
        self.root_dir = Path('day_7/root')
        self.current_dir = Path('day_7/root')

    def process_lines(self, lines):
        i = 0
        while i < len(lines):
            line = lines[i]
            values = line.split(' ')
            if values[0] == '$':
                # Command
                if values[1] == 'cd':
                    self.parse_cd(values[2])
                # ls doesn't do much in this setting
            else:
                self.parse_ls(values)
            i += 1

    def parse_cd(self, dir_name):
        if dir_name == '..':
            # Move up one level
            self.current_dir = self.current_dir.parent
        elif dir_name != '..':
            # move to specific dir
            if dir_name != '/':
                self.current_dir = self.current_dir / dir_name
            else:
                self.current_dir = self.root_dir
            Path(self.current_dir).mkdir(exist_ok=True, parents=True)

    def parse_ls(self, values):
        if values[0] == 'dir':
            # has dir
            (self.current_dir / values[1]).mkdir(exist_ok=True)
        else:
            # has file
            (self.current_dir / f"{values[0]}.aoc").touch(exist_ok=True)


def get_remove_candidates():
    total_space = 70000000
    total_used = sum([int(f.stem) for f in Path('day_7/root').rglob('**/*.aoc')])
    total_unused = total_space - total_used
    needed = 30000000

    # Min amount of space to remove
    min_needed = needed - total_unused

    candidates = []
    for d in Path('day_7').rglob('**/**'):
        if d.is_dir():
            size = sum([int(f.stem) for f in d.rglob('**/*.aoc')])
            if size >= min_needed:
                candidates.append(size)
    return candidates


def solve(data):
    dir_parser = DirParser()
    dir_parser.process_lines(data)
    candidates = get_remove_candidates()
    return min(candidates)


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
