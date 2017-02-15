import unittest

import utils

class Utils(unittest.TestCase):
    def test_get_numerical_suffix_st(self):
        number = 101
        expected = "st"

        result = utils.get_numerical_suffix(number)
        self.assertEqual(expected, result)

    def test_get_numerical_suffix_nd(self):
        number = 102
        expected = "nd"

        result = utils.get_numerical_suffix(number)
        self.assertEqual(expected, result)

    def test_get_numerical_suffix_rd(self):
        number = 103
        expected = "rd"

        result = utils.get_numerical_suffix(number)
        self.assertEqual(expected, result)

    def test_get_numerical_suffix_th(self):
        number = 104
        expected = "th"

        result = utils.get_numerical_suffix(number)
        self.assertEqual(expected, result)

    def test_get_numerical_suffix_string(self):
        number = "80"
        expected = "th"

        result = utils.get_numerical_suffix(number)
        self.assertEqual(expected, result)

