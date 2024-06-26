import logger
import constants
from commands import characterlist as CharacterList
from commands.framedata import FrameData
from models.errors import UserInputException

# Default db resource to null to avoid requiring running DB requests outside of Lambda env.
def process_bot_command(data: dict, command_name: str, dynamodb = None) -> dict:
    message_content = None
    reponse = None
    embeds = []

    try:
        if command_name == "howtoframedata":
            message_content = "Select moon and input char name and move input (e.g. 236C, 236A~236B, ~214X Ender)."
            message_content += "\nIf the first command fails, press up and try again. Sometimes first try fails."
            message_content += "\nContact @enpicie on discord about any issues."
        elif command_name == "characterlist":
            logger.log_command_match(command_name)
            message_content = CharacterList.get_allowed_names()
        elif command_name == "framedata":
            logger.log_command_match(command_name)
            framedata = FrameData(data, dynamodb)
            embeds = framedata.get_frame_data()
            if len(embeds) > 1:
                # Get message related to additional move(s) as first embed's data will show.
                message_content = framedata.get_multiple_moves_message(embeds[1:])
        else:
            logger.log_command_match_error(command_name)

    except UserInputException as e:
        logger.log_user_input_exception(command_name, e)
        # Error type suggests we want to tell user about error.
        message_content = e.message
        embeds = [] # Empty embeds to return just error message
    except Exception as e:
        logger.log_command_processing_exception(command_name, e)
        raise e

    try:
        logger.log_message_data(message_content, embeds)

        response = {
            "type": constants.RESPONSE_TYPES["MESSAGE_WITH_SOURCE"],
            "data": {
                "content": message_content,
                "embeds": []
            }
        }
        if len(embeds) > 0:
            # to_dict() is on discord.py's Embed class but cannot specify types for python lambdas.
            convert_embed = lambda embed: embed.to_dict()
            response["data"]["embeds"] = [convert_embed(embed) for embed in embeds]

    except Exception as e:
        logger.log_exception("Error setting response data", e)
        raise e

    return response