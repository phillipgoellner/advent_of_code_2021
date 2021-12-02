from day_02.conf import input_values
from day_02.day_2_part_1 import parse_line
from test_dsl import ReadableTestCase, parameterized_test


def calculate_aim_movement(given_position, given_command):
    command, distance = given_command
    x, y, aim = given_position

    if command == 'down':
        return x, y, aim + distance
    if command == 'up':
        return x, y, aim - distance
    return x + distance, y + (distance * aim), aim


def calculate_end_position_with_aim(given):
    commands = [parse_line(cmd) for cmd in given]
    position = (0, 0, 0)

    for command in commands:
        position = calculate_aim_movement(position, command)

    return position


class AimMovement(ReadableTestCase):
    @parameterized_test(params=[
        ((0, 0, 0), ('forward', 1), (1, 0, 0)),
        ((0, 0, 0), ('down', 1), (0, 0, 1)),
        ((0, 0, 1), ('up', 1), (0, 0, 0)),
        ((0, 0, 1), ('forward', 1), (1, 1, 1)),
        ((0, 0, 1), ('forward', 1), (1, 1, 1)),
    ])
    def test_should_calculate_aimed_move(self, given_position, given_command, expected_position):
        actual = calculate_aim_movement(given_position, given_command)
        self.expect(actual).to_be(expected_position)


class AimCommandChainTest(ReadableTestCase):
    @parameterized_test(params=[
        (['forward 1'], (1, 0, 0)),
        (['forward 1', 'down 1'], (1, 0, 1)),
        (['forward 5', 'down 5', 'forward 8', 'up 3', 'down 8', 'forward 2'], (15, 60, 10)),
    ])
    def test_should_execute_command_chain(self, given, expected_position):
        actual = calculate_end_position_with_aim(given)
        self.expect(actual).to_be(expected_position)


if __name__ == "__main__":
    print(calculate_end_position_with_aim(input_values))
