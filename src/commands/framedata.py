import boto3
import constants
from data import mizuumi
from typing import List, Union
from discord import Embed
from data import inputreader
from models.errors import UserInputException
from models.framedata import MoveFrameData
from models.inputcomponents import InputComponents

class FrameData:
    moon: str
    char_name: str
    move_input: InputComponents
    dynamodb: any # No type label to specify for dynamodb resource

    def _match_move_input(self) -> Union[InputComponents, None]:
        for matcher in inputreader.input_matchers:
            match_result = matcher(input=self.move_input)
            if match_result is not None:
                return match_result
        return None

    # Combines moon+name to output in the way community often refers to characters.
    def _get_full_char_name(self) -> str:
        return f"{self.moon}-{self.char_name}"

    def __init__(self, data: dict, dynamodb = None):
        # Command inputs defined in this order.
        self.moon = data["options"][0]["value"]
        self.char_name = str(data["options"][1]["value"]).capitalize()
        move_input = data["options"][2]["value"]
        if move_input is None:
            raise UserInputException(f"Invalid move input '{move_input}'")
        self.move_input = InputComponents.from_string(move_input)
        self.dynamodb = dynamodb

    def _query_frame_data(self) -> MoveFrameData:
        table = self.dynamodb.Table(constants.DYNAMODB_TABLE_NAME)
        moon_path = mizuumi.get_moon_path(self.moon)
        char_path = mizuumi.get_char_path(self.char_name)
        db_key = {
            constants.DYNAMODB_PARTITION_KEY: char_path ,
            constants.DYNAMODB_SORT_KEY: moon_path
        }
        print(f"DynamoDB request with key: {db_key}")
        db_item = table.get_item(
            Key=db_key,
            ProjectionExpression="moves" # Name of field for list of moves.
        )
        print(f"From DynamoDB: {db_item}")
        # Projected "moves" field is a list of moves.
        move_list = [MoveFrameData.from_dynamoDB_item(item) for item in db_item["Item"]["moves"]]
        print(f"Parsed moves: {move_list}")

        for move in move_list:
            if move.input == str(self.move_input):
                return move
        return None # Should never occur but providing default to be safe.

    def get_frame_data(self) -> List[Embed]:
        char_wiki_url = mizuumi.get_character_url(self.char_name, self.moon)
        # TODO: use framedata after testing
        if self.dynamodb is not None:
            print("Set to use DB. Proceeding to query frame data.")
            move_framedata = self._query_frame_data()
            print(f"Found frame data for {self.move_input}: {move_framedata}")

        # TODO: replace with real data
        framedata_embed = Embed(
            title=f"{self._get_full_char_name()} {self.move_input}",
            url=char_wiki_url
        )
        framedata_embed.set_image(url="https://wiki.gbl.gg/images/1/10/CLen_421D.png")
        framedata_embed.add_field(name="First Active", value="6")
        framedata_embed.add_field(name="Active", value="7")
        framedata_embed.add_field(name="Recovery", value="24")
        framedata_embed.add_field(name="Frame Adv", value="-13")
        framedata_embed.add_field(name="Proration", value="78%")
        return [framedata_embed]
