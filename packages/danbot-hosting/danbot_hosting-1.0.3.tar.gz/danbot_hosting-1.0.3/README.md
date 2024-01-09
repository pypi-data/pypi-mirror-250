# dbh-bots-wrapper - DanBot Hosting Bots API Wrapper

## Overview

The `dbh-bots-wrapper` is a Python module designed to simplify interactions with the DanBot Hosting API for adding Discord bots. It provides a `bot` class with methods for adding bots, retrieving bot information, and obtaining information of all bots.

## Installation

To use `dbh-bots-wrapper`, you must install it first. You can do this using the following command:

```bash
pip install dbh-bots-wrapper
```

## Usage

### Importing the Module

```python
from dbh-bots-wrapper import bot
```

### Initializing the Bot

```python
my_bot = bot(
    discord_id="YOUR_DISCORD_BOT_ID",
    owner_id="YOUR_DISCORD_USER_ID",
    api_key="YOUR_DBH_API_KEY",
    name="BotName",
    avatar="AvatarURL",
    users=1000,
    guilds=10,
    shards=1
)
```

### API Information

To retrieve information about the bot:

```python
info = my_bot.info()
print(info)
```

### Bot Status

To retrieve the status of the API from the DanBot Hosting API:

```python
status = my_bot.status()
print(status)
```

### Adding a Bot

To add the bot to DanBot Hosting:

```python
add_result = my_bot.add_bot()
print(add_result)
```

### Retrieving a Bot

To retrieve information about a specific bot:

```python
bot_info = my_bot.get_bot()
print(bot_info)
```

### Retrieving Bot List

To retrieve a information of all bots:

```python
bots_list = my_bot.get_bots()
print(bots_list)
```

## Example

```python
from dbhwrapper import bot

# Initialize the bot
my_bot = bot(
    discord_id="123456789012345678",
    owner_id="987654321098765432",
    api_key="YOUR_DBH_API_KEY",
    name="MyAwesomeBot",
    avatar="https://example.com/avatar.png",
    users=1000,
    guilds=10,
    shards=1
)

# Retrieve bot information
info = my_bot.info()
print("Bot Information:", info)

# Retrieve bot status
status = my_bot.status()
print("Bot Status:", status)

# Add the bot to DanBot Hosting
add_result = my_bot.add_bot()
print("Add Bot Result:", add_result)

# Retrieve information about the added bot
bot_info = my_bot.get_bot()
print("Bot Info:", bot_info)

# Retrieve a list of bots associated with the user
bots_list = my_bot.get_bots()
print("User's Bots:", bots_list)
```

Replace the placeholder values with your actual Discord bot and user information.


# DanBot

> [!NOTE]
> Found a bug? Open a [GitHub Issue](https://github.com/DanBot-Hosting/DBH-BOT-API/issues/new). Found a vulnerability? Open a ticket in our [Discord Server](https://discord.gg/dbh) (Soon enough on a support website!)

> Made with ❤️ by [DanBot Hosting](https://danbot.host).
