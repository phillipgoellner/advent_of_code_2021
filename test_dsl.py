import unittest


class ReadableTestCase(unittest.TestCase):
    class Asserter(unittest.TestCase):
        def __init__(self, actual_value):
            super().__init__()
            self._actual_value = actual_value

        def to_be(self, expected_value):
            self.assertEqual(expected_value, self._actual_value)

        def to_not_be(self, expected_value):
            self.assertNotEqual(expected_value, self._actual_value)

        def to_be_of_type(self, expected_type):
            self.assertIsInstance(self._actual_value, expected_type)

        def to_equal_list(self, expected_list):
            self.assertListEqual(expected_list, self._actual_value)

        def to_be_true(self):
            self.assertTrue(self._actual_value)

        def to_be_false(self):
            self.assertFalse(self._actual_value)

        def to_be_none(self):
            self.assertIsNone(self._actual_value)

        def to_not_be_none(self):
            self.assertIsNotNone(self._actual_value)

        def to_be_a_list(self):
            self.to_be_of_type(list)

        def to_be_a_dict(self):
            self.to_be_of_type(dict)

        def to_be_a_set(self):
            self.to_be_of_type(set)

    def expect(self, actual_value):
        return self.Asserter(actual_value)


def parameterized_test(params):
    def decorator_function(function):
        def parameter_handler(self):
            for param in params:
                if isinstance(param, tuple):
                    test_params = [_p for _p in param]
                else:
                    test_params = [param]

                with self.subTest(i=test_params[0]):
                    function(self, *test_params)
        return parameter_handler

    return decorator_function
