import requests
from data import mizuumi
from typing import List
from discord import Embed

class FrameData:
    moon: str
    char_name: str
    move_input: str

    def __init__(self, data: dict):
        # Command inputs defined in this order.
        self.moon = data["options"][0]["value"]
        self.char_name = data["options"][1]["value"]
        self.move_input = data["options"][2]["value"]

    def _get_move_name(self) -> str:
        input_start_index = 0
        prefix = ""
        if self.move_input[0].lower() == "j":
            prefix = "j" # Ensure air moves always start with lowercase j.
            input_start_index = 1
            if self.move_input[1] != ".":
                prefix += "." # Index 1 includes present "." if found, but we add it this way if not present.
        # Reamining part of move_input should be A/B/C/D at the end and should be capitalized.
        formatted_move = f"{prefix}{self.move_input[input_start_index:].upper()}"
        return f"{self.moon.upper()}-{self.char_name.capitalize()} {formatted_move}"

    def get_frame_data(self) -> List[Embed]:
        char_url = mizuumi.get_character_url(self.char_name, self.moon)
        # TODO: make request to this url and get data.

        # TODO: replace with real data
        framedata_embed = Embed(title=self._get_move_name())
        framedata_embed.set_image(url="https://wiki.gbl.gg/images/1/10/CLen_421D.png")
        framedata_embed.add_field(name="First Active", value="6")
        framedata_embed.add_field(name="Active", value="7")
        framedata_embed.add_field(name="Recovery", value="24")
        framedata_embed.add_field(name="Frame Adv", value="-13")
        framedata_embed.add_field(name="Proration", value="78%")
        return [framedata_embed]
