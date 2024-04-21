import requests
import local_env

APP_ID = "1231490345565683814"
SERVER_ID = "883089201850093578"
BOT_TOKEN = local_env.BOT_TOKEN

# global commands are cached and only update every hour
# url = f'https://discord.com/api/v10/applications/{APP_ID}/commands'

# while server commands update instantly
# they're much better for testing
url = f'https://discord.com/api/v10/applications/{APP_ID}/guilds/{SERVER_ID}/commands'

json = [
  {
    'name': 'poronga',
    'description': 'Test command.',
    'options': []
  }
]

response = requests.put(url, headers={
  'Authorization': f'Bot {BOT_TOKEN}'
}, json=json)

print(response.json())