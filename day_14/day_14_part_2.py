from collections import Counter

from day_14.conf import input_polymer_string, input_polymerization_rules
from test_dsl import ReadableTestCase, parameterized_test


def calculate_overall_occurrences(polymer_string, polymerization_rules, steps):
    lookup_table = calculate_lookup_tables(polymerization_rules, for_steps=steps)

    overall_counter = Counter()

    for pair in (polymer_string[i:i + 2] for i, _ in enumerate(polymer_string) if len(polymer_string[i:i + 2]) == 2):
        overall_counter.update(lookup_table[pair])

    overall_counter.subtract(polymer_string[1:-1])

    return overall_counter


def calculate_lookup_tables(polymerization_rules, for_steps=1, base_lookup=None):
    if base_lookup is None:
        base_lookup = {pair: Counter(f'{pair[0]}{polymerization_rules[pair]}{pair[1]}')
                       for pair
                       in polymerization_rules}

    if for_steps != 1:
        return calculate_lookup_tables(polymerization_rules, for_steps - 1,
                                       {
                                           pair: get_next_lookup_level_counter(pair, polymerization_rules, base_lookup)
                                           for pair
                                           in base_lookup
                                       })

    return base_lookup


def get_next_lookup_level_counter(pair, polymerization_rules, current_lookup_table):
    new_polymer_string = f'{pair[0]}{polymerization_rules[pair]}{pair[1]}'

    left_child_pair, right_child_pair = new_polymer_string[:2], new_polymer_string[-2:]
    return current_lookup_table[left_child_pair] + current_lookup_table[right_child_pair] - Counter(new_polymer_string[1])


class OccurrenceCalculatorTest(ReadableTestCase):
    def setUp(self) -> None:
        self.polymerization_rules = {'CH': 'B', 'HH': 'N', 'CB': 'H', 'NH': 'C', 'HB': 'C', 'HC': 'B', 'HN': 'C',
                                     'NN': 'C', 'BH': 'H', 'NC': 'B', 'NB': 'B', 'BN': 'B', 'BB': 'N', 'BC': 'B',
                                     'CC': 'N', 'CN': 'C', }

    @parameterized_test(params=[
        ('NNCB', 1, Counter('NCNBCHB')),
        ('NNCB', 2, Counter('NBCCNBBBCBHCB')),
        ('NNCB', 10, Counter(N=865, B=1749, H=161, C=298)),
        ('NNCB', 20, Counter(N=1003774, B=2009315, H=47997, C=84643)),
        ('NNCB', 30, Counter(N=1061265944, B=2122542413, H=13713104, C=23704012)),
        ('NNCB', 40, Counter(N=1096047802353, B=2192039569602, H=3849876073, C=6597635301)),
    ])
    def test_calculate_overall_occurrences(self, given_polymer, given_steps, expected_count):
        actual = calculate_overall_occurrences(given_polymer, self.polymerization_rules, given_steps)
        self.expect(actual).to_be(expected_count)


if __name__ == "__main__":
    rules = input_polymerization_rules
    start_string = input_polymer_string
    steps = 40
    print(calculate_overall_occurrences(start_string, rules, steps).most_common())
