from argparse import ArgumentParser

FILEPATH = '../data/day_9_1.txt'


class HeadTail:
    def __init__(self):
        self.head = (0, 0)
        self.tail = (0, 0)
        self.tail_locations = [(0, 0)]
        self.last_move = None

    def is_corner(self, move):
        horizontal = ['L', 'R']
        vertical = ['D', 'U']
        if ((self.last_move in horizontal and move in vertical) or
            (self.last_move in vertical and move in horizontal)):
            return True
        else:
            return False

    def is_adjacent(self, head_loc):
        head_y, head_x = head_loc
        tail_y, tail_x = self.tail
        return (abs(head_x - tail_x) < 2) and abs(head_y - tail_y) < 2

    def make_move(self, move):
        direction, steps = move.split(' ')
        steps = int(steps)
        head_moves = []
        head_y, head_x = self.head
        if direction == 'L':
            head_moves = list(zip([head_y] * (steps + 1), range(head_x, head_x - steps - 1, -1)))
        if direction == 'R':
            head_moves = list(zip([head_y] * (steps + 1), range(head_x, head_x + steps + 1)))
        if direction == 'U':
            head_moves = list(zip(range(head_y, head_y + steps + 1), [head_x] * (steps + 1)))
        if direction == 'D':
            head_moves = list(zip(range(head_y, head_y - steps - 1, -1), [head_x] * (steps + 1)))
        self.head = head_moves[-1]

        i = 0
        has_to_move = False
        while i < len(head_moves):
            if not self.is_adjacent(head_moves[i]):
                has_to_move = True
                break
            i += 1
        if has_to_move:
            self.tail_locations += head_moves[i - 1: -1]
            self.tail = head_moves[-2]
        print(move)
        print(head_moves[i - 1: -1])
        print(self.tail)

        # if self.last_move is None:
        #     self.tail = head_moves[-1]  # next to last
        #     self.tail_locations += head_moves[:-1]
        # elif self.is_corner(direction):
        #     if len(head_moves) > 2:
        #         self.tail = head_moves[-2]
        #         self.tail_locations += head_moves[1:-1]  #
        # elif not self.is_corner(direction):
        #     if direction == self.last_move:
        #         self.tail = head_moves[-2]
        #         self.tail_locations += head_moves[:-1]
        #     elif direction != self.last_move:
        #         # moves over tail
        #         if len(head_moves) > 1:
        #             self.tail = head_moves[-2]
        #             self.tail_locations += head_moves[:-1]

        self.last_move = direction

    def count_locations(self):
        # return count of unique locations
        return len(list(set(self.tail_locations)))

    def plot_locations(self):
        print(self.tail_locations)


def solve(data):
    head_tail = HeadTail()
    for move in data:
        head_tail.make_move(move)
    total = head_tail.count_locations()
    head_tail.plot_locations()
    return total


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
