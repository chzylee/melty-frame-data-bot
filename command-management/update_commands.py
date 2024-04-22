import requests
import yaml
import local_env

TOKEN = local_env.BOT_TOKEN
APPLICATION_ID = "1231490345565683814"
URL = f"https://discord.com/api/v9/applications/{APPLICATION_ID}/commands"


with open("bot_commands.yaml", "r") as file:
    yaml_content = file.read()

commands = yaml.safe_load(yaml_content)
headers = {"Authorization": f"Bot {TOKEN}", "Content-Type": "application/json"}

# Send the POST request for each command
for command in commands:
    response = requests.post(URL, json=command, headers=headers)
    command_name = command["name"]
    print(f"Command {command_name} created: {response.status_code}")