import logging
from typing import List
from discord import Embed
from models.errors import UserInputException

INFO_TAG = "[INFO] |"
COMMAND_ERROR_TAG = "[COMMAND_ERROR] |"
GENERAL_ERROR_TAG = "[ERROR] |"

def log_command(command_name: str):
    print(f"{INFO_TAG} Received command '{command_name}'")

def log_command_match(command_name: str):
    print(f"{INFO_TAG} Matched command '{command_name}'")

def log_command_finished(command_name: str):
    print(f"{INFO_TAG} Finished processing command {command_name}")

def log_message_data(message_content: str, embeds: List[Embed]):
    print(f"{INFO_TAG} Message content: '{message_content}'")
    print("Embeds:")
    for embed in embeds:
        print(f"{INFO_TAG} {embed.to_dict()}")

def log_response(response: dict):
    print(f"{INFO_TAG} Response: {response}")

def log_command_match_error(command_name: str):
    print(f"{COMMAND_ERROR_TAG} Failed to match command '{command_name}'")

def log_command_processing_exception(command_name: str, exception: Exception):
    logging.exception(
        msg = f"{COMMAND_ERROR_TAG} Error processing command '{command_name}'",
        exc_info = exception
    )

def log_user_input_exception(command_name: str, exception: UserInputException):
    print(f"{COMMAND_ERROR_TAG} Command '{command_name}' raised user input error: {exception}")

def log_exception(message: str, exception: Exception):
    print(f"{GENERAL_ERROR_TAG} {message}")
    logging.exception(msg=message, exc_info=exception)
