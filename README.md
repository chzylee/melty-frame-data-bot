# melty-frame-data-bot

Discord bot to query MBAACC frame data from Mizuumi.

## Architecture

This bot runs via AWS Lambda hooked into a Discord bot via Interactions Endpoint URL.

PyNaCl was imported for verification with Discord via Lambda Layers. The Layer consumes nacl.zip from S3, which is a zipped PyNaCl installed and packaged on EC2 instance via Python 3.8.

### Poronga

Poronga exists as the starting point for the project. The Python code is the boilerplate to verify a Discord bot ping, and this was used as the first entry to the Lambda.

This was created following tutorial for setting up a serverless Discord bot [here](https://oozio.medium.com/serverless-discord-bot-55f95f26f743).

## Update Commands

[update_commands.py](./update_commands.py) is a script calling the endpoint needed in order to update Slash Commands. As of April 2024, these are only updateable via request to this endpoint. Script will be update/run as needed.

## Assets

Images used in the bot's presentation will be committed to keep everything together. Namely [icon.png](./icon.png) is used as the bot's profile picture.
