# melty-frame-data-bot

Discord bot to query MBAACC frame data from Mizuumi.

## Architecture

This bot runs via AWS Lambda hooked into a Discord bot via Interactions Endpoint URL.

PyNaCl was imported for verification with Discord via Lambda Layers. The Layer consumes nacl.zip from S3, which is a zipped PyNaCl installed and packaged on EC2 instance via Python 3.8.

### File Organization

- [lambda_function.py](./src/lambda_function.py) is the entry point to the Lambda (following AWS default standard).
- Command logic will go in [/commands](./src/commands/); however, commands are still imported as `import poronga` (for commands/poronga.py) as zipping will flatten the file structure for successful import. This done to keep code organized.

## Update Commands

[update_commands.py](./command-management/update_commands.py) is a script calling the endpoint needed in order to update Slash Commands. As of April 2024, these are only updateable via request to this endpoint. Script will be update/run as needed. This has been based on guide [here](https://www.youtube.com/watch?v=BmtMr6Nmz9k).

## Assets

Images used in the bot's presentation will be committed to keep everything together. Namely [icon.png](./icon.png) is used as the bot's profile picture.
