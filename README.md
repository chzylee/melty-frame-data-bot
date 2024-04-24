# melty-frame-data-bot

Discord bot to query MBAACC frame data from Mizuumi.

## Architecture

This bot runs via AWS Lambda hooked into a Discord bot via Interactions Endpoint URL. Python code from [src](./src/) is built and deployed via GitHub Actions workflows, and we update the code using a .zip package pushed to S3.

PyNaCl was imported for verification with Discord via Lambda Layers. The Layer consumes nacl.zip from S3, which is a zipped PyNaCl installed and packaged on EC2 instance via Python 3.8.

### CI/CD

Builds and deployments run automatically via GitHub Actions workflows. There are general Unit Test, Build, and Deploy composable actions to designate CI/CD stages.

Build and Deploy workflows have conditional steps to handle different environments. Each environment should have its own .yml file (e.g. development.yml) that passes inputs into each pipeline stage. Packages will have `-<env>` at the end of their filenames to designate releases from dev deployments.

**Dev** will always build and deploy for continuous integration testing. It deploys to a separate Lambda from Release.

**Release** uses `prod` environment and is triggered when new tags are pushed to `main` matching a numeric pattern such as `1.0.0`. Release builds will pull the version number from the tag and ensure there is not already a .zip package in S3 for the designated app version to avoid overwriting releases for a given version.

### File Organization

- [lambda_function.py](./src/lambda_function.py) is the entry point to the Lambda (following AWS default standard).
- Command logic will go in [/commands](./src/commands/).
  - Can import commands using `from commands import <command_filename>`
- [data_helpers/](./src/data_helpers/) contains utilities to help manage use of Discord data models.

## Update Commands

[update_commands.py](./command-management/update_commands.py) is a script calling the endpoint needed in order to update Slash Commands. As of April 2024, these are only updateable via request to this endpoint. Script will be update/run as needed. This has been based on guide [here](https://www.youtube.com/watch?v=BmtMr6Nmz9k).

Postman collection will also be added with requests to facilitate managing bot commands.

### Bot Token

The Token generated for the bot in Discord developer applications page should _NOT_ be committed. This token is stored locally and is used in the gitignored local_env.py file to allow update_commands.py to import the token without it being committed.

As Noah/enpicie created the bot, ask them for the token if needed.

## Assets

Images used in the bot's presentation will be committed to keep everything together. Namely [icon.png](./icon.png) is used as the bot's profile picture.
