from day_05.conf import input_lines
from test_dsl import ReadableTestCase, parameterized_test


class Line:
    def __init__(self, line_string: str):
        l_strings = line_string.split(' -> ')
        self.start_point = Point(point_string=l_strings[0])
        self.end_point = Point(point_string=l_strings[1])

    def is_v_or_h(self):
        return self.start_point.x == self.end_point.x or self.start_point.y == self.end_point.y

    def is_diagonal(self):
        d_x = self.end_point.x - self.start_point.x
        d_y = self.end_point.y - self.start_point.y
        return abs(d_x) == abs(d_y)

    def get_points(self):
        out = []
        d_x = self.end_point.x - self.start_point.x
        d_y = self.end_point.y - self.start_point.y

        step_x = 1 if d_x == 0 else int((d_x / abs(d_x)))
        step_y = 1 if d_y == 0 else int((d_y / abs(d_y)))

        if self.is_diagonal():
            for _x, _y in zip(range(self.start_point.x, self.end_point.x + step_x, step_x),
                              range(self.start_point.y, self.end_point.y + step_y, step_y)):
                out.append(Point(x=_x, y=_y))
        else:
            for _x in range(self.start_point.x, self.end_point.x + step_x, step_x):
                for _y in range(self.start_point.y, self.end_point.y + step_y, step_y):
                    out.append(Point(x=_x, y=_y))

        return out


class Point:
    def __init__(self, point_string: str = '', x=-1, y=-1):
        if point_string != '':
            p_strings = point_string.split(',')
            self.x = int(p_strings[0])
            self.y = int(p_strings[1])
        else:
            self.x = x
            self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(hash(self.x) + hash(self.y))

    def __str__(self):
        return f'({self.x},{self.y})'


def determine_number_of_intersections(given_lines, consider_diagonal=False):
    all_points = []
    point_counter = {}

    for line in given_lines:
        if line.is_v_or_h() or (consider_diagonal and line.is_diagonal()):
            line_points = line.get_points()
            for point in line_points:
                all_points.append(point)

    for point in all_points:
        if point in point_counter:
            point_counter[point] = point_counter[point] + 1
        else:
            point_counter[point] = 1

    return len([point for point in point_counter if point_counter[point] > 1])


class LineTest(ReadableTestCase):
    @parameterized_test(params=[
        (Line('2,2 -> 2,1'), True),
        (Line('0,9 -> 2,9'), True),
        (Line('0,8 -> 2,9'), False),
    ])
    def test_lines_should_detect_v_h(self, given_line, expected):
        actual = given_line.is_v_or_h()
        self.expect(actual).to_be(expected)

    @parameterized_test(params=[
        (Line('2,2 -> 4,4'), True),
        (Line('0,9 -> 2,9'), False),
        (Line('9,7 -> 7,9'), True),
        (Line('5,5 -> 8,2'), True),
    ])
    def test_lines_should_detect_diagonal(self, given_line, expected):
        actual = given_line.is_diagonal()
        self.expect(actual).to_be(expected)

    @parameterized_test(params=[
        (Point(x=0, y=0), Point(x=0, y=0), True),
        (Point(x=0, y=0), Point(x=0, y=1), False),
    ])
    def test_should_compare_points(self, given_point_1, given_point_2, expected_result):
        actual = given_point_1 == given_point_2
        self.expect(actual).to_be(expected_result)

    @parameterized_test(params=[
        (Line('0,0 -> 0,2'), [Point(x=0, y=0), Point(x=0, y=1), Point(x=0, y=2)]),
        (Line('0,4 -> 0,1'), [Point(x=0, y=4), Point(x=0, y=3), Point(x=0, y=2), Point(x=0, y=1)]),
        (Line('0,0 -> 2,2'), [Point(x=0, y=0), Point(x=1, y=1), Point(x=2, y=2)]),
        (Line('2,2 -> 0,0'), [Point(x=2, y=2), Point(x=1, y=1), Point(x=0, y=0)]),
        (Line('9,7 -> 7,9'), [Point(x=9, y=7), Point(x=8, y=8), Point(x=7, y=9)]),
    ])
    def test_should_return_points(self, given_line, expected_points):
        actual = given_line.get_points()
        self.expect(actual).to_be(expected_points)

    @parameterized_test(params=[
        ([Line('0,0 -> 0,2'), Line('0,0 -> 2,0')], 1),
        ([Line('0,0 -> 2,2'), Line('2,2 -> 0,0')], 3),
        ([Line('0,0 -> 2,0'), Line('2,0 -> 0,2'), Line('0,0 -> 0,2')], 3),
        ([Line('0,0 -> 2,0'), Line('2,0 -> 0,2'), Line('0,0 -> 0,2'), Line('0,0 -> 2,2')], 4),
        ([Line('0,9 -> 5,9'), Line('8,0 -> 0,8'), Line('9,4 -> 3,4'), Line('2,2 -> 2,1'), Line('7,0 -> 7,4'),
          Line('6,4 -> 2,0'), Line('0,9 -> 2,9'), Line('3,4 -> 1,4'), Line('0,0 -> 8,8'), Line('5,5 -> 8,2')], 12),
    ])
    def test_should_determine_intersections(self, given_lines, expected_number_of_intersections):
        actual = determine_number_of_intersections(given_lines)
        self.expect(actual).to_be(expected_number_of_intersections)


if __name__ == "__main__":
    lines = [Line(l_str) for l_str in input_lines]
    print(determine_number_of_intersections(lines))
