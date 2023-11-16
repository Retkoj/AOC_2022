from argparse import ArgumentParser
from enum import Enum

FILEPATH = '../data/day_25_1.txt'


D_TO_P = {
    3: '=',
    4: '-',
    0: '0',
    1: '1',
    2: '2'
}

P_TO_D = {
    '=': -2,
    '-': -1,
    '0': 0,
    '1': 1,
    '2': 2
}

def decimal_to_pental(number: int):
    """Convert decimal number to number in pental system"""
    finished = False
    remainders = []
    while not finished:
        quotient = number // 5
        remainder = number % 5
        remainders.append(remainder)
        print(f"Q: {quotient}, R: {remainder}")
        if quotient == 0:
            break
        number = quotient

    # Waar nodig (>=3), 1 optellen bij de volgende
    updated = [remainders[0]]
    for n in range(0, len(remainders) - 1):
        nn = remainders[n + 1]
        if remainders[n] >= 3:
            nn += 1
        if nn > 4:
            nn = 0
        remainders[n + 1] = nn
        updated.append(nn)
    print(remainders)
    print(updated)

    updated.reverse()
    answer = ''
    for i, n in enumerate(updated):
        if i == 0 and n >=3:
            answer += '1'
        answer += D_TO_P[n]

    print(answer)
    return answer


def pental_to_decimal(number: str):
    number = list(number)
    number.reverse()
    answer = 0
    for i, n in enumerate(number):
        answer += P_TO_D[n] * 5**i
    return answer


def solve(data):
    total = sum([pental_to_decimal(d) for d in data])
    print(total)
    result = decimal_to_pental(total)

    return result


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
