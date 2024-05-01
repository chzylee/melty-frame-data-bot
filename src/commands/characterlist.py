from typing import List
from data import mizuumi

def get_allowed_names() -> str:
    char_names = [name.capitalize() for name in mizuumi.CHAR_MAPPINGS.keys()]
    joined_names = ", ".join(char_names)
    return f"Allowed names for `/framedata` command:\n```{joined_names}```"
