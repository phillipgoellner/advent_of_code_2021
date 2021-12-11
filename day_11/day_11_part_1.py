from day_11.conf import input_energy_levels
from test_dsl import ReadableTestCase


def get_total_flashes(octopuses, steps):
    flashes = 0
    for _ in range(steps):
        octopuses, new_flashes = one_step(octopuses)
        flashes += new_flashes
    return flashes


def get_neighbouring_positions(x, y):
    out = []

    if 0 < x < 9:
        out.append((x + 1, y))
        out.append((x - 1, y))
        if 0 < y < 9:
            out.append((x, y + 1))
            out.append((x, y - 1))
            out.append((x + 1, y + 1))
            out.append((x - 1, y - 1))
            out.append((x + 1, y - 1))
            out.append((x - 1, y + 1))
        elif y == 0:
            out.append((x, y + 1))
            out.append((x + 1, y + 1))
            out.append((x - 1, y + 1))
        else:
            out.append((x, y - 1))
            out.append((x - 1, y - 1))
            out.append((x + 1, y - 1))
    elif x == 0:
        out.append((x + 1, y))
        if 0 < y < 9:
            out.append((x, y + 1))
            out.append((x, y - 1))
            out.append((x + 1, y + 1))
            out.append((x + 1, y - 1))
        elif y == 0:
            out.append((x, y + 1))
            out.append((x + 1, y + 1))
        else:
            out.append((x, y - 1))
            out.append((x + 1, y - 1))
    else:
        out.append((x - 1, y))
        if 0 < y < 9:
            out.append((x, y + 1))
            out.append((x, y - 1))
            out.append((x - 1, y - 1))
            out.append((x - 1, y + 1))
        elif y == 0:
            out.append((x, y + 1))
            out.append((x - 1, y + 1))
        else:
            out.append((x, y - 1))
            out.append((x - 1, y - 1))

    return out


def one_step(octopuses):
    number_of_flashes = 0
    octopuses = [[level + 1 for level in line] for line in octopuses]
    has_flashed = [[False for _ in line] for line in octopuses]
    should_run_again = True

    while should_run_again:
        should_run_again = False
        for row, line in enumerate(octopuses):
            for col, energy_level in enumerate(line):
                if energy_level > 9 and not has_flashed[row][col]:
                    should_run_again = True
                    has_flashed[row][col] = True
                    for x, y in get_neighbouring_positions(row, col):
                        octopuses[x][y] += 1

    for row, line in enumerate(has_flashed):
        for col, octopus_has_flashed in enumerate(line):
            if octopus_has_flashed:
                number_of_flashes += 1
                octopuses[row][col] = 0

    return octopuses, number_of_flashes


class FlashSimulationTest(ReadableTestCase):
    def test_total_flash_count(self):
        given = [[5, 4, 8, 3, 1, 4, 3, 2, 2, 3],
                 [2, 7, 4, 5, 8, 5, 4, 7, 1, 1],
                 [5, 2, 6, 4, 5, 5, 6, 1, 7, 3],
                 [6, 1, 4, 1, 3, 3, 6, 1, 4, 6],
                 [6, 3, 5, 7, 3, 8, 5, 4, 7, 8],
                 [4, 1, 6, 7, 5, 2, 4, 6, 4, 5],
                 [2, 1, 7, 6, 8, 4, 1, 7, 2, 1],
                 [6, 8, 8, 2, 8, 8, 1, 1, 3, 4],
                 [4, 8, 4, 6, 8, 4, 8, 5, 5, 4],
                 [5, 2, 8, 3, 7, 5, 1, 5, 2, 6]]

        actual = get_total_flashes(given, 10)
        self.expect(actual).to_be(204)

    def test_total_flash_count_100(self):
        given = [[5, 4, 8, 3, 1, 4, 3, 2, 2, 3],
                 [2, 7, 4, 5, 8, 5, 4, 7, 1, 1],
                 [5, 2, 6, 4, 5, 5, 6, 1, 7, 3],
                 [6, 1, 4, 1, 3, 3, 6, 1, 4, 6],
                 [6, 3, 5, 7, 3, 8, 5, 4, 7, 8],
                 [4, 1, 6, 7, 5, 2, 4, 6, 4, 5],
                 [2, 1, 7, 6, 8, 4, 1, 7, 2, 1],
                 [6, 8, 8, 2, 8, 8, 1, 1, 3, 4],
                 [4, 8, 4, 6, 8, 4, 8, 5, 5, 4],
                 [5, 2, 8, 3, 7, 5, 1, 5, 2, 6]]

        actual = get_total_flashes(given, 100)
        self.expect(actual).to_be(1656)

    def test_one_step(self):
        given = [[3, 4, 5, 4, 3],
                 [4, 0, 0, 0, 4],
                 [5, 0, 0, 0, 5],
                 [4, 0, 0, 0, 4],
                 [3, 4, 5, 4, 3]]

        expected_octopuses = [[4, 5, 6, 5, 4],
                              [5, 1, 1, 1, 5],
                              [6, 1, 1, 1, 6],
                              [5, 1, 1, 1, 5],
                              [4, 5, 6, 5, 4]]

        expected_number_of_flashes = 0

        actual = one_step(given)
        self.expect(actual).to_be((expected_octopuses, expected_number_of_flashes))

    def test_one_step_with_flashes(self):
        given = [[1, 1, 1, 1, 1],
                 [1, 9, 9, 9, 1],
                 [1, 9, 1, 9, 1],
                 [1, 9, 9, 9, 1],
                 [1, 1, 1, 1, 1]]

        expected_octopuses = [[3, 4, 5, 4, 3],
                              [4, 0, 0, 0, 4],
                              [5, 0, 0, 0, 5],
                              [4, 0, 0, 0, 4],
                              [3, 4, 5, 4, 3]]

        expected_number_of_flashes = 9

        actual = one_step(given)
        self.expect(actual).to_be((expected_octopuses, expected_number_of_flashes))


if __name__ == "__main__":
    print(get_total_flashes(input_energy_levels, 100))
