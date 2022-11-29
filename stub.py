FILEPATH = ""


def solve(data):
    pass


def read_file(file_path):
    with open(file_path) as file:
        data = [i.strip('\n') for i in file.readlines()]
    return data


if __name__ == '__main__':
    input_data = read_file(FILEPATH)
    print(input_data)
    print(solve(input_data))
