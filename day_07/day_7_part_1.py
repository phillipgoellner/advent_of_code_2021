from day_07.conf import input_positions
from test_dsl import ReadableTestCase, parameterized_test
from functools import reduce


def calculate_fuel_consumption(given_positions, given_alignment_position):
    positions_deltas = list(map(lambda x: abs(x - given_alignment_position), given_positions))
    return reduce(lambda x, y: x + y, positions_deltas, 0)


def calculate_ideal_alignment_position(given_positions):
    upper_limit = max(given_positions)
    result = upper_limit * len(given_positions)
    found_position = -1

    for position in range(upper_limit + 1):
        consumption = calculate_fuel_consumption(given_positions, position)
        if result > consumption:
            result = consumption
            found_position = position

    return found_position


class FuelConsumptionTest(ReadableTestCase):
    @parameterized_test(params=[
        ([1, 2], 1, 1),
        ([16, 1, 2, 0, 4, 2, 7, 1, 2, 14], 1, 41),
        ([16, 1, 2, 0, 4, 2, 7, 1, 2, 14], 2, 37),
        ([16, 1, 2, 0, 4, 2, 7, 1, 2, 14], 10, 71),
    ])
    def test_should_calculate_fuel_consumption(self, given_positions, given_alignment_position, expected_consumption):
        actual = calculate_fuel_consumption(given_positions, given_alignment_position)
        self.expect(actual).to_be(expected_consumption)

    def test_should_align_at_lowest_consumption(self):
        actual = calculate_ideal_alignment_position([16, 1, 2, 0, 4, 2, 7, 1, 2, 14])
        self.expect(actual).to_be(2)


if __name__ == "__main__":
    positions = input_positions
    best_pos = calculate_ideal_alignment_position(positions)
    print(calculate_fuel_consumption(positions, best_pos))
