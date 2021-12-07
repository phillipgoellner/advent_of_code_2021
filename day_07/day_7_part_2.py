from functools import reduce

from day_07.conf import input_positions
from test_dsl import ReadableTestCase, parameterized_test


def calculate_fuel_consumption(given_positions, given_alignment_position):
    def calculate_consumption_for_distance(actual_position):
        delta = abs(actual_position - given_alignment_position)
        return int(delta * ((delta + 1) / 2))

    positions_deltas = list(map(calculate_consumption_for_distance, given_positions))
    return reduce(lambda x, y: x + y, positions_deltas, 0)


def calculate_ideal_alignment_position(given_positions):
    upper_limit = max(given_positions)
    result = -1
    found_position = -1

    for position in range(upper_limit + 1):
        consumption = calculate_fuel_consumption(given_positions, position)
        if result == -1 or result > consumption:
            result = consumption
            found_position = position

    return found_position


class FuelConsumptionTest(ReadableTestCase):
    @parameterized_test(params=[
        ([16, 1, 2, 0, 4, 2, 7, 1, 2, 14], 2, 206),
        ([16, 1, 2, 0, 4, 2, 7, 1, 2, 14], 5, 168),
    ])
    def test_should_calculate_fuel_consumption(self, given_positions, given_alignment_position, expected_consumption):
        actual = calculate_fuel_consumption(given_positions, given_alignment_position)
        self.expect(actual).to_be(expected_consumption)

    def test_should_align_at_lowest_consumption(self):
        actual = calculate_ideal_alignment_position([16, 1, 2, 0, 4, 2, 7, 1, 2, 14])
        self.expect(actual).to_be(5)


if __name__ == "__main__":
    positions = input_positions
    best_pos = calculate_ideal_alignment_position(positions)
    print(calculate_fuel_consumption(positions, best_pos))
