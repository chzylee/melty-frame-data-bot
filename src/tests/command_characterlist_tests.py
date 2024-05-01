import unittest
from commands import characterlist

class TestCharacterList(unittest.TestCase):
    def test_get_allowed_names_returns_list_of_character_names_as_text(self):
        char_list = characterlist.get_allowed_names()
        self.assertIsInstance(char_list, str)
        self.assertGreater(len(char_list), 0)
        self.assertIn(",", char_list)

if __name__ == '__main__':
    unittest.main()
