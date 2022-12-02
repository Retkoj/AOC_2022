from argparse import ArgumentParser

FILEPATH = '../data/day_1_1.txt'


def solve(data):
    """
    Find the Elf carrying the most Calories. How many total Calories is that Elf carrying?

    :param data: List, the number of Calories contained by the various meals, snacks, rations, etc. the elves
        brought with them. Each Elf separates their own inventory from the previous Elf's inventory (if any)
        by a blank item.
    :return: int, Highest calory count
    """
    highest = 0
    current = 0
    for c in data:
        if c:
            current += int(c)
        else:
            if current > highest:
                highest = current
            current = 0
    if current > highest:
        highest = current
    return highest


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
