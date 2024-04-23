import requests
from discord import Embed
from app.commands.data.types import MeltyMove

def get_char_and_move(data: dict) -> MeltyMove:
    char_name = data["options"][0]["value"] # Char is first option
    move_input = data["options"][1]["value"]
    return MeltyMove(char=char_name, input=move_input)

def get_frame_data(melty_move: MeltyMove) -> Embed:
    response = Embed(title=f"{melty_move.char} {melty_move.input}")
    return response