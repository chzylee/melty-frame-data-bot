import sys
import requests
import yaml
from local_env import env_vars


env = input("Enter bot environment: ")

if env.lower() != 'dev' and env.lower() != 'prod':
    print("Allowed environments are 'dev' or 'prod'")
    sys.exit()

bot_token = env_vars[env]["bot_token"]
application_id = env_vars[env]["application_id"]

if env.lower() == 'dev':
    server_id = env_vars[env]["server_id"]
    url = f"https://discord.com/api/v10/applications/{application_id}/guilds/{server_id}/commands"
else:
    url = f'https://discord.com/api/v10/applications/{application_id}/commands'

# global commands are cached and only update every hour
# URL = f'https://discord.com/api/v10/applications/{APPLICATION_ID}/commands'

with open("bot_commands.yaml", "r") as file:
    yaml_content = file.read()

commands = yaml.safe_load(yaml_content)
headers = {"Authorization": f"Bot {bot_token}", "Content-Type": "application/json"}

# Send the POST request for each command
for command in commands:
    response = requests.post(url, json=command, headers=headers)
    command_name = command["name"]
    print(f"Command {command_name} created: {response.status_code}")

print(response.json())