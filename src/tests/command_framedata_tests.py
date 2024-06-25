import unittest
import boto3
import constants
from moto import mock_aws
from typing import List
from discord import Embed
from models.errors import UserInputException
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

    def test_initialization_given_invalid_character_name_in_data_raises_UserInputException(self):
        moon = "C"
        character = "zapoke" # intentionally wrong name.
        move_input = "3C"
        data = {
            "options": [
                # Input order is moon, char name, move input
                { "value": moon },
                { "value": character },
                { "value": move_input }
            ]
        }
        with self.assertRaises(UserInputException):
            framedata = FrameData(data)

    def test_get_multiple_moves_message_given_multiple_move_embeds_returns_message_with_embed_titles(self):
        data = {
            "options": [
                # Input order is moon, char name, move input
                { "value": "Crescent" },
                { "value": "Warachia" },
                { "value": "214C" }
            ]
        }
        framedata = FrameData(data)

        # Simulate case for Wara 214C which has the summon data and data for the summoned Nero
        embeds = [
            Embed(title="C-Warachia 214C"),
            Embed(title="C-Warachia 214C (Nero)")
        ]

        message = framedata.get_multiple_moves_message(embeds)
        self.assertIn("C-Warachia 214C (Nero)", message)

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
                    "image": image,
                    "alts": []
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

    @mock_aws
    def test_get_frame_data_given_alt_input_of_move_in_db_returns_data_in_populated_embed(self):
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

        move_input = "623A~A"
        alt_input = "623AA" # Another common way of writing this input.
        first_active = "1+9 ~ 10" # Numbers in this test still correspond to j.236C. Values don't matter for this.
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
                    "image": image,
                    "alts": [alt_input]
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
                { "value": alt_input } # Won't match base input, but should match alt.
            ]
        }
        framedata = FrameData(data=data, dynamodb=dynamodb)

        embeds = framedata.get_frame_data()
        self.assertIsInstance(embeds, List)
        self.assertEqual(len(embeds), 1)
        embed = embeds[0]

        self.assertEqual(embed.title, "C-Len 623A~A") # Standard name format for moves
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

    @mock_aws
    def test_get_frame_data_given_poorly_formatted_input_for_move_in_db_returns_data_in_populated_embed(self):
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
                    "image": image,
                    "alts": []
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
                { "value": "j236c" } # Should not care that "." after j was missed and should be case insensitive.
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

    @mock_aws
    def test_get_frame_data_given_input_matching_multiple_moves_in_db_returns_data_in_populated_embed(self):
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
            constants.DYNAMODB_PARTITION_KEY: "Warachia",
            constants.DYNAMODB_SORT_KEY: "Crescent_Moon",
            "moves": [
                {
                    "input": "214C",
                    "image": "https://wiki.gbl.gg/images/thumb/c/c9/MBCWarachia214C.png/175px-MBCWarachia214C.png",
                    "first_active": "-",
                    "active": "49",
                    "recovery": "-",
                    "frame_adv": "-",
                    "proration": "-",
                    "invuln": "-",
                    "alts": []
                },
                {
                    "input": "214C (Nero)",
                    "image": "https://wiki.gbl.gg/images/thumb/c/c9/MBCWarachia214C.png/175px-MBCWarachia214C.png",
                    "first_active": "75",
                    "active": "3",
                    "recovery": "-",
                    "frame_adv": "-",
                    "proration": "80% (O)",
                    "invuln": "-",
                    "alts": ["214C", "214C Nero", "214 Nero", "Nero Summon"]
                }
            ]
        }
        table.put_item(Item=test_data)

        move_input = "214C"
        moon = "C"
        character = "Warachia"
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
        self.assertEqual(len(embeds), 2)
        embed1 = embeds[0]
        embed2 = embeds[1]

        self.assertIn("C-Warachia", embed1.title) # Ensure embed titles contain char name.
        self.assertIn("C-Warachia", embed2.title)
        # Won't check both are fully populated to keep test light. Leaving that to other tests



if __name__ == '__main__':
    unittest.main()
