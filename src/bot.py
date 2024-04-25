
import logger
import constants
from commands import teatime as TeaTime
from commands.framedata import FrameData


def process_bot_command(data: dict, command_name: str) -> dict:
    message_content = None
    reponse = None
    embeds = []

    try:
        if command_name == "teatime":
            message_content = TeaTime.have_teatime()
        elif command_name == "framedata":
            framedata = FrameData(data)
            message_content = framedata.get_move_name()
            embeds = framedata.get_frame_data()
        else:
            logger.log_command_match_error(command_name)

    except Exception as e:
        logger.log_command_processing_exception(command_name, e)

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