from day_13.conf import input_dots, input_instructions
from day_13.day_13_part_1 import Paper, multiple_folds

if __name__ == "__main__":
    result = multiple_folds(Paper(input_dots), input_instructions)
    print(result.__str__())
