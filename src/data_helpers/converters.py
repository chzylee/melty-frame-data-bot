from discord import Embed

def convert_embed_to_json(embed: Embed) -> object:
    return {
        # TODO: implement other properties.
        "title": embed.title
    }
