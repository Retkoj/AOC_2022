import re
from argparse import ArgumentParser

FILEPATH = '../data/day_4_1.txt'


def parse_pair(pairs):
    match_groups = re.findall(r'(\d+)-(\d+),(\d+)-(\d+)', pairs)
    p1, p2 = match_groups[0][:2], match_groups[0][2:]
    pair_1 = range(int(p1[0]), int(p1[1]) + 1)
    pair_2 = range(int(p2[0]), int(p2[1]) + 1)
    return pair_1, pair_2


def solve(data):
    total = 0
    for pairs in data:
        p1, p2 = parse_pair(pairs)
        if set(p1).issubset(set(p2)) or set(p2).issubset(set(p1)):
            total += 1
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
