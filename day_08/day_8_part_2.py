from functools import reduce
from typing import Dict

from day_08.conf import input_lines_seven_digits
from day_08.day_8_part_1 import parse_input_line
from test_dsl import ReadableTestCase

digits = {
    'abcefg': '0',
    'cf': '1',
    'acdeg': '2',
    'acdfg': '3',
    'bcdf': '4',
    'abdfg': '5',
    'abdefg': '6',
    'acf': '7',
    'abcdefg': '8',
    'abcdfg': '9',
}

"""
 aaaa 
b    c
b    c
 dddd
e    f
e    f
 gggg 
"""


def get_mappings(number_string: str) -> Dict[str, str]:
    def delta_letters(longer: str, subtract: str):
        cache = longer
        for char in subtract:
            cache = cache.replace(char, '')
        return cache

    input_sequence = parse_input_line(number_string)[0]

    one = [num for num in input_sequence if len(num) == 2][0]
    four = [num for num in input_sequence if len(num) == 4][0]
    seven = [num for num in input_sequence if len(num) == 3][0]
    eight = [num for num in input_sequence if len(num) == 7][0]

    six_segments = [num for num in input_sequence if len(num) == 6]
    six_segments_remainders = [delta_letters(eight, current) for current in six_segments]

    e_segment = [delta_letters(current, four) for current in six_segments_remainders if delta_letters(current, four) != ''][0]
    one_nine = one + e_segment
    d_segment = [delta_letters(current, one_nine) for current in six_segments_remainders if delta_letters(current, one_nine) != ''][0]

    a_segment = delta_letters(seven, one)
    b_segment = delta_letters(delta_letters(four, one), d_segment)
    g_segment = delta_letters(eight, a_segment + b_segment + e_segment + four)
    c_segment = \
    [delta_letters(current, d_segment + e_segment) for current in six_segments_remainders if delta_letters(current, d_segment + e_segment) != ''][0]
    f_segment = delta_letters(one, c_segment)

    return {
        a_segment: 'a',
        b_segment: 'b',
        c_segment: 'c',
        d_segment: 'd',
        e_segment: 'e',
        f_segment: 'f',
        g_segment: 'g',
    }


def transform_number_string(num_str):
    mappings = get_mappings(num_str)
    input_sequence = ' '.join(parse_input_line(num_str)[1])
    output_sequence = ''

    for char in input_sequence:
        if char == ' ':
            output_sequence += ' '
        else:
            output_sequence += mappings[char]

    return output_sequence


def get_number_for_sequence(sequence):
    transformed_sequence = transform_number_string(sequence).split(' ')
    output_number = ''

    for number_string in transformed_sequence:
        number_string = ''.join(sorted(number_string))
        output_number += digits[number_string]

    return int(output_number)


def get_number_string_sum(sequences):
    sequences = sequences.split('\n')
    sequences = [get_number_for_sequence(seq) for seq in sequences]

    return reduce(lambda x, y: x + y, sequences, 0)


class MappingTest(ReadableTestCase):
    def test_get_mappings(self):
        given_number_string = 'acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf'
        expected_mapping = {
            'd': 'a',
            'e': 'b',
            'a': 'c',
            'f': 'd',
            'g': 'e',
            'b': 'f',
            'c': 'g',
        }

        actual = get_mappings(given_number_string)
        self.expect(actual).to_be(expected_mapping)

    def test_number_string_transformation(self):
        given_number_string = 'acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf'
        expected_transformed_string = 'gadbf dgcaf gadbf gafcd'
        actual = transform_number_string(given_number_string)

        self.expect(actual).to_be(expected_transformed_string)

    def test_get_number_for_sequence(self):
        given_number_string = 'acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf'
        expected_number = 5353
        actual = get_number_for_sequence(given_number_string)

        self.expect(actual).to_be(expected_number)

    def test_get_number_string_sum(self):
        given_number_string = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""
        expected_number = 61229
        actual = get_number_string_sum(given_number_string)

        self.expect(actual).to_be(expected_number)


if __name__ == "__main__":
    print(get_number_string_sum(input_lines_seven_digits))
