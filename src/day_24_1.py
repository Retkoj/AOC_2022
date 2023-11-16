from argparse import ArgumentParser
from collections import deque
from copy import copy
from math import gcd
from queue import PriorityQueue

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


def heuristic(current_cell, target_cell):
    """Manhattan distance as heuristic function"""
    return sum([abs(a - b) for a, b in zip(current_cell, target_cell)])

def a_star(start_node, target_node, all_locations, blizzard_locations_at_t, walls):
    queue = PriorityQueue()
    time = 0
    # queue.put((heuristic(start_node, target_node), (time + heuristic(start_node, target_node)), time, start_node))
    set_queue = {(heuristic(start_node, target_node), (time + heuristic(start_node, target_node)), time, start_node)}
    a_path = {}
    g_scores = {row: float("inf") for row in all_locations}
    g_scores[start_node] = 0
    f_scores = {row: float("inf") for row in all_locations}
    f_scores[start_node] = heuristic(start_node, target_node)
    # search_path = [start_node]
    target_found = False

    while not target_found:
        # h, f, time, current_node = queue.get()
        set_queue = set(sorted(set_queue))
        h, f, time, current_node = set_queue.pop()
        # search_path.append(current_node)
        print(f"h: {h}, f: {f}, time: {time}, current_node: {current_node}")
        # print_board(current_node, blizzard_locations_at_t, walls, time, height, width)
        if current_node == target_node:
            return time

        possible_moves = get_possible_moves(current_node)
        open_locations = get_open_locations_at_t(all_locations, blizzard_locations_at_t, time + 1)
        valid_moves = possible_moves.intersection(open_locations)
        for child_node in valid_moves:
            tmp_g = time + 1
            tmp_h = heuristic(child_node, target_node)
            tmp_f = tmp_g + tmp_h

            # if tmp_f < f_scores[child_node] or len(valid_moves) == 1:
            a_path[child_node] = current_node
            g_scores[child_node] = tmp_g
            f_scores[child_node] = tmp_f
            # queue.put((tmp_h, tmp_f, tmp_g, child_node))
            set_queue.add((tmp_h, tmp_f, tmp_g, child_node))


PATHS = []


def dfs(start_node, target_node, all_locations, blizzard_locations_at_t, lcm):

    queue = deque([(0, start_node)])

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


def walk_paths(current_node, end_node, path, time, all_locations, blizzard_locations_at_t):
    # if end reached, break
    if current_node == end_node:
        PATHS.append(path)

    else:
        possible_moves = get_possible_moves(current_node)
        open_locations = get_open_locations_at_t(all_locations, blizzard_locations_at_t, time)
        valid_moves = possible_moves.intersection(open_locations)

        # if stuck, break
        if len(valid_moves) == 0:
            PATHS.append(path)

        else:
            if len(valid_moves) >= 2 and len(path) > 5:
                valid_moves = valid_moves.difference({path[-1]})

            for move in valid_moves:
                new_path = copy(path)
                new_path.append(move)
                walk_paths(move, end_node, new_path, time + 1, all_locations, blizzard_locations_at_t)


def solve(data):
    blizzard_locations_at_t = get_blizzard_locations(data)
    all_locations = get_all_locations(data)
    width, height = len(data[0]), len(data)
    end_node = (height - 1, width - 2)
    lcm = height * width // gcd(height, width)

    # walls = get_wall_locations(data)
    # search_path, a_path, fwd_path = a_star((0, 1), end_node, all_locations, blizzard_locations_at_t, walls)
    # steps = a_star((0, 1), end_node, all_locations, blizzard_locations_at_t, walls)
    # print(fwd_path)
    steps = dfs((0, 1), end_node, all_locations, blizzard_locations_at_t, lcm)
    return steps


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
