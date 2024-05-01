import constants
from data import mizuumi
from typing import List, Union
from discord import Embed
from data import inputreader as InputReader
from models.errors import UserInputException
from models.moveframedata import MoveFrameData

class FrameData:
    moon: str
    char_name: str
    move_input: str
    dynamodb: any # No type label to specify for dynamodb resource

    def _format_move_input(self) -> str:
        input_start_index = 0
        prefix = ""
        if self.move_input[0].lower() == "j":
            prefix = "j" # Ensure air moves always start with lowercase j.
            input_start_index = 1
            if self.move_input[1] != ".":
                prefix += "." # Index 1 includes present "." if found, but we add it this way if not present.
        # Reamining part of move_input should be A/B/C/D at the end and should be capitalized.
        formatted_move = f"{prefix}{self.move_input[input_start_index:].upper()}"

    def _match_move_input(self) -> Union[str, None]:
        for matcher in InputReader.input_matchers:
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
        self.move_input = InputReader.format_move_input(move_input)
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
        # Projected "moves" field is a list of moves.
        move_list = [MoveFrameData.from_dynamoDB_item(item) for item in db_item["Item"]["moves"]]
        print(f"Parsed moves from DB: {move_list}")
        for move in move_list:
            print(f"Attempting to match move {move}")
            if move.input == str(self.move_input):
                print(f"Successfully matched with input '{self.move_input}'")
                return move
        print(f"Failed to match move '{self.move_input}' with move list from DB")
        raise Exception(f"Failed to get frame data for {self._get_full_char_name()} {self.move_input}")

    def get_frame_data(self) -> List[Embed]:
        char_wiki_url = mizuumi.get_character_url(self.char_name, self.moon)
        move_framedata = self._query_frame_data()

        framedata_embed = Embed(
            title=f"{self._get_full_char_name()} {self.move_input}",
            url=char_wiki_url
        )
        framedata_embed.set_image(url=move_framedata.image)
        framedata_embed.add_field(name="First Active", value=move_framedata.first_active)
        framedata_embed.add_field(name="Active", value=move_framedata.active)
        framedata_embed.add_field(name="Recovery", value=move_framedata.recovery)
        framedata_embed.add_field(name="Frame Adv", value=move_framedata.frame_adv)
        framedata_embed.add_field(name="Proration", value=move_framedata.proration)
        framedata_embed.add_field(name="Invuln", value=move_framedata.invuln)
        return [framedata_embed]
