from argparse import ArgumentParser
from copy import deepcopy
from dataclasses import dataclass

FILEPATH = '../data/day_20_1.txt'

@ dataclass
class Item:
    original_index: int
    value: int
    current_index: int


def find_grove_numbers(final_list):
    zero_index = [item for item in final_list if item.value == 0][0].current_index
    thousand = (zero_index + 1001) % len(final_list)
    thousand_value = [item for item in final_list if item.current_index == thousand][0].value
    twothousand = (zero_index + 2001) % len(final_list)
    twothousand_value = [item for item in final_list if item.current_index == twothousand][0].value
    threethousand = (zero_index + 3001) % len(final_list)
    threethousand_value = [item for item in final_list if item.current_index == threethousand][0].value
    print(f"{thousand_value} + {twothousand_value} + {threethousand_value}")
    return thousand_value + twothousand_value + threethousand_value


def calculate_new_index(current_index, move, list_length, index_items, item):
    new_index = (current_index + move)
    if new_index > (list_length - 1):
        new_index = (new_index % list_length) + 1
    elif new_index == (list_length - 1):
        new_index = 0
    elif new_index < 0:
        new_index = (new_index % list_length) - 1
    elif new_index == 0:
        new_index = list_length - 1

    for n in index_items:
        if n.current_index > current_index:
            # move left when removing item
            n.current_index -= 1

        if n.current_index >= new_index:
            # Move right when inserting item
            n.current_index += 1
    item.current_index = new_index
    return index_items


def print_list(index_items):
    out = [0] * len(index_items)
    for item in index_items:
        out[item.current_index] = item.value
    print(out)


def move_items(new_index, item, current_list):
    insert_value = current_list.pop(item.current_index)
    new_list = current_list[:new_index] + [insert_value] + current_list[new_index:]
    return new_list


def solve(data):
    index_items = [Item(i, value, i) for i, value in enumerate(data)]
    current_round = 0
    target_round = 1
    while current_round < target_round:
        for index in range(0, len(index_items)):
            item = [n for n in index_items if n.original_index == index][0]
            if item.value != 0:
                index_items = calculate_new_index(item.current_index, item.value, len(index_items), index_items, item)
                # print_list(index_items)

        current_round += 1
    grove_number = find_grove_numbers(index_items)
    return grove_number


def read_file(file_path):
    with open(file_path) as file:
        data = [int(i.strip('\n')) for i in file.readlines()]

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
