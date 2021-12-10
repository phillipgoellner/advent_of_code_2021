from typing import List
from functools import reduce

from day_08.conf import input_lines_seven_digits
from test_dsl import ReadableTestCase, parameterized_test


def parse_input_line(input_line: str) -> List[List[str]]:
    content = input_line.split(' | ')
    return [[value for value in c_part.split(' ')] for c_part in content]


def get_unique_digit_amount(input_lines: str):
    def count_unique_digits(line: List[List[str]]):
        line = line[1]
        instances = 0
        for element in line:
            if len(element) == 2:
                instances += 1
            if len(element) == 3:
                instances += 1
            if len(element) == 4:
                instances += 1
            if len(element) == 7:
                instances += 1
        return instances

    input_lines = input_lines.split('\n')
    input_lines = [parse_input_line(line) for line in input_lines]

    return reduce(lambda x, y: x + y, map(count_unique_digits, input_lines), 0)


class ParseTest(ReadableTestCase):
    @parameterized_test(params=[
        ('be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe',
         [['be', 'cfbegad', 'cbdgef', 'fgaecd', 'cgeb', 'fdcge', 'agebfd', 'fecdb', 'fabcd', 'edb'],
          ['fdgacbe', 'cefdb', 'cefbgd', 'gcbe']]),
        ('edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc',
         [['edbfga', 'begcd', 'cbg', 'gc', 'gcadebf', 'fbgde', 'acbgfd', 'abcde', 'gfcbed', 'gfec'],
          ['fcgedb', 'cgb', 'dgebacf', 'gc']]),
    ])
    def test_parse_input_line(self, given_line, expected_output):
        actual = parse_input_line(given_line)
        self.expect(actual).to_be(expected_output)

    @parameterized_test(params=[
        ("""be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc""", 5),
    ])
    def test_get_unique_digit_amount(self, given_lines, expected_output):
        actual = get_unique_digit_amount(given_lines)
        self.expect(actual).to_be(expected_output)


if __name__ == "__main__":
    print(get_unique_digit_amount(input_lines_seven_digits))
