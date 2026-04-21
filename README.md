# Discord Keyword Alert Bot

A simple Discord bot that watches server messages for keywords and logs alerts when a match is found.

This project is a small companion utility for **Upsteered**:
https://upsteered.com

## What it does

- Monitors Discord messages in servers where the bot is installed
- Detects keywords or phrases from `keywords.txt`
- Logs matches to the console
- Optionally posts alerts to a private Discord channel

## Files

- `bot.py` — bot logic
- `keywords.txt` — keywords and phrases to monitor
- `requirements.txt` — Python dependencies
- `.gitignore` — files not to commit
- `.env.example` — environment variable example

## Setup

1. Create a Discord application in the Discord Developer Portal.
2. Add a bot user.
3. Enable **Message Content Intent** in the bot settings.
4. Invite the bot to your server with the permissions it needs.
5. Install dependencies:

```bash
pip install -r requirements.txt
