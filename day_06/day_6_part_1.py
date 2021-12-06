from day_06.conf import input_population
from unittest import skip
from test_dsl import ReadableTestCase, parameterized_test


def calculate_new_state(given_population):
    original_population = [6 if fish == 0 else fish - 1 for fish in given_population]
    new_population = [8 for _ in range(given_population.count(0))]

    return original_population + new_population


def calculate_for_days(given_population, days):
    for _ in range(days):
        given_population = calculate_new_state(given_population)
    return given_population


def calculate_new_state_efficient(given_population):
    out = {}

    for age, count in given_population:
        if age == 0:
            if 6 in out:
                out[6] = out[6] + count
            else:
                out[6] = count
            if 8 in out:
                out[8] = out[8] + count
            else:
                out[8] = count
        else:
            if age - 1 in out:
                out[age - 1] = out[age - 1] + count
            else:
                out[age - 1] = count

    return [(age, out[age]) for age in out]


def calculate_for_days_efficient(given_population, days):
    given_population = [(i, given_population.count(i)) for i in range(9)]

    for _ in range(days):
        given_population = calculate_new_state_efficient(given_population)

    out = 0
    for _, count in given_population:
        out += count

    return out


class LanternFishTest(ReadableTestCase):
    @parameterized_test(params=[
        ([3, 4, 3, 1, 2], [2, 3, 2, 0, 1]),
        ([5, 6, 5, 3, 4, 5, 6, 7, 7, 8], [4, 5, 4, 2, 3, 4, 5, 6, 6, 7]),
    ])
    def test_day_tick(self, given_population, expected_population):
        actual = calculate_new_state(given_population)
        self.expect(actual).to_be(expected_population)

    @parameterized_test(params=[
        ([2, 3, 2, 0, 1], [1, 2, 1, 6, 0, 8]),
        ([2, 3, 2, 0, 1, 2, 3, 4, 4, 5], [1, 2, 1, 6, 0, 1, 2, 3, 3, 4, 8]),
        ([0, 1, 0, 5, 6, 0, 1, 2, 2, 3, 7, 8], [6, 0, 6, 4, 5, 6, 0, 1, 1, 2, 6, 7, 8, 8, 8]),
    ])
    def test_population_increase(self, given_population, expected_population):
        actual = calculate_new_state(given_population)
        self.expect(actual).to_be(expected_population)

    @parameterized_test(params=[
        ([3, 4, 3, 1, 2], 18, [6, 0, 6, 4, 5, 6, 0, 1, 1, 2, 6, 0, 1, 1, 1, 2, 2, 3, 3, 4, 6, 7, 8, 8, 8, 8]),
        ([5, 6, 5, 3, 4, 5, 6, 7, 7, 8], 2, [3, 4, 3, 1, 2, 3, 4, 5, 5, 6]),
    ])
    def test_should_calculate_multiple_days(self, given_population, days, expected_population):
        actual = calculate_for_days(given_population, days)
        self.expect(actual).to_be(expected_population)

    def test_should_calculate_80_days(self):
        actual = calculate_for_days_efficient([3, 4, 3, 1, 2], 80)
        self.expect(actual).to_be(5934)

    def test_should_calculate_256_days(self):
        actual = calculate_for_days_efficient([3, 4, 3, 1, 2], 256)
        self.expect(actual).to_be(26984457539)


if __name__ == "__main__":
    print(calculate_for_days_efficient(input_population, 256))
