import re
from argparse import ArgumentParser
from copy import deepcopy

FILEPATH = '../data/day_21_1.txt'


class NumberGame:
    def __init__(self, data):
        self.data = data
        self.monkeys = {}
        self.number_monkeys = []
        self.original_monkeys = {}

    def parse_data(self, human_value):
        for line in self.data:
            monkey, value = line.split(': ')
            if monkey == "humn":
                value = str(human_value)
            if value.isnumeric():
                self.monkeys[monkey] = {"value": int(value), "name": monkey,
                                        "lhs": '', "operation": '', "rhs": ''}
                self.number_monkeys.append(self.monkeys[monkey])
            else:
                lhs, operation, rhs = re.findall(r'(\w+) ([+-/*]) (\w+)', value)[0]
                self.monkeys[monkey] = {"lhs": lhs.strip(), "operation": operation, "rhs": rhs.strip(), "name": monkey}
        self.original_monkeys = deepcopy(self.monkeys)

    def find_human_path(self):
        pass

    def update_values(self):
        while len(self.number_monkeys) > 0:
            current_monkey = self.number_monkeys.pop(0)
            current_value = current_monkey['value']
            updatable_monkeys = {monkey: value for monkey, value in self.monkeys.items()
                                 if value['lhs'] == current_monkey['name'] or
                                 value['rhs'] == current_monkey['name']}
            for m, value in updatable_monkeys.items():
                if value['lhs'] == current_monkey['name']:
                    self.monkeys[m]['lhs'] = current_value
                elif value['rhs'] == current_monkey['name']:
                    self.monkeys[m]['rhs'] = current_value
                if (type(self.monkeys[m]['rhs']) in [int, float]) and (type(self.monkeys[m]['lhs']) in [int, float]):
                    if self.monkeys[m]['operation'] == '+':
                        self.monkeys[m]['value'] = self.monkeys[m]['lhs'] + self.monkeys[m]['rhs']
                    elif self.monkeys[m]['operation'] == '-':
                        self.monkeys[m]['value'] = self.monkeys[m]['lhs'] - self.monkeys[m]['rhs']
                    elif self.monkeys[m]['operation'] == '/':
                        self.monkeys[m]['value'] = self.monkeys[m]['lhs'] / self.monkeys[m]['rhs']
                    elif self.monkeys[m]['operation'] == '*':
                        self.monkeys[m]['value'] = self.monkeys[m]['lhs'] * self.monkeys[m]['rhs']
                    self.number_monkeys.append(self.monkeys[m])


def solve(data):
    number_game = NumberGame(data)
    winning_value = None
    for value in [1]:
        number_game.parse_data(human_value=value)
        number_game.update_values()
        print(f"lhs: {number_game.monkeys['root']['lhs']} == rhs: {number_game.monkeys['root']['rhs']}")
        if number_game.monkeys['root']['lhs'] == number_game.monkeys['root']['rhs']:
            winning_value = value
            break
    return winning_value


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
