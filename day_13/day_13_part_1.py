from typing import List, Tuple

from day_13.conf import input_dots, input_instructions
from test_dsl import ReadableTestCase


class Paper:
    def __init__(self, dot_lines: List[str], dots: List[List[bool]] = None):
        if dots is None:
            self.dots = [tuple(dot.split(',')) for dot in dot_lines]
            self.dots = [(int(x), int(y)) for x, y in self.dots]
            width = 0
            height = 0

            for x, y in self.dots:
                if x > width:
                    width = x
                if y > height:
                    height = y

            width += 1
            height += 1

            self.dots = [
                [
                    (col, row) in self.dots for col in range(width)
                ] for row in range(height)
            ]
        else:
            self.dots = dots

    def get_x_sub_papers(self, separation_line: int):
        left, right = [], []
        for row, line in enumerate(self.dots):
            left.append([])
            right.append([])

            for index, value in enumerate(line):
                if index < separation_line:
                    left[row].append(value)
                if index > separation_line:
                    right[row].append(value)

        left, right = Paper([], dots=left), Paper([], dots=right)

        return left, right

    def get_y_sub_papers(self, separation_line: int):
        top, bottom = self.dots[:separation_line], self.dots[separation_line + 1:]

        top, bottom = Paper([], dots=top), Paper([], dots=bottom)
        return top, bottom

    def flip_x(self):
        dots = [line[::-1] for line in self.dots]
        return Paper([], dots=dots)

    def flip_y(self):
        dots = self.dots[::-1]
        return Paper([], dots=dots)

    def __str__(self) -> str:
        out = ''

        for row in self.dots:
            for is_dot in row:
                out += '#' if is_dot else '.'
            out += '\n'

        return out[:-1]


def fold_paper(paper_to_fold: Paper, fold_line: int, fold_x: bool = True):
    if fold_x:
        left, right = paper_to_fold.get_x_sub_papers(fold_line)
        page_one, page_two = left.flip_x(), right
    else:
        top, bottom = paper_to_fold.get_y_sub_papers(fold_line)
        page_one, page_two = bottom.flip_y(), top

    new_dots = []

    for row, line in enumerate(page_one.dots):
        new_dots.append([])
        for col, value in enumerate(line):
            new_dots[row].append(value or page_two.dots[row][col])

    return Paper([], dots=new_dots)


def multiple_folds(starting_paper: Paper, folding_instructions: List[Tuple[str, int]]):
    for direction, folding_line in folding_instructions:
        starting_paper = fold_paper(starting_paper, folding_line, direction == 'x')

    return starting_paper


class TestPaper(ReadableTestCase):
    def setUp(self) -> None:
        given = ['6,10', '0,14', '9,10', '0,3', '10,4', '4,11', '6,0', '6,12', '4,1', '0,13', '10,12', '3,4', '3,0',
                 '8,4', '1,10', '2,14', '8,10', '9,0']
        self.paper = Paper(given)

    def test_string_representation(self):
        expected = """...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
...........
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........"""

        actual = self.paper.__str__()
        self.expect(actual).to_be(expected)

    def test_x_sub_pages(self):
        actual_left, actual_right = self.paper.get_x_sub_papers(5)
        expected = ("""...#.
....#
.....
#....
...#.
.....
.....
.....
.....
.....
.#...
....#
.....
#....
#.#..""", """#..#.
.....
.....
.....
..#.#
.....
.....
.....
.....
.....
#.##.
.....
#...#
.....
.....""")

        self.expect((actual_left.__str__(), actual_right.__str__())).to_be(expected)

    def test_y_sub_pages(self):
        actual_top, actual_bottom = self.paper.get_y_sub_papers(7)
        expected = ("""...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........""", """...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........""")

        self.expect((actual_top.__str__(), actual_bottom.__str__())).to_be(expected)

    def test_flip_x(self):
        actual = Paper(['0,0', '2, 2']).flip_x()
        self.expect(actual.__str__()).to_be("""..#
...
#..""")

    def test_flip_y(self):
        actual = Paper(['0,1', '2, 2']).flip_y()
        self.expect(actual.__str__()).to_be("""..#
#..
...""")

    def test_fold_paper_x(self):
        actual = fold_paper(Paper([], dots=[[True, False, True, True, False, False, True, False, False, True, False],
                                            [True, False, False, False, True, False, False, False, False, False, False],
                                            [False, False, False, False, False, False, True, False, False, False, True],
                                            [True, False, False, False, True, False, False, False, False, False, False],
                                            [False, True, False, True, False, False, True, False, True, True, True],
                                            [False, False, False, False, False, False, False, False, False, False,
                                             False],
                                            [False, False, False, False, False, False, False, False, False, False,
                                             False]]), 5)
        expected = """#####
#...#
#...#
#...#
#####
.....
....."""

        self.expect(actual.__str__()).to_be(expected)

    def test_fold_paper_y(self):
        actual = fold_paper(self.paper, 7, fold_x=False)
        expected = """#.##..#..#.
#...#......
......#...#
#...#......
.#.#..#.###
...........
..........."""

        self.expect(actual.__str__()).to_be(expected)

    def test_multiple_folds(self):
        actual = multiple_folds(self.paper, [('y', 7), ('x', 5)])
        expected = """#####
#...#
#...#
#...#
#####
.....
....."""

        self.expect(actual.__str__()).to_be(expected)


if __name__ == "__main__":
    result = fold_paper(Paper(input_dots), 655)
    print(result.__str__())
