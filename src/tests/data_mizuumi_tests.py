import unittest
from data import mizuumi
from models.errors import UserInputException

class TestMizuumi(unittest.TestCase):
    def test_get_character_url_given_valid_data_returns_url(self):
        char = "Len"
        moon = "C"
        url = mizuumi.get_character_url(char, moon)
        # Values used in Mizuumi routes.
        self.assertIn("Len", url)
        self.assertIn("Crescent_Moon", url)

    def test_get_character_url_given_invalid_char_name_throws_error(self):
        char = "warakia" # Misspelled.
        moon = "C"
        with self.assertRaises(UserInputException):
            mizuumi.get_character_url(char, moon)

if __name__ == '__main__':
    unittest.main()
