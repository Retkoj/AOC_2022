from argparse import ArgumentParser

FILEPATH = '../data/day_6_1.txt'


def solve(data):
    message = list(data)
    i = 4
    while i < len(message):
        if len(set(message[i - 4: i])) == 4:
            return i
        i += 1
    return -1


def read_file(file_path):
    with open(file_path) as file:
        data = file.read()

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
