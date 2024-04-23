import unittest
from discord import Embed
from commands import framedata
from commands.data.types import MeltyMove

class TestFrameData(unittest.TestCase):
    def test_get_char_and_move_given_valid_event_data_returns_correct_MeltyMove(self):
        character = "Len"
        move_input = "3C"
        data = {
            "options": [
                # Name is first option, move is second.
                { "value": character },
                { "value": move_input }
            ]
        }
        char_move = framedata.get_char_and_move(data)
        self.assertIsNotNone(char_move)
        self.assertIsInstance(char_move, MeltyMove)
        self.assertEqual(char_move.char, character)
        self.assertEqual(char_move.input, move_input)

    def test_get_frame_data_returns_embed_with_data_for_move(self):
        melty_move = MeltyMove(char="Len", input="3C")
        response = framedata.get_frame_data(melty_move)
        self.assertIsNotNone(response)
        self.assertTrue(isinstance(response, Embed))
        self.assertIn(melty_move.char, response.title)
        self.assertIn(melty_move.input, response.title)


if __name__ == '__main__':
    unittest.main()
