from argparse import ArgumentParser

FILEPATH = '../data/day_2_1.txt'

# 1 for Rock, 2 for Paper, and 3 for Scissors
# A for Rock, B for Paper, and C for Scissors
# X for Rock, Y for Paper, and Z for Scissors
MOVE_POINTS = {
    'A': 1,
    'B': 2,
    'C': 3,
    'X': 1,
    'Y': 2,
    'Z': 3
}


def solve(data):
    """
    To decide whose tent gets to be closest to the snack storage, a giant Rock Paper Scissors tournament is already
    in progress. one Elf gives you an encrypted strategy guide (your puzzle input)
    The first column is what your opponent is going to play: A for Rock, B for Paper, and C for Scissors.
    ** The second column must be what you should play in response: X for Rock, Y for Paper, and Z for Scissors. **

    Your total score is the sum of your scores for each round. The score for a single round is the score for the shape
    you selected (1 for Rock, 2 for Paper, and 3 for Scissors) plus the score for the outcome of the round (0 if you
    lost, 3 if the round was a draw, and 6 if you won).

    What would your total score be if everything goes exactly according to your strategy guide?

    :param data: list, list with strings of 2 space-seperated letters, e.g. ['A Z', 'B X', ..]
    :return: int, Total score
    """
    total_points = 0
    for round in data:
        move_elf, move_self = round.split(' ')
        move_elf = MOVE_POINTS[move_elf]
        move_self = MOVE_POINTS[move_self]

        total_points += move_self

        if move_elf == move_self:
            # draw
            total_points += 3

        elif ((move_elf == 1 and move_self == 3) or
              (move_elf == 2 and move_self == 1) or
              (move_elf == 3 and move_self == 2)):
            # Elf wins
            total_points += 0

        else:
            # Self wins
            total_points += 6

    return total_points


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
