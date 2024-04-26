import unittest
from typing import List
from discord import Embed
from commands.framedata import FrameData

class TestFrameData(unittest.TestCase):
    def test_initialization_given_valid_event_data_sets_properties_correctly(self):
        moon = "C"
        character = "Len"
        move_input = "3C"
        data = {
            "options": [
                # Input order is moon, char name, move input
                { "value": moon },
                { "value": character },
                { "value": move_input }
            ]
        }
        framedata = FrameData(data)
        self.assertIsNotNone(framedata.moon)
        self.assertIsNotNone(framedata.char_name)
        self.assertIsNotNone(framedata.move_input)
        self.assertEqual(framedata.moon, moon)
        self.assertEqual(framedata.char_name, character)
        self.assertEqual(str(framedata.move_input), move_input)
        self.assertEqual(framedata.move_input.directions, "3")
        self.assertEqual(framedata.move_input.button, "C")

    def test_get_frame_data_successfully_gets_move_data_returns_fully_populated_embed(self):
        moon = "C"
        character = "Len"
        move_input = "3C"
        data = {
            "options": [
                # Input order is moon, char name, move input
                { "value": moon },
                { "value": character },
                { "value": move_input }
            ]
        }
        framedata = FrameData(data)

        embeds = framedata.get_frame_data()
        self.assertIsInstance(embeds, List)
        self.assertEqual(len(embeds), 1)
        embed = embeds[0]

        self.assertEqual(embed.title, "C-Len 3C") # Standard name format for moves
        self.assertGreater(len(embed.url), 0)
        self.assertIsNotNone(embed.image)

        # Should have Startup, Active, Recovery, Frame Adv, Proration.
        self.assertEqual(len(embed.fields), 5)
        # Fields should be ordered.
        self.assertEqual(embed.fields[0].name, "First Active") # Named to match wiki.
        self.assertEqual(embed.fields[1].name, "Active")
        self.assertEqual(embed.fields[2].name, "Recovery")
        self.assertEqual(embed.fields[3].name, "Frame Adv")
        self.assertEqual(embed.fields[4].name, "Proration")
        self.assertTrue(all(field.inline for field in embed.fields))


if __name__ == '__main__':
    unittest.main()
