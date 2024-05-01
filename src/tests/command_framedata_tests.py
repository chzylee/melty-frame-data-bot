import unittest
import boto3
import constants
from moto import mock_aws
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

    @mock_aws
    def test_get_frame_data_given_char_and_move_in_db_returns_data_in_populated_embed(self):
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

        move_input = "j.236C"
        first_active = "1+9 ~ 10"
        active = "~18"
        recovery = "6"
        frame_adv = "-2 (TK)"
        proration = "100%"
        invuln = "Full 1-13"
        image = "https://wiki.gbl.gg/images/thumb/3/32/Clenj236c.png/175px-Clenj236c.png"
        test_data = {
            # Data should be indexed by Name and Moon used in wiki url path.
            # This treats the wiki paths as the source of truth for names.
            constants.DYNAMODB_PARTITION_KEY: "Len",
            constants.DYNAMODB_SORT_KEY: "Crescent_Moon",
            "moves": [
                {
                    "input": move_input,
                    "first_active": first_active,
                    "active": active,
                    "recovery": recovery,
                    "frame_adv": frame_adv,
                    "proration": proration,
                    "invuln": invuln,
                    "image": image
                }
            ]
        }
        table.put_item(Item=test_data)

        moon = "C"
        character = "Len"
        data = {
            "options": [
                # Input order is moon, char name, move input
                { "value": moon },
                { "value": character },
                { "value": move_input }
            ]
        }
        framedata = FrameData(data=data, dynamodb=dynamodb)

        embeds = framedata.get_frame_data()
        self.assertIsInstance(embeds, List)
        self.assertEqual(len(embeds), 1)
        embed = embeds[0]

        self.assertEqual(embed.title, "C-Len j.236C") # Standard name format for moves
        self.assertGreater(len(embed.url), 0)
        self.assertIsNotNone(embed.image)
        self.assertEqual(embed.image.url, image)

        # Should have Startup, Active, Recovery, Frame Adv, Proration.
        self.assertEqual(len(embed.fields), 6)
        # Fields should be ordered.
        self.assertEqual(embed.fields[0].name, "First Active") # Named to match wiki.
        self.assertEqual(embed.fields[0].value, first_active)
        self.assertEqual(embed.fields[1].name, "Active")
        self.assertEqual(embed.fields[1].value, active)
        self.assertEqual(embed.fields[2].name, "Recovery")
        self.assertEqual(embed.fields[2].value, recovery)
        self.assertEqual(embed.fields[3].name, "Frame Adv")
        self.assertEqual(embed.fields[3].value, frame_adv)
        self.assertEqual(embed.fields[4].name, "Proration")
        self.assertEqual(embed.fields[4].value, proration)
        self.assertEqual(embed.fields[5].name, "Invuln")
        self.assertEqual(embed.fields[5].value, invuln)
        self.assertTrue(all(field.inline for field in embed.fields))


if __name__ == '__main__':
    unittest.main()
