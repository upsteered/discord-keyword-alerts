"""
discord-keyword-alert-bot

A small Discord bot that watches message content for configured keywords
and logs alerts to the console. Optionally, it can also post alerts to a
designated Discord channel.

Use only in servers you own or have permission to monitor.

Environment variables:
- TOKEN (required): Discord bot token
- ALERT_CHANNEL_ID (optional): channel ID to receive alerts
"""

from __future__ import annotations

import asyncio
import logging
import os
import re
from pathlib import Path
from typing import Optional

import discord

# -----------------------------
# Logging
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("discord-keyword-alert-bot")

# -----------------------------
# Config
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
KEYWORDS_FILE = BASE_DIR / "keywords.txt"

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("Missing TOKEN environment variable.")

ALERT_CHANNEL_ID_RAW = os.getenv("ALERT_CHANNEL_ID", "").strip()
ALERT_CHANNEL_ID = int(ALERT_CHANNEL_ID_RAW) if ALERT_CHANNEL_ID_RAW.isdigit() else None

# -----------------------------
# Keyword loading
# -----------------------------
def load_keywords(path: Path) -> list[str]:
    """
    Load keywords from a text file.
    One keyword or phrase per line.
    Blank lines and lines starting with '#' are ignored.
    """
    if not path.exists():
        raise FileNotFoundError(f"Keyword file not found: {path}")

    keywords: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        item = line.strip()
        if not item or item.startswith("#"):
            continue
        keywords.append(item)

    if not keywords:
        raise ValueError(f"No keywords found in {path}")

    return keywords


def compile_patterns(keywords: list[str]) -> list[tuple[str, re.Pattern[str]]]:
    """
    Compile case-insensitive whole-word-ish patterns for each keyword.
    This reduces false positives compared with a raw substring match.
    """
    patterns: list[tuple[str, re.Pattern[str]]] = []
    for keyword in keywords:
        # Works well for single words and short phrases.
        pattern = re.compile(rf"(?<!\w){re.escape(keyword)}(?!\w)", re.IGNORECASE)
        patterns.append((keyword, pattern))
    return patterns


def find_matching_keyword(message_content: str, patterns: list[tuple[str, re.Pattern[str]]]) -> Optional[str]:
    """Return the first matching keyword, or None."""
    for keyword, pattern in patterns:
        if pattern.search(message_content):
            return keyword
    return None


# Load keywords at startup
KEYWORDS = load_keywords(KEYWORDS_FILE)
PATTERNS = compile_patterns(KEYWORDS)
logger.info("Loaded %d keywords from %s", len(KEYWORDS), KEYWORDS_FILE.name)

# -----------------------------
# Discord setup
# -----------------------------
intents = discord.Intents.default()
intents.message_content = True  # Must also be enabled in the Discord Developer Portal
client = discord.Client(intents=intents)


async def send_alert(destination: discord.abc.Messageable, *, keyword: str, message: discord.Message) -> None:
    """Send an alert message to a Discord channel."""
    guild_name = message.guild.name if message.guild else "DM"
    channel_name = f"#{message.channel.name}" if hasattr(message.channel, "name") else "unknown"
    content = message.content.replace("```", "ˋˋˋ")  # keep formatting safe

    alert_text = (
        "🚨 **Keyword Alert**\n"
        f"**Keyword:** `{keyword}`\n"
        f"**Server:** {guild_name}\n"
        f"**Channel:** {channel_name}\n"
        f"**User:** {message.author}\n"
        f"**Message:** {content}"
    )

    await destination.send(alert_text)


@client.event
async def on_ready() -> None:
    logger.info("Logged in as %s (ID: %s)", client.user, client.user.id if client.user else "unknown")
    if ALERT_CHANNEL_ID:
        logger.info("Alert channel enabled: %s", ALERT_CHANNEL_ID)


@client.event
async def on_message(message: discord.Message) -> None:
    # Ignore our own messages and other bots
    if message.author.bot:
        return

    # Ignore DMs; monitor server messages only
    if message.guild is None:
        return

    content = message.content.strip()
    if not content:
        return

    matched_keyword = find_matching_keyword(content, PATTERNS)
    if not matched_keyword:
        return

    logger.info(
        "MATCH | keyword=%r | user=%s | guild=%s | channel=%s | content=%r",
        matched_keyword,
        message.author,
        message.guild.name,
        getattr(message.channel, "name", "unknown"),
        content,
    )

    # Optional alert channel
    if ALERT_CHANNEL_ID:
        channel = client.get_channel(ALERT_CHANNEL_ID)
        if channel is None:
            try:
                channel = await client.fetch_channel(ALERT_CHANNEL_ID)
            except discord.NotFound:
                logger.warning("Alert channel not found: %s", ALERT_CHANNEL_ID)
                channel = None
            except discord.Forbidden:
                logger.warning("No permission to access alert channel: %s", ALERT_CHANNEL_ID)
                channel = None

        if channel is not None:
            try:
                await send_alert(channel, keyword=matched_keyword, message=message)
            except discord.DiscordException as exc:
                logger.warning("Failed to send alert message: %s", exc)


def main() -> None:
    """Entry point."""
    client.run(TOKEN)


if __name__ == "__main__":
    main()
