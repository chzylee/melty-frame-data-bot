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
    "aki": "Akiha_Tohno",
    "aoko": "Aoko_Aozaki",
    "arc": "Arcueid_Brunestud",
    "arcueid": "Arcueid_Brunestud",
    "ciel": "Ciel",
    "cl": "Ciel",
    "hime": "Archetype:_Earth",
    "hisui": "Hisui",
    "koha-mech": "Koha_%26_Mech",
    "koha mech": "Koha_%26_Mech",
    "kohamech": "Koha_%26_Mech",
    "km": "Koha_%26_Mech",
    "kohaku": "Kohaku",
    "koha": "Kohaku",
    "kouma": "Kouma_Kishima",
    "len": "Len",
    # maids commented for now because they havent been added to db yet.
    # "maids": "Hisui_%26_Kohaku", # Preserving % codes in routes to avoid errors.
    "mech": "Mech-Hisui",
    "mech hisui": "Mech-Hisui",
    "m hisui": "Mech-Hisui",
    "miyako": "Miyako_Arima",
    "miya": "Miyako_Arima",
    "nac": "Neco-Arc_Chaos",
    "nanaya": "Shiki_Nanaya",
    "nana": "Shiki_Nanaya",
    "neco": "Neco-Arc",
    "neco-mech": "Neco_%26_Mech", # Support original and common spellings.
    "neco mech": "Neco_%26_Mech",
    "necomech": "Neco_%26_Mech",
    "neko-mech": "Neco_%26_Mech",
    "neko mech": "Neco_%26_Mech",
    "nekomech": "Neco_%26_Mech",
    "nm": "Neco_%26_Mech",
    "nero": "Nero_Chaos",
    "nrvnqsr": "Nero_Chaos",
    "chaos": "Nero_Chaos",
    "pciel": "Powered_Ciel",
    "piel": "Powered_Ciel",
    "p-ciel": "Powered_Ciel",
    "p ciel": "Powered_Ciel",
    "pcl": "Powered_Ciel",
    "p-ciel": "Powered_Ciel",
    "powered ciel": "Powered_Ciel",
    "powerd ciel": "Powered_Ciel",
    "pee seal": "Powered_Ciel",
    "red arcueid": "Red_Arcueid",
    "red arc": "Red_Arcueid",
    "warc": "Red_Arcueid",
    "riesbyfe": "Riesbyfe_Stridberg",
    "ries": "Riesbyfe_Stridberg",
    "roa": "Roa",
    "mike": "Roa",
    "michael": "Roa",
    "ryougi": "Shiki_Ryougi",
    "roog": "Shiki_Ryougi",
    "satsuki": "Satsuki_Yumizuka",
    "sats": "Satsuki_Yumizuka",
    "yumiduka": "Satsuki_Yumizuka",
    "duka": "Satsuki_Yumizuka",
    "sei": "Akiha_Tohno_(Seifuku)",
    "seifuku": "Akiha_Tohno_(Seifuku)",
    "saki": "Akiha_Tohno_(Seifuku)",
    "sigma akiha": "Akiha_Tohno_(Seifuku)",
    "sion": "Sion_Eltnam_Atlasia",
    "tohno": "Shiki_Tohno",
    "tony": "Shiki_Tohno",
    "toneman": "Shiki_Tohno",
    "vakiha": "Akiha_Vermilion",
    "vaki": "Akiha_Vermilion",
    "va": "Akiha_Vermilion",
    "vsion": "Sion_TATARI",
    "vs": "Sion_TATARI",
    "wara": "Warachia",
    "warachia": "Warachia",
    "warakia": "Warachia",
    "white len": "White_Len",
    "wlen": "White_Len",
    "w-len": "White_Len",
    "w len": "White_Len"
}

def get_character_url(char_name: str, moon: str) -> str:
    if char_name.lower() not in CHAR_MAPPINGS:
        raise UserInputException(f"Name '{char_name}' not allowed.")
    # No need to validate moon because values are limited to specific choices by bot command.

    char_path = CHAR_MAPPINGS[char_name.lower()]
    moon_path = _MOON_MAPPINGS[moon]
    return f"https://wiki.gbl.gg/w/Melty_Blood/MBAACC/{char_path}/{moon_path}"

def get_moon_path(moon: str) -> str:
    return _MOON_MAPPINGS[moon]

def get_char_path(char_name: str) -> str:
    return CHAR_MAPPINGS[char_name.lower()]

def is_char_name_valid(char_name: str) -> bool:
    if char_name.lower() in CHAR_MAPPINGS:
        return True
    # Valid names are all keys in the mapping dict.
    return False
