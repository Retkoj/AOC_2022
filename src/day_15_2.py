import datetime
import re
from argparse import ArgumentParser

FILEPATH = '../data/day_15_1.txt'

MIN_X_Y = 0
if FILEPATH == '../data/day_15_2.txt':
    LINE = 20
    MAX_X_Y = 20
else:
    LINE = 4000000
    MAX_X_Y = 4000000


def manhattan_distance(lhs, rhs):
    dist = [abs(a - b) for a, b in zip(lhs, rhs)]
    return sum(dist)


def find_empty_space(final_ranges):
    within_line = []
    # Empty space is just a col coordinate
    empty_space = None
    for start, end in final_ranges.items():
        # if start >= MIN_X_Y or end <= MAX_X_Y:
        new_start = max(start, MIN_X_Y)
        new_end = min(MAX_X_Y, end)
        within_line.append((new_start, new_end))
    if len(within_line) > 1:
        within_line.sort()
        empty_space = within_line[0][1] + 1
    if len(within_line) == 1:
        if within_line[0][0] != MIN_X_Y:
            empty_space = 0
        elif within_line[0][1] != MAX_X_Y:
            empty_space = MAX_X_Y

    return empty_space


def minimize_range(ranges):
    """

    :param ranges: dict {start: end} all ranges
    :return:
    """
    ranges.sort()
    final_range = {}
    for line_range in ranges:
        new_ranges = {}
        if len(final_range.keys()) == 0:
            new_ranges[line_range[0]] = line_range[1]
        for start, end in final_range.items():
            if line_range[0] in range(start, end + 2) or line_range[1] in range(start, end + 2):
                new_start = min(line_range[0], start)
                new_end = max(line_range[1], end)
                new_ranges[new_start] = new_end
            else:
                new_ranges[start] = end
                new_ranges[line_range[0]] = line_range[1]
        final_range = new_ranges
    return final_range


def find_overlap_on_line(sensor_beacon_distances, line):
    diffs_in_range = {}
    for sensor, m_distance in sensor_beacon_distances.items():
        diff = abs(sensor[1] - line)
        if diff <= m_distance:
            diffs_in_range[sensor] = diff

    range_one_line = []
    for s, d in diffs_in_range.items():
        spread = sensor_beacon_distances[s] - d
        if s[0] >= 0:
            range_one_line.append((s[0] - spread, s[0] + spread))
        else:
            range_one_line.append((s[0] + spread, s[0] - spread))

    return range_one_line


def solve(data):
    sensors = {}
    sensor_beacon_distances = {}
    for line in data:
        numbers = [int(n) for n in re.findall(r'(-?\d+)', line)]
        sensors[(numbers[0], numbers[1])] = (numbers[2], numbers[3])
        sensor_beacon_distances[(numbers[0], numbers[1])] = manhattan_distance((numbers[0], numbers[1]),
                                                                               (numbers[2], numbers[3]))
    print(sensors)
    print(sensor_beacon_distances)
    empty_space = None
    for l in range(0, LINE + 1):
        ranges = find_overlap_on_line(sensor_beacon_distances, line=l)
        final_ranges = minimize_range(ranges)
        beacons_on_line = list(set([b for b in sensors.values() if b[1] == l]))
        outcome = find_empty_space(final_ranges)
        if outcome is not None:
            empty_space = (outcome, l)
            return empty_space
    return empty_space


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
    start_time = datetime.datetime.now()
    result = solve(input_data)
    final_result = (result[0] * 4000000) + result[1]
    print(f"{'-' * 100}\nOUTPUT: {final_result}")
    print(f"result in {datetime.datetime.now() - start_time}")
