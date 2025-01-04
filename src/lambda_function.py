import boto3
import bot
import constants
import discord_helper
import logger

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

def lambda_handler(event, context):
    print(f"event {event}") # debug print

    # verify the signature
    try:
        discord_helper.verify_signature(event)
    except Exception as e:
        raise Exception(f"[UNAUTHORIZED] Invalid request signature: {e}")

    if not event["body-json"]:
        return { "message": "Request is not Lambda event: 'body-json' not found" }

    body = event["body-json"]

    if discord_helper.is_ping_pong(body):
        print("is_ping_pong: True")
        response = constants.PING_PONG
    else:
        data = body["data"]
        command_name = data["name"]
        logger.log_command(command_name)

        response = bot.process_bot_command(
            data=data,
            command_name=command_name,
            dynamodb=dynamodb) # Should use DB when Lambda is triggered.

    logger.log_response(response)
    return response
