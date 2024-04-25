import unittest
from typing import List
from discord import Embed
import bot
from commands.framedata import FrameData

# Note: not mocking as this test will contain high-level assertions
# to ensure bot's orchestration works as expected.

class TestBotProcess(unittest.TestCase):
    def test_process_bot_command_given_framedata_command_and_options_returns_framedata_response(self):
        # Copied data from a request from integration testing.
        # Even if not all fields are used, using this to simulate realistic case.
        data = {
            "guild_id": "1232882434857631755",
            "id": "1232889478297948221",
            "name": "framedata",
            "options": [
                { "name": "moon", "type": 3, "value": "C" },
                { "name": "character", "type": 3, "value": "Len" },
                { "name": "move", "type": 3, "value": "5B" }
            ],
            "type": 1
        }

        response = bot.process_bot_command(data, "framedata")

        self.assertIsInstance(response["data"]["content"], str)

        response_embeds = response["data"]["embeds"]
        self.assertIsInstance(response_embeds, List)
        self.assertEqual(len(response_embeds), 2) # 1 for image and 1 for framedata.
        # Check they are dicts to ensure this method returned JSON serializable data.
        self.assertIsInstance(response_embeds[0], dict)
        self.assertIsInstance(response_embeds[1], dict)
