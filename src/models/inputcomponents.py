import re
from typing import Union
from data import inputs

class InputComponents:
    air: Union[str | None]
    directions: Union[str | None]
    button: Union[str | None]

    # All components optional to cover all types.
    def __init__(self, air=None, directions=None, button=None):
        self.air = air
        self.directions = directions
        self.button = button

    @classmethod
    def from_string(cls, input: str) -> "InputComponents":
        air_match = re.search(r"j.", input)
        directions_match = re.search(r"[1-9]{1,3}", input)
        button_match = re.search(r"(\[[ABCD]\])|[ABCD]", input)

        air = air_match.group() if air_match else None
        directions = directions_match.group() if directions_match else None
        button = button_match.group() if button_match else None

        return cls(air=air, directions=directions, button=button)

    def __str__(self):
        air = "" if self.air == None else self.air
        directions = "" if self.directions == None else self.directions
        button = "" if self.button == None else self.button
        return f"{air}{directions}{button}"

    # Determines if input is plain normal.
    # Charged normals are organized differently, so they arent considered plain normals.
    def is_normal(self) -> bool:
        if (
            inputs.match_ground_normal(str(self)) or
            inputs.match_air_normal(str(self)) or
            inputs.match_air_cmd_normal(str(self))
        ) and not self.is_charged():
            return True
        return False

    def is_charged(self) -> bool:
        return "[" in self.button and "]" in self.button

    def is_special(self) -> bool:
        return len(self.directions) > 1

    def is_air(self) -> bool:
        return self.air != None
