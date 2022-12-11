import math
import re
from argparse import ArgumentParser
from dataclasses import dataclass

FILEPATH = '../data/day_11_1.txt'


@dataclass
class Monkey:
    number: int
    starting_items: list
    items: list
    total_items_checked: int
    operation: tuple
    test: dict

    def add_item(self, item):
        self.items.append(item)

    def get_all_items(self):
        self.total_items_checked += len(self.items)
        items = self.items
        self.items = []
        return items

    def get_item(self):
        if len(self.items) > 0:
            self.total_items_checked += 1
            return self.items.pop(0)
        else:
            return -1

    def do_operation(self, item):
        lhs = item

        if self.operation[2] == 'old':
            rhs = item
        else:
            rhs = int(self.operation[2])

        if self.operation[1] == '*':
            return lhs * rhs
        elif self.operation[1] == '+':
            return lhs + rhs
        elif self.operation[1] == '-':
            return lhs - rhs
        elif self.operation[1] == '/':
            return lhs / rhs


class MonkeyGame:
    def __init__(self):
        self.monkeys = {}
        self.total_monkey_business = None
        self.current_monkey = None
        self.n_monkeys = 0
        self.round = 0
        self.kgv = 1

    def calculate_kgv(self):
        """kleinst gemeenschappelijke veelvoud"""
        product = 1
        for monkey in self.monkeys.values():
            product *= monkey.test['divisible_by']
        self.kgv = product / math.gcd(*[monkey.test['divisible_by'] for monkey in self.monkeys.values()])

    def play_game(self):
        while self.round < 10000:
            self.play_round()
            self.round += 1

        self.calculate_total_monkey_business()
        return self.total_monkey_business

    def calculate_total_monkey_business(self):
        all = []
        for monkey in self.monkeys.values():
            all.append(monkey.total_items_checked)
        all.sort(reverse=True)
        self.total_monkey_business = all[0] * all[1]

    def play_round(self):
        for n in range(0, self.n_monkeys):
            self.current_monkey = n
            monkey = self.monkeys[n]

            for item in monkey.get_all_items():
                updated_item = monkey.do_operation(item)
                less_worried = updated_item
                if updated_item > self.kgv:
                    less_worried = updated_item % self.kgv
                if less_worried % monkey.test['divisible_by'] == 0:
                    self.monkeys[monkey.test['true']].add_item(less_worried)
                else:
                    self.monkeys[monkey.test['false']].add_item(less_worried)

    def parse_monkey(self, monkey_text):
        for line in monkey_text.split('\n'):
            line = line.strip()
            if line.startswith('Monkey'):
                number = int(re.findall(r'(\d+)', line)[0])
                self.monkeys[number] = Monkey(number, [], [], 0, (), {})
                self.current_monkey = number
            elif line.startswith('Starting items:'):
                items = [int(n) for n in re.findall(r'(\d+),?', line)]
                self.monkeys[self.current_monkey].items = items
                self.monkeys[self.current_monkey].starting_items = items
            elif line.startswith('Operation:'):
                self.monkeys[self.current_monkey].operation = re.findall(r'.+new = (.+) (.) (.+)', line)[0]
            elif line.startswith('Test:'):
                divisible_by = int(re.findall(r'(\d+)', line)[0])
                self.monkeys[self.current_monkey].test['divisible_by'] = divisible_by
            elif line.startswith('If true:'):
                monkey_n = int(re.findall(r'(\d+)', line)[0])
                self.monkeys[self.current_monkey].test['true'] = monkey_n
            elif line.startswith('If false:'):
                monkey_n = int(re.findall(r'(\d+)', line)[0])
                self.monkeys[self.current_monkey].test['false'] = monkey_n
        self.n_monkeys = max(self.n_monkeys, len(self.monkeys.keys()))
        self.calculate_kgv()


def solve(data):
    monkey_game = MonkeyGame()
    for monkey in data:
        monkey_game.parse_monkey(monkey)

    total = monkey_game.play_game()
    return total


def read_file(file_path):
    with open(file_path) as file:
        data = file.read()
    monkeys = [i.strip('\n') for i in data.split('\n\n')]

    print(f"INPUT DATA:\n{monkeys}\n")
    return monkeys


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
