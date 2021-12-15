from collections import Counter
from functools import reduce

from day_14.conf import input_polymer_string, input_polymerization_rules
from test_dsl import ReadableTestCase, parameterized_test


def polymerization_step(polymer_template, polymerization_rules):
    out = '_'

    polymer_pairs = [polymer_template[i:i + 2] for i, _ in enumerate(polymer_template) if
                     len(polymer_template[i:i + 2]) == 2]

    for pair in polymer_pairs:
        left, right = pair[0], pair[1]

        middle = polymerization_rules.get(pair, '')
        out = f'{out[:-1]}{left}{middle}{right}'

    return out


def get_most_common_element(polymer_string):
    return _char_dist(polymer_string)[0]


def get_least_common_element(polymer_string):
    return _char_dist(polymer_string)[-1]


def _char_dist(polymer_string):
    counter = Counter()

    for char in polymer_string:
        counter[char] += 1

    return counter.most_common()


def most_minus_least(polymer_string):
    _, most_count = get_most_common_element(polymer_string)
    _, least_count = get_least_common_element(polymer_string)

    return most_count - least_count


class PolymerizationTest(ReadableTestCase):
    def setUp(self) -> None:
        self.polymerization_rules = {'CH': 'B', 'HH': 'N', 'CB': 'H', 'NH': 'C', 'HB': 'C', 'HC': 'B', 'HN': 'C',
                                     'NN': 'C', 'BH': 'H', 'NC': 'B', 'NB': 'B', 'BN': 'B', 'BB': 'N', 'BC': 'B',
                                     'CC': 'N', 'CN': 'C', }

    @parameterized_test(params=[
        ('NNCB', 'NCNBCHB'),
        ('NCNBCHB', 'NBCCNBBBCBHCB'),
    ])
    def test_polymerization_step(self, polymer_template, expected_polymer):
        actual = polymerization_step(polymer_template, self.polymerization_rules)
        self.expect(actual).to_be(expected_polymer)

    @parameterized_test(params=[
        ('NBCCNBBBCBHCB', ('B', 6)),
    ])
    def test_get_most_common_element(self, polymer_string, expected_result):
        actual = get_most_common_element(polymer_string)
        self.expect(actual).to_be(expected_result)

    @parameterized_test(params=[
        ('NBCCNBBBCBHCB', ('H', 1)),
    ])
    def test_get_least_common_element(self, polymer_string, expected_result):
        actual = get_least_common_element(polymer_string)
        self.expect(actual).to_be(expected_result)


if __name__ == "__main__":
    polymer_string = input_polymer_string

    for _ in range(20):
        polymer_string = polymerization_step(polymer_string, input_polymerization_rules)

    print(most_minus_least(polymer_string))
