import unittest
import boto3
import constants
from moto import mock_aws
from typing import List
import bot
from commands.framedata import FrameData

# Note: not mocking as this test will contain high-level assertions
# to ensure bot's orchestration works as expected.

class TestBotProcess(unittest.TestCase):
    def test_process_bot_command_catches_UserInputException_returns_error_in_message(self):
        data = {
            "guild_id": "1232882434857631755",
            "id": "1232889478297948221",
            "name": "framedata",
            "options": [
                { "name": "moon", "type": 3, "value": "C" },
                # Submitting invalid character should cause error for framedata command.
                { "name": "character", "type": 3, "value": "notcharacter" },
                { "name": "move", "type": 3, "value": "5B" }
            ],
            "type": 1
        }

        response = bot.process_bot_command(data, "framedata")
        self.assertEqual(len(response["data"]["embeds"]), 0)
        self.assertGreater(len(response["data"]["content"]), 0)

    def test_process_bot_command_given_characterlist_command_returns_text_message(self):
        # Passing empty data as it should not be needed
        response = bot.process_bot_command({}, "characterlist")
        self.assertGreater(len(response["data"]["content"]), 0)

    @mock_aws
    def test_process_bot_command_given_framedata_command_with_options_returns_framedata_response(self):
        # Mock simulating real env.
        dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
        table = dynamodb.create_table(
            TableName=constants.DYNAMODB_TABLE_NAME,
            KeySchema=[
                {
                    'AttributeName': constants.DYNAMODB_PARTITION_KEY,
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': constants.DYNAMODB_SORT_KEY,
                    'KeyType': 'RANGE'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': constants.DYNAMODB_PARTITION_KEY,
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': constants.DYNAMODB_SORT_KEY,
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        test_data = {
            # Data should be indexed by Name and Moon used in wiki url path.
            # This treats the wiki paths as the source of truth for names.
            constants.DYNAMODB_PARTITION_KEY: "Len",
            constants.DYNAMODB_SORT_KEY: "Crescent_Moon",
            "moves": [
                {
                    "input": "j.236C",
                    "first_active": "1+9 ~ 10",
                    "active": "~18",
                    "recovery": "6",
                    "frame_adv": "-2 (TK)",
                    "proration": "100%",
                    "invuln": "Full 1-13",
                    "image": "https://wiki.gbl.gg/images/thumb/3/32/Clenj236c.png/175px-Clenj236c.png",
                    "alts": []
                }
            ]
        }
        table.put_item(Item=test_data)

        # Copied data from a request from integration testing.
        # Even if not all fields are used, using this to simulate realistic case.
        data = {
            "guild_id": "1232882434857631755",
            "id": "1232889478297948221",
            "name": "framedata",
            "options": [
                { "name": "moon", "type": 3, "value": "C" },
                { "name": "character", "type": 3, "value": "Len" },
                { "name": "move", "type": 3, "value": "j.236C" }
            ],
            "type": 1
        }

        response = bot.process_bot_command(data=data, command_name="framedata", dynamodb=dynamodb)

        self.assertIsNone(response["data"]["content"])

        response_embeds = response["data"]["embeds"]
        self.assertIsInstance(response_embeds, List)
        self.assertEqual(len(response_embeds), 1) # 1 for image and 1 for framedata.
        # Check Embed is dict to ensure this method returned JSON serializable data.
        self.assertIsInstance(response_embeds[0], dict)
