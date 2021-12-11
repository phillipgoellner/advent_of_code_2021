from day_10.conf import input_lines
from day_10.day_10_part_1 import opening_chars, char_mapping, get_first_corrupt_character
from test_dsl import ReadableTestCase, parameterized_test

char_scores = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}


def get_autocomplete_string(syntax_line) -> str:
    chars = []
    completion_string = ''

    for char in syntax_line:
        if char in opening_chars:
            chars.append(char)
        else:
            last_opening_char = chars.pop()
            if char != char_mapping[last_opening_char]:
                return char
    for char in chars:
        completion_string = f'{char_mapping[char]}{completion_string}'

    return completion_string


def calculate_completion_score(completion_line) -> int:
    score = 0

    for char in completion_line:
        score *= 5
        score += char_scores[char]

    return score


def get_winning_score(scores):
    sorted(scores)
    return sorted(scores)[int(len(scores) / 2)]


def determine_overall_winning_score(syntax_lines):
    syntax_lines = [line for line in syntax_lines if get_first_corrupt_character(line) == '']
    completion_lines = [get_autocomplete_string(line) for line in syntax_lines]
    completion_scores = [calculate_completion_score(line) for line in completion_lines]

    return get_winning_score(completion_scores)


class CompletionTest(ReadableTestCase):
    @parameterized_test(params=[
        ('[({(<(())[]>[[{[]{<()<>>', '}}]])})]'),
        ('[(()[<>])]({[<{<<[]>>(', ')}>]})'),
    ])
    def test_autocompletion_string(self, given, expected):
        actual = get_autocomplete_string(given)
        self.expect(actual).to_be(expected)

    @parameterized_test(params=[
        ('}}]])})]', 288957),
        (')}>]})', 5566),
    ])
    def test_calculate_completion_score(self, given, expected):
        actual = calculate_completion_score(given)
        self.expect(actual).to_be(expected)

    def test_get_winning_score(self):
        actual = get_winning_score([288957, 5566, 1480781, 995444, 294])
        self.expect(actual).to_be(288957)

    def test_determine_overall_winning_score(self):
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
        actual = determine_overall_winning_score(given)
        self.expect(actual).to_be(288957)


if __name__ == "__main__":
    print(determine_overall_winning_score(input_lines))
