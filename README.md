# melty-frame-data-bot

Discord bot to query MBAACC frame data from Mizuumi.

## Architecture

This bot runs via AWS Lambda hooked into a Discord bot via Interactions Endpoint URL. Python code from [src](./src/) is built and deployed via GitHub Actions workflows, and we update the code using a .zip package pushed to S3.

PyNaCl was imported for verification with Discord via Lambda Layers. The Layer consumes nacl.zip from S3, which is a zipped PyNaCl installed and packaged on EC2 instance via Python 3.8.

### CI/CD

GitHub Actions pipeline is defined in [./github/workflows](./.github/workflows/). App version needs to be explicitly updated in [build.yml](./.github/workflows//build.yml) whenever new deployments need to be made.

#### Tagging

Tags are created with a generic version tag starting at 1.0.0. Increment as needed for updates and update the VERSION env variable in build.yml to do so. Tags are used to mark releases. There is no need to update the version/tag if there is not a need for a new deployment.

#### Pipeline

Build and deployment pipelines will only run when the pipeline is run with a new tag. If there already exists a tag for the version set in build.yml when the code is pushed, no build/deployment will run. Here is a summary of the pipeline overall:

1. Create Git Tag for designated version if one does not yet exist for it.
2. If new tag was created in Git for the current version, `cd src` and zip the src directory.
3. Connect to AWS using GitHub IAM role and upload the .zip file to S3.
4. **Deployment pipeline must be manually triggered** using the version you want to deploy as the input.
5. Deployment pipeline will find the .zip in S3 and update the code for the bot's Lambda using it.

### File Organization

- [lambda_function.py](./src/lambda_function.py) is the entry point to the Lambda (following AWS default standard).
- Command logic will go in [/commands](./src/commands/).
  - Can import commands using `from commands import <command_filename>`

## Update Commands

[update_commands.py](./command-management/update_commands.py) is a script calling the endpoint needed in order to update Slash Commands. As of April 2024, these are only updateable via request to this endpoint. Script will be update/run as needed. This has been based on guide [here](https://www.youtube.com/watch?v=BmtMr6Nmz9k).

Postman collection will also be added with requests to facilitate managing bot commands.

### Bot Token

The Token generated for the bot in Discord developer applications page should _NOT_ be committed. This token is stored locally and is used in the gitignored local_env.py file to allow update_commands.py to import the token without it being committed.

As Noah/enpicie created the bot, ask them for the token if needed.

## Assets

Images used in the bot's presentation will be committed to keep everything together. Namely [icon.png](./icon.png) is used as the bot's profile picture.
