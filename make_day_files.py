from argparse import ArgumentParser
from pathlib import Path


def make_day_files(day_number: str):
    """
    Creates:
      - ./src/day_[day_number]_1.py
      - ./src/day_[day_number]_2.py
      - ./data/day_[day_number]_1.txt
      - ./data/day_[day_number]_2.txt

    The .py file is created with the template provided in ./stub.py

    :param day_number: number of the day
    """
    for i in [1, 2]:
        input_file = Path('./data') / f'day_{day_number}_{i}.txt'
        with open(str(input_file), 'w+') as in_file:
            in_file.write('')
            print('Created input file: {}'.format(input_file))

        file_path = Path('./src') / f'day_{day_number}_{i}.py'
        if file_path.exists():
            print('{} already exists'.format(file_path))
        else:
            with (open(str(file_path), 'w+') as new_file,
                 open(str(Path().cwd() / 'stub.py'), 'r') as stub_file):
                for line in stub_file.readlines():
                    if line == 'FILEPATH = ""\n':
                        # Input is usually the same for both stars
                        line = f"FILEPATH = '../data/day_{day_number}_1.txt'\n"
                    new_file.write(line)
                print('Created file {}'.format(file_path))


if __name__ == '__main__':
    argparser = ArgumentParser()
    argparser.add_argument('day', type=int, help="Puzzle day, integer")
    args = argparser.parse_args()
    make_day_files(args.day)
