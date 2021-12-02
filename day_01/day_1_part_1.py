from day_01.conf import input_values
from test_dsl import parameterized_test, ReadableTestCase


class DepthIncreaseDetection(ReadableTestCase):
    @parameterized_test(params=[
        (0, 1, True),
        (0, 0, False),
        (1, 0, False),
    ])
    def test_should_determine_increase_correctly(self, first_value, second_value, expected):
        actual = is_depth_increase(first_value, second_value)
        self.expect(actual).to_be(expected)


class DepthIncreaseCounter(ReadableTestCase):
    @parameterized_test(params=[
        ([], 0),
        ([0, 1], 1),
        ([3, 2, 3], 1),
        ([199, 200, 208, 210, 200, 207, 240, 269, 260, 263], 7),
        ([607, 618, 618, 617, 647, 716, 769, 792], 5),
    ])
    def test_should_count_increases_correctly(self, depth_list, count):
        actual = count_depth_increases(depth_list)
        self.expect(actual).to_be(count)


def is_depth_increase(current_depth, next_depth):
    return current_depth < next_depth


def count_depth_increases(depths_list):
    counter = 0

    for index, depth in enumerate(depths_list):
        if index == 0:
            continue
        if is_depth_increase(depths_list[index - 1], depth):
            counter += 1

    return counter


if __name__ == "__main__":
    print(count_depth_increases(input_values))
