def format_move_input(move_input: str) -> str:
    input_start_index = 0
    prefix = ""
    if move_input[0].lower() == "j":
        prefix = "j" # Ensure air moves always start with lowercase j.
        input_start_index = 1
        if move_input[1] != ".":
            prefix += "." # Index 1 includes present "." if found, but we add it this way if not present.
    # Reamining part of move_input should be A/B/C/D at the end and should be capitalized.
    return f"{prefix}{move_input[input_start_index:].upper()}"
