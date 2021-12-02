from typing import List

from day_01.day_1_part_1 import count_depth_increases, input_values
from test_dsl import ReadableTestCase, parameterized_test


def sum_sliding_windows(depth_list: List[int]):
    def reduce(d_list):
        total_sum = 0

        for depth in d_list:
            total_sum += depth

        return total_sum

    sub_lists = [depth_list[i:i + 3] for i, _ in enumerate(depth_list) if len(depth_list[i:i + 3]) == 3]

    return [reduce(_sub_list) for _sub_list in sub_lists]


class SlidingWindowSum(ReadableTestCase):
    @parameterized_test(params=[
        ([1, 2, 3], [6]),
        ([2, 3, 4], [9]),
        ([1, 2, 3, 4], [6, 9]),
        ([199, 200, 208, 210, 200, 207, 240, 269, 260, 263], [607, 618, 618, 617, 647, 716, 769, 792]),
    ])
    def test_should_sum_sliding_windows_correctly(self, depth_list, expected_windows_sum):
        actual = sum_sliding_windows(depth_list)
        self.expect(actual).to_be(expected_windows_sum)


if __name__ == "__main__":
    print(count_depth_increases(sum_sliding_windows(input_values)))
