from day_05.conf import input_lines
from day_05.day_5_part_1 import Line, determine_number_of_intersections

if __name__ == "__main__":
    lines = [Line(l_str) for l_str in input_lines]
    print(determine_number_of_intersections(lines, consider_diagonal=True))
