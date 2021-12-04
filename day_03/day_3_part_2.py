from day_03.conf import input_values
from day_03.day_3_part_1 import parse_diagnostics, get_bit_population_for_position, convert_rate_to_decimal
from test_dsl import ReadableTestCase, parameterized_test


def get_oxygen_rating(given_diagnostics):
    index = 0
    given_diagnostics = parse_diagnostics(given_diagnostics)

    while len(given_diagnostics) > 1:
        bit_population = get_bit_population_for_position(given_diagnostics, index)
        if bit_population.get(0, 0) > bit_population.get(1, 0):
            most_common_bit = 0
        else:
            most_common_bit = 1
        given_diagnostics = [line for line in given_diagnostics if line[index] == most_common_bit]
        index += 1

    return given_diagnostics[0]


def get_co2_rating(given_diagnostics):
    index = 0
    given_diagnostics = parse_diagnostics(given_diagnostics)

    while len(given_diagnostics) > 1:
        bit_population = get_bit_population_for_position(given_diagnostics, index)
        if bit_population.get(0, 0) > bit_population.get(1, 0):
            least_common_bit = 1
        else:
            least_common_bit = 0
        given_diagnostics = [line for line in given_diagnostics if line[index] == least_common_bit]
        index += 1

    return given_diagnostics[0]


def get_life_support_rating(given_diagnostics):
    oxygen_rating = get_oxygen_rating(given_diagnostics)
    co2_rating = get_co2_rating(given_diagnostics)
    return convert_rate_to_decimal(oxygen_rating) * convert_rate_to_decimal(co2_rating)


class RatingDeterminationTest(ReadableTestCase):
    @parameterized_test(params=[
        (['0'], (0,)),
        (['01', '11', '10'], (1, 1,)),
        (['00100', '11110', '10110', '10111', '10101', '01111', '00111', '11100', '10000', '11001', '00010', '01010'],
         (1, 0, 1, 1, 1)),
    ])
    def test_find_oxygen_rating(self, given_diagnostics, expected_line):
        actual = get_oxygen_rating(given_diagnostics)
        self.expect(actual).to_be(expected_line)

    @parameterized_test(params=[
        (['0'], (0,)),
        (['01', '11', '10'], (0, 1,)),
        (['00100', '11110', '10110', '10111', '10101', '01111', '00111', '11100', '10000', '11001', '00010', '01010'],
         (0, 1, 0, 1, 0)),
    ])
    def test_find_co2_rating(self, given_diagnostics, expected_line):
        actual = get_co2_rating(given_diagnostics)
        self.expect(actual).to_be(expected_line)

    def test_get_life_support_rating(self):
        given_diagnostics = ['00100', '11110', '10110', '10111', '10101', '01111', '00111', '11100', '10000', '11001',
                             '00010', '01010']
        actual = get_life_support_rating(given_diagnostics)
        self.expect(actual).to_be(230)


if __name__ == "__main__":
    print(get_life_support_rating(input_values))
