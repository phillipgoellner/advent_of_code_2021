from day_02.conf import input_values
from test_dsl import parameterized_test, ReadableTestCase


def parse_line(param: str):
    params = param.split(' ', 1)
    return params[0], int(params[1])


def calculate_movement(given_position, given_command):
    command, distance = given_command
    x, y = given_position

    if command == 'up':
        return x, y - distance
    if command == 'down':
        return x, y + distance
    return x + distance, y


def calculate_end_position(given):
    commands = [parse_line(cmd) for cmd in given]
    position = (0, 0)

    for command in commands:
        position = calculate_movement(position, command)

    return position


class ParseTest(ReadableTestCase):
    @parameterized_test(params=[
        ('up 1', ('up', 1)),
        ('forward 1', ('forward', 1)),
        ('down 1', ('down', 1)),
        ('down 100', ('down', 100)),
    ])
    def test_parsing(self, given, expected_output):
        actual = parse_line(given)
        self.expect(actual).to_be(expected_output)


class MovementTest(ReadableTestCase):
    @parameterized_test(params=[
        ((0, 0), ('down', 1), (0, 1)),
        ((0, 1), ('up', 1), (0, 0)),
        ((0, 0), ('forward', 1), (1, 0)),
    ])
    def test_compute_movement(self, given_position, given_command, expected_position):
        actual = calculate_movement(given_position, given_command)
        self.expect(actual).to_be(expected_position)


class CommandChainTest(ReadableTestCase):
    @parameterized_test(params=[
        (['forward 1'], (1, 0)),
        (['forward 1', 'down 1'], (1, 1)),
        (['forward 5', 'down 5', 'forward 8', 'up 3', 'down 8', 'forward 2'], (15, 10)),
    ])
    def test_should_execute_command_chain(self, given, expected):
        actual = calculate_end_position(given)
        self.expect(actual).to_be(expected)


if __name__ == "__main__":
    print(calculate_end_position(input_values))
