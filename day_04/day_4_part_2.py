from day_04.conf import input_board_strings, input_numbers
from day_04.day_4_part_1 import BingoBoard
from test_dsl import ReadableTestCase, parameterized_test


if __name__ == "__main__":
    boards = [BingoBoard(board_string) for board_string in input_board_strings]

    for number in input_numbers:
        for board in boards:
            board.mark_number(number)
        if len(boards) != 1:
            boards = [board for board in boards if not board.has_won()]
        if len(boards) == 1 and boards[0].has_won():
            print(f'{boards[0].get_unmarked_number_sum()} * {number}')
