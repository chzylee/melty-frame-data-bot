from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import constants
import logger
from data_helpers import converters
from commands import teatime
from commands.framedata import FrameData

def verify_signature(event):
    raw_body = event["rawBody"]
    verify_key = VerifyKey(bytes.fromhex(constants.PUBLIC_KEY))
    auth_sig = event["params"]["header"].get("x-signature-ed25519")
    auth_ts  = event["params"]["header"].get("x-signature-timestamp")
    
    try:
        verify_key.verify(f"{auth_ts}{raw_body}".encode(), bytes.fromhex(auth_sig))
    except BadSignatureError:
        raise Exception("Verification failed")


def is_lambda_request_event(event):
    if event["body-json"]:
        return True
    return False


def is_ping_pong(body):
    if body["type"]:
        if body["type"] == 1:
            return True
    return False


def lambda_handler(event, context):
    print(f"event {event}") # debug print
    
    # verify the signature
    try:
        verify_signature(event)
    except Exception as e:
        raise Exception(f"[UNAUTHORIZED] Invalid request signature: {e}")

    if not is_lambda_request_event(event):
        return { "message": "Request is not Lambda event: 'body-json' not found" }
    
    body = event["body-json"]
    message_content = None
    reponse = None
    embeds = []

    if is_ping_pong(body):
        print("is_ping_pong: True")
        response = constants.PING_PONG
    else:
        data = body["data"]
        command_name = data["name"]
        logger.log_command(command_name=command_name)

        try:
            if command_name == "teatime":
                message_content = teatime.have_teatime()
            elif command_name == "framedata":
                framedata = FrameData(data)
                message_content = framedata.get_move_name()
                embeds.append(framedata.get_frame_data())

            if message_content == None:
                logger.log_error(constants.COMMAND_NAME_ERROR_MESSAGE)
        except Exception as e:
            print("Error occurred: ", e)
            message_content = f"Error occurred: {e}"

        response = {
            "type": constants.RESPONSE_TYPES["MESSAGE_WITH_SOURCE"],
            "data": { 
                "content": message_content,
                "embeds": []
            }
        }
        
        if len(embeds) > 0:
            for embed in embeds:
                embed_json = converters.convert_embed_to_json(embed)
                response["data"]["embeds"].append(embed_json)

    return response
