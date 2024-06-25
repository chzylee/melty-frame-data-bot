import unittest
from data import inputreader as InputReader

class TestInputReader(unittest.TestCase):
    def test_format_move_input_given_ground_normal_returns_correctly_formatted_name(self):
        message = InputReader.format_move_input("3C")
        # Hardcoding message based on above data to check to avoid forcing logic into test.
        self.assertEqual(message, "3C")

    def test_format_move_input_given_ground_special_returns_correctly_formatted_name(self):
        message = InputReader.format_move_input("623b")
        # Hardcoding message based on above data to check to avoid forcing logic into test.
        self.assertEqual(message, "623B")

    def test_format_move_input_given_air_move_returns_correctly_formatted_name(self):
        message = InputReader.format_move_input("j.236C")
        # Hardcoding message based on above data to check to avoid forcing logic into test.
        self.assertEqual(message, "j.236C")

    def test_format_move_input_given_shorthand_air_normal_returns_correctly_formatted_name(self):
        message = InputReader.format_move_input("jB")
        self.assertEqual(message, "j.B")

    def test_format_move_input_given_nonstandard_capitalization_returns_correctly_formatted_name(self):
        message = InputReader.format_move_input("JA")
        self.assertEqual(message, "j.A")

if __name__ == '__main__':
    unittest.main()
