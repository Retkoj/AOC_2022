import math
import re
from argparse import ArgumentParser

FILEPATH = '../data/day_15_1.txt'

if FILEPATH == '../data/day_15_2.txt':
    LINE = 10
else:
    LINE = 2000000


def manhattan_distance(lhs, rhs):
    dist = [abs(a - b) for a, b in zip(lhs, rhs)]
    return sum(dist)


def count_places(final_ranges, beacons):
    """

    :param final_ranges:

    :param beacons: list of known beacons; to be removed from line
    :return:
    """
    total = 0
    for start, end in final_ranges.items():
        total += abs((end + 1) - start)
        for b in beacons:
            if b[0] in range(start, end + 1):
                total -= 1
    return total


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
            if line_range[0] in range(start, end + 1) or line_range[1] in range(start, end + 1):
                new_start = min(line_range[0], start)
                new_end = max(line_range[1], end)
                new_ranges[new_start] = new_end
            else:
                new_ranges[start] = end
                new_ranges[line_range[0]] = line_range[1]
        final_range = new_ranges
    return final_range


def find_overlap_on_line(sensor_beacon_distances):
    diffs_in_range = {}
    for sensor, m_distance in sensor_beacon_distances.items():
        diff = abs(sensor[1] - LINE)
        if diff <= m_distance:
            diffs_in_range[sensor] = diff

    range_one_line = []
    for s, d in diffs_in_range.items():
        spread = sensor_beacon_distances[s] - d
        if s[0] >= 0:
            range_one_line.append((s[0] - spread, s[0] + spread))
            # range_one_line.append(range(s[0] - spread, s[0] + spread + 1))
        else:
            range_one_line.append((s[0] + spread, s[0] - spread))
            # range_one_line.append(range(s[0] + spread, s[0] - spread - 1))

    # TODO remove known beacons

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
    ranges = find_overlap_on_line(sensor_beacon_distances)
    final_ranges = minimize_range(ranges)
    beacons_on_line = list(set([b for b in sensors.values() if b[1] == LINE]))
    outcome = count_places(final_ranges, beacons_on_line)
    return outcome


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
