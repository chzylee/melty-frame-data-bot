import requests
from bs4 import BeautifulSoup
from data import mizuumi
from typing import List, Union
from discord import Embed
from data import inputs
from models.errors import UserInputException
from models.framedata import MoveFrameData
from models.inputcomponents import InputComponents

class FrameData:
    moon: str
    char_name: str
    move_input: InputComponents

    def _match_move_input(self) -> Union[InputComponents, None]:
        for matcher in inputs.input_matchers:
            match_result = matcher(input=self.move_input)
            if match_result is not None:
                return match_result
        return None

    # Combines moon+name to output in the way community often refers to characters.
    def _get_full_char_name(self) -> str:
        return f"{self.moon}-{self.char_name}"

    def __init__(self, data: dict):
        # Command inputs defined in this order.
        self.moon = data["options"][0]["value"]
        self.char_name = str(data["options"][1]["value"]).capitalize()
        move_input = data["options"][2]["value"]
        if move_input is None:
            raise UserInputException(f"Invalid move input '{move_input}'")
        self.move_input = InputComponents.from_string(move_input)

    def _parse_frame_data_from_wiki(self, soup: BeautifulSoup) -> MoveFrameData:
        # Inputs are labeled differently on wiki pages for charged moves and specials.
        move_search_tag = "small" if self.move_input.is_charged() or self.move_input.is_special() else "big"
        input_labels = [tag.text for tag in soup.find_all(move_search_tag)]
        return

    def get_frame_data(self) -> List[Embed]:
        char_wiki_url = mizuumi.get_character_url(self.char_name, self.moon)
        print(f"Sending request to '{char_wiki_url}'")
        wiki_response = requests.get(char_wiki_url)
        print(f"Wiki response: {wiki_response}")
        print(f"Wiki response: {wiki_response.text}")
        wiki_soup = BeautifulSoup(markup=wiki_response.text, features="html.parser")
        print("Instantiated BeautifulSoup")
        # TODO: make request to this url and get data.

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
