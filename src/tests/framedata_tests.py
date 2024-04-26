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
        self.assertEqual(framedata.move_input, move_input)

    def test_get_move_name_given_ground_normal_returns_correctly_formatted_name(self):
        data = {
            "options": [
                { "value": "C" },
                { "value": "Len" },
                { "value": "3C" }
            ]
        }
        framedata = FrameData(data)
        message = framedata._get_move_name()
        # Hardcoding message based on above data to check to avoid forcing logic into test.
        self.assertEqual(message, "C-Len 3C")

    def test_get_move_name_given_air_move_returns_correctly_formatted_name(self):
        data = {
            "options": [
                { "value": "C" },
                { "value": "Len" },
                { "value": "j.236C" }
            ]
        }
        framedata = FrameData(data)
        message = framedata._get_move_name()
        # Hardcoding message based on above data to check to avoid forcing logic into test.
        self.assertEqual(message, "C-Len j.236C")

    def test_get_move_name_given_shorthand_air_normal_returns_correctly_formatted_name(self):
        data = {
            "options": [
                { "value": "C" },
                { "value": "Len" },
                { "value": "jB" } # Different from standard j.B format
            ]
        }
        framedata = FrameData(data)
        message = framedata._get_move_name()
        self.assertEqual(message, "C-Len j.B")

    def test_get_move_name_given_nonstandard_capitalization_returns_correctly_formatted_name(self):
        data = {
            "options": [
                { "value": "c" }, # Differs from standard capital moon initial format
                { "value": "lEn" }, # Handle case of weird capitalization in name.
                { "value": "JA" } # Different from standard j.A format.
            ]
        }
        framedata = FrameData(data)
        message = framedata._get_move_name()
        self.assertEqual(message, "C-Len j.A")

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
