from models.errors import UserInputException

# Mappings map Input Value -> String used in Mizuumi URLs.

_MOON_MAPPINGS = {
    "C": "Crescent_Moon",
    "H": "Half_Moon",
    "F": "Full_Moon"
}

# Keys set in all lowercase to simplify matching.
CHAR_MAPPINGS = {
    "akiha": "Akiha_Tohno",
    "aoko": "Aoko_Aozaki",
    "arc": "Arcueid_Brunestud",
    "arcueid": "Arcueid_Brunestud",
    "ciel": "Ciel",
    "hime": "Archetype:_Earth",
    "hisui": "Hisui",
    "koha-mech": "Koha_%26_Mech",
    "koha mech": "Koha_%26_Mech",
    "kohamech": "Koha_%26_Mech",
    "kohaku": "Kohaku",
    "kouma": "Kouma_Kishima",
    "len": "Len",
    "maids": "Hisui_%26_Kohaku", # Presetving % codes in routes to avoid errors.
    "mech": "Mech-Hisui",
    "miyako": "Miyako_Arima",
    "nac": "Neco-Arc_Chaos",
    "nanaya": "Shiki_Nanaya",
    "neco": "Neco-Arc",
    "neco-mech": "Neco_%26_Mech", # Support original and common spellings.
    "neco mech": "Neco_%26_Mech",
    "necomech": "Neco_%26_Mech",
    "neko-mech": "Neco_%26_Mech",
    "neko mech": "Neco_%26_Mech",
    "nekomech": "Neco_%26_Mech",
    "nero": "Nero_Chaos",
    "nrvnqsr": "Nero_Chaos",
    "pciel": "Powered_Ciel",
    "p-ciel": "Powered_Ciel",
    "warc": "Red_Arcueid",
    "red arc ": "Red_Arcueid",
    "ries": "Riesbyfe_Stridberg",
    "roa": "Roa",
    "ryougi": "Shiki_Ryougi",
    "sats": "Satsuki_Yumizuka",
    "satsuki": "Satsuki_Yumizuka",
    "sei": "Akiha_Tohno_(Seifuku)",
    "seifuku": "Akiha_Tohno_(Seifuku)",
    "sion": "Sion_Eltnam_Atlasia",
    "tohno": "Shiki_Tohno",
    "tony": "Shiki_Tohno",
    "vaki": "Akiha_Vermilion",
    "vakiha": "Akiha_Vermilion",
    "vsion": "Sion_TATARI",
    "wara": "Warachia",
    "warachia": "Warachia",
    "wlen": "White_Len",
    "w-len": "White_Len"
}

def get_character_url(char_name: str, moon: str):
    if char_name.lower() not in CHAR_MAPPINGS:
        raise UserInputException(f"Name '{char_name}' not allowed.")
    # No need to validate moon because values are limited to specific choices by bot command.

    char_path = CHAR_MAPPINGS[char_name.lower()]
    moon_path = _MOON_MAPPINGS[moon]
    return f"https://wiki.gbl.gg/w/Melty_Blood/MBAACC/{char_path}/{moon_path}"
