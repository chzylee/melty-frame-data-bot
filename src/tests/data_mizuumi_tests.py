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
        char = "warakkia" # Misspelled.
        moon = "C"
        with self.assertRaises(UserInputException):
            mizuumi.get_character_url(char, moon)

    # Only testing case of valid param as data validation via discord action spec
    # allows us to guarantee input is valid.
    def test_get_moon_path_given_moon_value_returns_moon_path(self):
        moon = mizuumi.get_moon_path("C")
        self.assertEqual(moon, "Crescent_Moon")

    # Also only testing positive case as data should be validated ahead of time.
    # Both get char/moon are simple accesses. These essentially test if mapping exists.
    def test_get_char_path_given_valid_char_returns_path(self):
        char_path = mizuumi.get_char_path("Aoko")
        self.assertEqual(char_path, "Aoko_Aozaki")

if __name__ == '__main__':
    unittest.main()
