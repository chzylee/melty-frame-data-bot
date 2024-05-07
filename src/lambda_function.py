from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import constants
import logger
import bot
import dbclient

def verify_signature(event):
    raw_body = event["rawBody"]
    verify_key = VerifyKey(bytes.fromhex(constants.PUBLIC_KEY))
    auth_sig = event["params"]["header"].get("x-signature-ed25519")
    auth_ts  = event["params"]["header"].get("x-signature-timestamp")

    try:
        verify_key.verify(f"{auth_ts}{raw_body}".encode(), bytes.fromhex(auth_sig))
    except BadSignatureError:
        raise Exception("Verification failed")


def is_lambda_request_event(event) -> bool:
    if event["body-json"]:
        return True
    return False


def is_ping_pong(body: dict) -> bool:
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

    if is_ping_pong(body): # Discord uses "ping pong" message to verify bot.
        print("is_ping_pong: True")
        response = constants.PING_PONG
    else:
        data = body["data"]
        command_name = data["name"]
        logger.log_command(command_name)

        dynamodb = dbclient.get_dynamodb_resource()

        response = bot.process_bot_command(
            data=data,
            command_name=command_name,
            dynamodb=dynamodb) # Should use DB when Lambda is triggered.

    logger.log_response(response)
    return response
