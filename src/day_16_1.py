import re
from argparse import ArgumentParser
from copy import deepcopy

import networkx as nx

FILEPATH = '../data/day_16_2.txt'


def valves_left(graph):
    return [v for v in graph.nodes() if graph.nodes[v]['flow_rate'] > 0 and graph.nodes[v]['state'] == 'closed']

TRAVEL_PATHS = {}
def determine_values(graph, current_node, minutes_left, target_nodes):
    values = {}
    closest = None
    closest_value = float("inf")
    for node in target_nodes:
        # minutes to get to target + to open valve
        if not TRAVEL_PATHS.get((current_node, node), False):
            shortest_path = nx.shortest_path(graph, current_node, node)
            TRAVEL_PATHS[(current_node, node)] = shortest_path
        else:
            shortest_path = TRAVEL_PATHS[(current_node, node)]
        travel_minutes = len(shortest_path)
        closest = node if travel_minutes < closest_value else closest
        closest_value = travel_minutes if travel_minutes < closest_value else closest_value
        # potential added value
        if (minutes_left - travel_minutes) > 0:
            potential_value = graph.nodes[node]['flow_rate'] * (minutes_left - travel_minutes)
        else:
            potential_value = 0
        values[node] = potential_value
    return values, closest


def walk_all_paths(graph):
    paths = {}
    max_value = 0

    def traverse_graph(graph, current_node, minutes_left, path, total_value):
        v_left = valves_left(graph)
        if minutes_left <= 0 or len(v_left) == 0:
            paths[total_value] = path
            return
        potential_values, _ = determine_values(graph, current_node, minutes_left, v_left)
        potential_values = {c: v for c, v in potential_values.items() if v > 0}
        if len(potential_values.keys()) == 0:
            paths[total_value] = path
            return
        potential_values = dict(sorted(potential_values.items(), key=lambda item: item[1], reverse=True))
        for cave, potential_value in potential_values.items():
            if len(path) == 1 or (len(path) > 2 and cave != path[-2]):

                # open valve route
                if potential_value > 0:
                    new_path = deepcopy(path)
                    shortest_path = TRAVEL_PATHS[(current_node, cave)]
                    new_path += shortest_path[1:]
                    new_path.append(cave)
                    new_graph = deepcopy(graph)
                    new_graph.nodes[cave]['state'] = 'open'
                    value = total_value + potential_values[cave]
                    traverse_graph(new_graph, cave, minutes_left - len(shortest_path), new_path, value)

    current_node = 'AA'
    traverse_graph(graph, current_node, 30, ['AA'], 0)
    return paths


def find_paths(graph):
    """
    DD
    BB
    JJ
    HH
    EE
    :param graph:
    :return:
    """
    total_score = 0
    current_node = 'AA'
    minutes_left = 30
    while minutes_left > 0:
        v_left = valves_left(graph)
        potential_values, closest = determine_values(graph, current_node, minutes_left, v_left)
        if potential_values:
            # highest_value_node = max(potential_values, key=potential_values.get)
            highest_value_node = closest
            shortest_path = TRAVEL_PATHS[(current_node, highest_value_node)]
            minutes_left -= len(shortest_path)
            total_score += potential_values[highest_value_node]
            graph.nodes[highest_value_node]['state'] = 'open'
            current_node = highest_value_node
            print(highest_value_node)
        else:
            break
    return total_score


def parse_data(data):
    graph = nx.Graph()
    for line in data:
        tunnels = re.findall(r'([A-Z]{2})', line)
        flow_rate = int(re.findall(r'(\d+)', line)[0])
        main_node = tunnels[0]
        edge_nodes = tunnels[1:]

        if main_node in graph.nodes():
            graph.nodes[main_node]['flow_rate'] = flow_rate
            graph.nodes[main_node]['state'] = 'closed'
        else:
            graph.add_node(main_node)
            graph.nodes[main_node]['flow_rate'] = flow_rate
            graph.nodes[main_node]['state'] = 'closed'
        graph.add_nodes_from(edge_nodes)
        graph.add_edges_from([(main_node, e) for e in edge_nodes])

    return graph


def solve(data):
    graph = parse_data(data)
    total = find_paths(graph)
    # paths = walk_all_paths(graph)
    return total #  max(paths.keys())


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
