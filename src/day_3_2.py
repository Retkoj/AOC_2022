from argparse import ArgumentParser
from string import ascii_letters

FILEPATH = '../data/day_3_1.txt'


def solve(data):
    """
    Each rucksack has two large compartments. All items of a given type are meant to go into exactly one of the two
    compartments. The Elf that did the packing failed to follow this rule for exactly one item type per rucksack.
    The list of items for each rucksack is given as characters all on a single line. A given rucksack always has the
    same number of items in each of its two compartments, so the first half of the characters represent items in the
    first compartment, while the second half of the characters represent items in the second compartment.

    To help prioritize item rearrangement, every item type can be converted to a priority:
    - Lowercase item types a through z have priorities 1 through 26.
    - Uppercase item types A through Z have priorities 27 through 52.

    ** Every set of three lines in your list corresponds to a single group. **

    Find the item type that corresponds to the badges of each three-Elf group. What is the sum of the priorities of
    those item types?

    :param data: list of strings, The list of items for each rucksack is given as characters all on a single line.
    :return: int, sum of priorities
    """
    total = 0
    i = 0
    while i < (len(data) - 2):
        # Group of three bags:
        b1, b2, b3 = data[i], data[i + 1], data[i + 2]
        overlap = set(b1).intersection(set(b2)).intersection(b3)
        # Assumes there's only one overlapping item
        total += ascii_letters.index(list(overlap)[0]) + 1
        i += 3
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
