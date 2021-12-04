from day_03.conf import input_values
from test_dsl import ReadableTestCase, parameterized_test


def parse_diagnostics_line(given_line: str):
    return tuple([int(_) for _ in given_line])


def parse_diagnostics(given_diagnostics):
    return [parse_diagnostics_line(_) for _ in given_diagnostics]


def get_most_common_bit_for_position(given_diagnostics, given_position) -> int:
    bit_population = get_bit_population_for_position(given_diagnostics, given_position)
    if bit_population.get(0, 0) > bit_population.get(1, 0):
        return 0
    return 1


def get_bit_population_for_position(given_diagnostics, given_position):
    out = {}
    given_diagnostics = parse_diagnostics(given_diagnostics)

    for line in given_diagnostics:
        if line[given_position] == 0:
            if 0 in out:
                out[0] = 1 + out[0]
            else:
                out[0] = 1
        else:
            if 1 in out:
                out[1] = 1 + out[1]
            else:
                out[1] = 1

    return out


def get_gamma_rate(given_diagnostics):
    result = [
        get_most_common_bit_for_position(given_diagnostics, position)
        for position, _
        in enumerate(given_diagnostics[0])
    ]

    return tuple(result)


def get_epsilon_rate(given_diagnostics):
    def flip_bit(bit):
        if bit == 0:
            return 1
        return 0

    gamma_rate = get_gamma_rate(given_diagnostics)
    gamma_rate = list(gamma_rate)

    epsilon_rate = [flip_bit(digit) for digit in gamma_rate]

    return tuple(epsilon_rate)


def convert_rate_to_decimal(rate):
    out = 0

    for i in range(len(rate)):
        val = rate[len(rate) - (i + 1)]
        out += val * (2 ** i)

    return out


def calculate_power_consumption(given_diagnostics):
    gamma_rate = get_gamma_rate(given_diagnostics)
    epsilon_rate = get_epsilon_rate(given_diagnostics)

    return convert_rate_to_decimal(gamma_rate) * convert_rate_to_decimal(epsilon_rate)


class DiagnosticsParserTest(ReadableTestCase):
    @parameterized_test(params=[
        ('00100', (0, 0, 1, 0, 0)),
        ('11110', (1, 1, 1, 1, 0)),
        ('10110', (1, 0, 1, 1, 0)),
    ])
    def test_should_parse_diagnostics_line(self, given_line, expected_output):
        actual = parse_diagnostics_line(given_line)
        self.expect(actual).to_be(expected_output)

    @parameterized_test(params=[
        (['00100'], [(0, 0, 1, 0, 0)]),
        (['00100', '11110'], [(0, 0, 1, 0, 0), (1, 1, 1, 1, 0)]),
    ])
    def test_should_parse_complete_diagnostics(self, given_diagnostics, expected_output):
        actual = parse_diagnostics(given_diagnostics)
        self.expect(actual).to_be(expected_output)


class RateExtractionTest(ReadableTestCase):
    @parameterized_test(params=[
        ([(0,)], 0, 0),
        (['00100'], 0, 0),
        (['00100', '11110', '10110'], 0, 1),
        (['00100', '11110', '10110', '10111', '10101', '01111', '00111', '11100', '10000', '11001', '00010', '01010'],
         0, 1),
        (['00100', '11110', '10110', '10111', '10101', '01111', '00111', '11100', '10000', '11001', '00010', '01010'],
         1, 0),
    ])
    def test_should_get_most_common_bit_for_position(self, given_diagnostics, given_position, expected_bit):
        actual = get_most_common_bit_for_position(given_diagnostics, given_position)
        self.expect(actual).to_be(expected_bit)

    @parameterized_test(params=[
        ([(0,)], 0, {0: 1}),
        ([(0,), (0,)], 0, {0: 2}),
        ([(0,), (1,)], 0, {0: 1, 1: 1}),
    ])
    def test_should_get_bit_population_for_position(self, given_diagnostics, given_position, expected_population):
        actual = get_bit_population_for_position(given_diagnostics, given_position)
        self.expect(actual).to_be(expected_population)

    @parameterized_test(params=[
        (['00100'], (0, 0, 1, 0, 0)),
        (['00100', '11110', '10110'], (1, 0, 1, 1, 0)),
        (['00100', '11110', '10110', '10111', '10101', '01111', '00111', '11100', '10000', '11001', '00010', '01010'],
         (1, 0, 1, 1, 0)),
    ])
    def test_should_get_gamma_rate(self, given_diagnostics, expected_gamma_rate):
        actual = get_gamma_rate(given_diagnostics)
        self.expect(actual).to_be(expected_gamma_rate)

    @parameterized_test(params=[
        (['00100'], (1, 1, 0, 1, 1)),
        (['00100', '11110', '10110'], (0, 1, 0, 0, 1)),
        (['00100', '11110', '10110', '10111', '10101', '01111', '00111', '11100', '10000', '11001', '00010', '01010'],
         (0, 1, 0, 0, 1)),
    ])
    def test_get_epsilon_rate(self, given_diagnostics, expected_epsilon_rate):
        actual = get_epsilon_rate(given_diagnostics)
        self.expect(actual).to_be(expected_epsilon_rate)


class RateConverterTest(ReadableTestCase):
    @parameterized_test(params=[
        ((0,), 0),
        ((1, 0), 2),
        ((1, 0, 0), 4),
        ((0, 1, 0, 0, 1), 9),
        ((1, 0, 1, 1, 0), 22),
    ])
    def test_should_convert_rates_to_decimal(self, given_rate, expected_decimal_value):
        actual = convert_rate_to_decimal(given_rate)
        self.expect(actual).to_be(expected_decimal_value)


class PowerConsumptionCalculatorTest(ReadableTestCase):
    @parameterized_test(params=[
        (['0'], 0),
        (['11'], 0),
        (['10'], 2),
        (['00100', '11110', '10110', '10111', '10101', '01111', '00111', '11100', '10000', '11001', '00010', '01010'],
         198)
    ])
    def test_should_calculate_power_consumption(self, given_rate, expected_power_consumption):
        actual = calculate_power_consumption(given_rate)
        self.expect(actual).to_be(expected_power_consumption)


if __name__ == "__main__":
    print(calculate_power_consumption(input_values))
