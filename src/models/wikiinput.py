import re
from models.inputcomponents import InputComponents

class WikiInputComponents(InputComponents):
    # Assumes given input string is from the wiki.
    @classmethod
    def from_string(cls, input: str) -> "InputComponents":
        air_match = cls._get_air_component_match(input)
        directions_match = cls._get_directions_component_match(input)

        air = air_match.group() if air_match else None
        directions = directions_match.group() if directions_match else None
        if directions_match is not None:
            # Start after directions if present.
            button_start_index = directions_match.start() + len(directions)
        else:
            # If no directions, must be air normal, so start after air portion.
            button_start_index = len(air)
        buttons = input[button_start_index:]

        return cls(air=air, directions=directions, button=buttons)
