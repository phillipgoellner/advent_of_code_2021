from functools import reduce

from day_10.conf import input_lines
from test_dsl import ReadableTestCase, parameterized_test

opening_chars = ['(', '{', '[', '<']
closing_chars = [')', '}', ']', '>']
char_mapping = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}

char_scoring = {
    '': 0,
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}


def is_incomplete_line(syntax_line) -> bool:
    open_count = reduce(lambda x, y: x + y, map(lambda char: 1 if char in opening_chars else 0, syntax_line), 0)
    close_count = reduce(lambda x, y: x + y, map(lambda char: 1 if char in closing_chars else 0, syntax_line), 0)

    return open_count != close_count


def get_first_corrupt_character(syntax_line) -> str:
    chars = []

    for char in syntax_line:
        if char in opening_chars:
            chars.append(char)
        else:
            last_opening_char = chars.pop()
            if char != char_mapping[last_opening_char]:
                return char

    return ''


def get_total_score(syntax_lines) -> int:
    syntax_lines = list(map(get_first_corrupt_character, syntax_lines))
    syntax_score = reduce(lambda x, y: x + y, map(lambda char: char_scoring[char], syntax_lines), 0)

    return syntax_score


class SyntaxTest(ReadableTestCase):
    @parameterized_test(params=[
        ('[({', True),
        ('[]', False),
        ('[)', False),
        ('[(])', False),
        ('{([])', True),
    ])
    def test_is_incomplete(self, given, expected):
        actual = is_incomplete_line(given)
        self.expect(actual).to_be(expected)

    @parameterized_test(params=[
        ('[}', '}'),
        ('[(>', '>'),
    ])
    def test_is_incomplete(self, given, expected):
        actual = get_first_corrupt_character(given)
        self.expect(actual).to_be(expected)

    def test_corruption_score(self):
        given = ['[({(<(())[]>[[{[]{<()<>>',
                 '[(()[<>])]({[<{<<[]>>(',
                 '{([(<{}[<>[]}>{[]{[(<()>',
                 '(((({<>}<{<{<>}{[]{[]{}',
                 '[[<[([]))<([[{}[[()]]]',
                 '[{[{({}]{}}([{[{{{}}([]',
                 '{<[[]]>}<{[{[{[]{()[[[]',
                 '[<(<(<(<{}))><([]([]()',
                 '<{([([[(<>()){}]>(<<{{',
                 '<{([{{}}[<[[[<>{}]]]>[]]']

        actual = get_total_score(given)
        self.expect(actual).to_be(26397)


if __name__ == "__main__":
    print(get_total_score(input_lines))
