from argparse import ArgumentParser
from collections import deque
from math import gcd

FILEPATH = '../data/day_24_1.txt'


def get_blizzard_locations(grid):
    start_locations = {}
    for i, row in enumerate(grid):
        for j, value in enumerate(row):
            if value.lower() in ['<', '>', '^', 'v']:
                start_locations[(i, j)] = value

    width, height = len(grid[0]), len(grid)

    blizzard_locations_at_t = {0: set(start_locations)}
    t = 0
    prev_locations = [(key, value) for key, value in start_locations.items()]
    while True:
        t += 1
        blizzard_locations_at_t[t] = set()
        new_locations = set()
        next_locations = []
        for location, direction in prev_locations:
            if direction == '<':
                move = (0, -1)
            elif direction == '>':
                move = (0, 1)
            elif direction == '^':
                move = (-1, 0)
            else:
                move = (1, 0)

            location = (location[0] + move[0], location[1] + move[1])
            if location[0] == 0:
                location = (height - 2, location[1])
            if location[0] == height - 1:
                location = (1, location[1])
            if location[1] == 0:
                location = (location[0], width - 2)
            if location[1] == width - 1:
                location = (location[0], 1)

            new_locations.add(location)
            next_locations.append((location, direction))

        if new_locations in blizzard_locations_at_t.values():
            print(f"Repeating blizzards pattern after {t} steps")
            break
        blizzard_locations_at_t[t] = new_locations
        prev_locations = next_locations

    return blizzard_locations_at_t


def get_wall_locations(grid) -> set:
    wall_locations = []
    for i, row in enumerate(grid):
        for j, value in enumerate(row):
            if value == '#':
                wall_locations.append((i, j))
    return set(wall_locations)


def get_all_locations(grid) -> set:
    """All storm locations and empty, thus not including walls"""
    all_locations = []
    for i, row in enumerate(grid):
        for j, value in enumerate(row):
            all_locations.append((i, j))
    walls = get_wall_locations(grid)
    valid_locations = set(all_locations).difference(walls)
    return valid_locations


def get_open_locations_at_t(all_locations, blizzards, t):
    if t > max(blizzards.keys()):
        t = t % max(blizzards.keys())

    return all_locations.difference(blizzards[t])


def get_possible_moves(location) -> set:
    """Four surrounding cells (NSEW) and current location"""
    moves = [(location[0] + 1, location[1]), (location[0], location[1] - 1), (location[0], location[1]),
             (location[0] - 1, location[1]), (location[0], location[1] + 1)]
    return set(moves)


def print_board(current_cell, blizzard_locations_at_t, walls, time, height, width):
    t = time % max(blizzard_locations_at_t.keys())
    grid = ''
    for i in range(height):
        for j in range(width + 1):
            if (i, j) in walls:
                grid += '#'
            elif (i, j) in blizzard_locations_at_t[t]:
                grid += '*'
            elif (i, j) == current_cell:
                grid += 'E'
            else:
                grid += '.'
        grid += '\n'
    print(f"time: {time}")
    print(f"E: {current_cell}")
    print(grid)
    print(blizzard_locations_at_t[t])


def dfs(start_node, start_time, target_node, all_locations, blizzard_locations_at_t, lcm):

    queue = deque([(start_time, start_node)])

    seen = set()

    while queue:
        time, current_location = queue.popleft()
        time += 1

        possible_moves = get_possible_moves(current_location)
        open_locations = get_open_locations_at_t(all_locations, blizzard_locations_at_t, time)

        for next_location in possible_moves.intersection(open_locations):

            if next_location == target_node:
                return time

            key = (next_location, time % lcm)
            if key not in seen:
                seen.add(key)
                queue.append((time, next_location))


def solve(data):
    blizzard_locations_at_t = get_blizzard_locations(data)
    all_locations = get_all_locations(data)
    width, height = len(data[0]), len(data)
    start_node = (0, 1)
    end_node = (height - 1, width - 2)
    lcm = height * width // gcd(height, width)

    minutes = dfs(start_node, 0, end_node, all_locations, blizzard_locations_at_t, lcm)
    print(f"first go: {minutes}")
    tmp = dfs(end_node, minutes, start_node, all_locations, blizzard_locations_at_t, lcm)
    print(f"return: {tmp - minutes}")
    minutes = tmp
    tmp = dfs(start_node, minutes, end_node, all_locations, blizzard_locations_at_t, lcm)
    print(f"second go: {tmp - minutes}")
    minutes = tmp
    return minutes


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
