# Commander League Discord Bot

A discord bot to handle the different aspects of a tournament:
- Registration: `!register player_nickname deck_hash deck_link`
- Results:  `!result player_1 result_1-result_2 player_2`
- Performance during one split: `!stats`
- Knowing who is selected for the end-of-split invitational: `!invitational`

## Contribute

**Contributions are welcome !**

## Hosting the bot

If you need to host a new version of the bot yourself,
[Python 3](https://www.python.org/downloads/) is required, as well as an
environment variable `DISCORD_TOKEN`.
The token can be found on your
[Discord applications page](https://discord.com/developers/applications).

The preferred way to run the bot is to use a python virtualenv:

```bash
/usr/bin/python3 -m venv venv
source venv/bin/activate
pip install league-bot
DISCORD_TOKEN=discord_token_of_your_bot
league-bot
```

A [systemd](https://en.wikipedia.org/wiki/Systemd) unit can be used
to configure the bot as a system service:

```ini
[Unit]
Description=league-bot
After=network-online.target

[Service]
Type=simple
Restart=always
WorkingDirectory=directory_where_krcg_is_installed
Environment=DISCORD_TOKEN=discord_token_of_your_bot
ExecStart=/bin/bash -c 'source venv/bin/activate && league-bot'

[Install]
WantedBy=multi-user.target
```

For development, the environment variable `DISCORD_TOKEN` can be provided
by a personal `.env` file at the root of the league-bot folder (ignored by git):

```bash
export DISCORD_TOKEN="discord_token_of_your_bot"
```
