from typing import Tuple, List

from day_04.conf import input_board_strings, input_numbers
from test_dsl import ReadableTestCase


class BingoBoard:
    def __init__(self, board_string: str):
        self.numbers = [line.replace('  ', ' ') for line in board_string.split('\n')]
        self.numbers: List[List[int]] = [[int(num) for num in number_string.split(' ') if num != ''] for number_string
                                         in self.numbers]
        self.marked = [
            [False, False, False, False, False, ],
            [False, False, False, False, False, ],
            [False, False, False, False, False, ],
            [False, False, False, False, False, ],
            [False, False, False, False, False, ],
        ]

    def _get_position_for_number(self, number) -> Tuple[int, int]:
        for row, line in enumerate(self.numbers):
            for col, value in enumerate(line):
                if value == number:
                    return row, col
        return -1, -1

    def mark_number(self, number):
        row, col = self._get_position_for_number(number)
        if row != -1:
            self.marked[row][col] = True

    def has_won(self) -> bool:
        for line in self.marked:
            if False in line:
                continue
            else:
                return True
        for index in range(len(self.marked)):
            for count, line in enumerate(self.marked):
                if not line[index]:
                    break
                if count == len(self.marked) - 1:
                    return True
        return False

    def get_unmarked_number_sum(self) -> int:
        unmarked_sum = 0

        for row, line in enumerate(self.marked):
            for col, marked in enumerate(line):
                if not marked:
                    unmarked_sum += self.numbers[row][col]
        return unmarked_sum


class BingoBoardTest(ReadableTestCase):
    def setUp(self) -> None:
        given = """22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19"""
        self.bingo_board = BingoBoard(given)

    def test_should_create_bingo_board(self):
        self.expect(self.bingo_board).to_not_be_none()

    def test_should_parse_string_correctly(self):
        self.expect(self.bingo_board.numbers).to_be([
            [22, 13, 17, 11, 0],
            [8, 2, 23, 4, 24],
            [21, 9, 14, 16, 7],
            [6, 10, 3, 18, 5],
            [1, 12, 20, 15, 19],
        ])

    def test_should_mark_number_correctly(self):
        self.bingo_board.mark_number(0)
        self.expect(self.bingo_board.marked).to_be([
            [False, False, False, False, True, ],
            [False, False, False, False, False, ],
            [False, False, False, False, False, ],
            [False, False, False, False, False, ],
            [False, False, False, False, False, ],
        ])

    def test_should_not_mark_number_correctly(self):
        self.bingo_board.mark_number(1000)
        self.expect(self.bingo_board.marked).to_be([
            [False, False, False, False, False, ],
            [False, False, False, False, False, ],
            [False, False, False, False, False, ],
            [False, False, False, False, False, ],
            [False, False, False, False, False, ],
        ])

    def test_should_have_not_won(self):
        self.expect(self.bingo_board.has_won()).to_be_false()

    def test_should_have_won(self):
        for num in [22, 13, 17, 11, 0]:
            self.bingo_board.mark_number(num)
        self.expect(self.bingo_board.has_won()).to_be_true()

    def test_should_have_won_col(self):
        for num in [22, 8, 21, 6, 1]:
            self.bingo_board.mark_number(num)
        self.expect(self.bingo_board.has_won()).to_be_true()

    def test_should_calculate_unmarked_number_sum(self):
        given = """14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""
        board = BingoBoard(given)
        for num in [7, 4, 9, 5, 11, 17, 23, 2, 0, 14, 21, 24]:
            board.mark_number(num)
        self.expect(board.has_won()).to_be_true()
        self.expect(board.get_unmarked_number_sum()).to_be(188)


if __name__ == "__main__":
    boards = [BingoBoard(board_string) for board_string in input_board_strings]
    for number in input_numbers:
        for board in boards:
            board.mark_number(number)
            if board.has_won():
                print(f'{board.get_unmarked_number_sum()} * {number}')
