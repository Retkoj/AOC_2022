import ast
from argparse import ArgumentParser

FILEPATH = '../data/day_13_1.txt'


def compare_ints(li, ri):
    if li < ri:
        return True
    elif li > ri:
        return False
    else:
        return 'continue'


def compare_pairs(lhs, rhs):
    index = 0
    while index < min(len(lhs), len(rhs)):
        i = lhs[index]
        j = rhs[index]
        if type(i) == int == type(j):
            right_order = compare_ints(i, j)
            if right_order != 'continue':
                return right_order
        elif type(i) == list == type(j):
            right_order = compare_pairs(i, j)
            if right_order != 'continue':
                return right_order
        elif type(i) == list and type(j) == int:
            j = [j]
            right_order = compare_pairs(i, j)
            if right_order != 'continue':
                return right_order
        elif type(j) == list and type(i) == int:
            i = [i]
            right_order = compare_pairs(i, j)
            if right_order != 'continue':
                return right_order
        index += 1
    if len(lhs) < len(rhs):
        return True
    elif len(lhs) > len(rhs):
        return False
    else:
        return 'continue'


def insertion_sort(packets):
    for i in range(1, len(packets)):
        j = i - 1
        current_value = packets[i]
        while j >= 0 and compare_pairs(current_value, packets[j]):
            packets[j + 1] = packets[j]
            j -= 1
        packets[j + 1] = current_value
    return packets


def solve(data):
    total = 0
    data.append([[2]])
    data.append([[6]])
    right_order_pairs = insertion_sort(data)
    p2 = right_order_pairs.index([[2]]) + 1
    p6 = right_order_pairs.index([[6]]) + 1
    print(right_order_pairs)
    return p2 * p6


def read_file(file_path):
    with open(file_path) as file:
        data = [ast.literal_eval(i.strip('\n')) for i in file.readlines() if i != '\n']

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
