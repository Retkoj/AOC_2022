from argparse import ArgumentParser

FILEPATH = '../data/day_2_1.txt'

# 1 for Rock, 2 for Paper, and 3 for Scissors
# A for Rock, B for Paper, and C for Scissors
MOVE_POINTS = {
    'A': 1,
    'B': 2,
    'C': 3
}

# X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win
ADVISED_OUTCOME = {
    'X': 0,
    'Y': 3,
    'Z': 6
}


def solve(data):
    """
    To decide whose tent gets to be closest to the snack storage, a giant Rock Paper Scissors tournament is already
    in progress. one Elf gives you an encrypted strategy guide (your puzzle input)
    The first column is what your opponent is going to play: A for Rock, B for Paper, and C for Scissors.
    ** The second column says how the round needs to end: X means you need to lose, Y means you need to end the round
    in a draw, and Z means you need to win. **

    Your total score is the sum of your scores for each round. The score for a single round is the score for the shape
    you selected (1 for Rock, 2 for Paper, and 3 for Scissors) plus the score for the outcome of the round (0 if you
    lost, 3 if the round was a draw, and 6 if you won).

    What would your total score be if everything goes exactly according to your strategy guide?

    :param data: list, list with strings of 2 space-seperated letters, e.g. ['A Z', 'B X', ..]
    :return: int, Total score
    :param data:
    :return:
    """
    total_points = 0
    for round in data:
        move_elf, outcome = round.split(' ')
        move_elf = MOVE_POINTS[move_elf]
        outcome = ADVISED_OUTCOME[outcome]

        total_points += outcome

        if outcome == 3:
            # If draw, make same move
            total_points += move_elf
        elif move_elf == 1:
            total_points += 2 if outcome == 6 else 3
        elif move_elf == 2:
            total_points += 3 if outcome == 6 else 1
        elif move_elf == 3:
            total_points += 1 if outcome == 6 else 2

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
