"""Monitor Telegram channels for new messages.

This script uses the Telethon library to connect to the Telegram API and
iterate through messages in configured channels.  New messages are
inserted into the SQLite database using helper functions from
``app.database``.  Because Telethon is asynchronous, the monitoring
function runs inside an event loop.

Refer to Telethon’s documentation for details on `iter_messages`, which
allows iterating over messages in a chat or channel【78046585748960†L3020-L3044】.
"""

import asyncio
import argparse
from datetime import datetime
from typing import Dict, Any

from telethon import TelegramClient

from .config import load_config
from .database import init_db, insert_message


async def monitor_telegram(config: Dict[str, Any]) -> None:
    """Monitor configured Telegram channels and store messages.

    This function connects to Telegram using the API credentials from the
    configuration, then iterates over a limited number of recent messages
    from each channel.  Messages without text are skipped.  Each message
    is inserted into the database with the current timestamp if the
    message’s date attribute is missing.

    Parameters
    ----------
    config : Dict[str, Any]
        Configuration dictionary loaded from YAML.
    """
    telegram_conf = config.get("telegram", {})
    api_id = telegram_conf.get("api_id")
    api_hash = telegram_conf.get("api_hash")
    session_name = telegram_conf.get("session_name", "session")
    channels = telegram_conf.get("channels", [])
    db_path = config.get("database", {}).get("path", "data/news.db")

    conn = init_db(db_path)

    # Use context manager to ensure the client disconnects properly
    async with TelegramClient(session_name, api_id, api_hash) as client:
        for channel in channels:
            try:
                # Iterate over recent messages using Telethon’s iter_messages【78046585748960†L3020-L3044】.
                async for message in client.iter_messages(channel, limit=50):
                    # Skip messages without text
                    if not getattr(message, "text", None):
                        continue
                    timestamp = (
                        message.date.strftime("%Y-%m-%d %H:%M:%S")
                        if getattr(message, "date", None)
                        else datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                    )
                    data = {
                        "source": "telegram",
                        "channel": str(channel),
                        # Use message ID as the title for reference
                        "title": str(message.id),
                        "content": message.text,
                        "url": "",  # Telegram messages do not have a direct URL by default
                        "date": timestamp,
                    }
                    insert_message(conn, data)
            except Exception as exc:
                # Log errors but continue with other channels
                print(f"Error processing channel {channel}: {exc}")

    conn.close()


def main() -> None:
    """CLI entry point for the Telegram monitor."""
    parser = argparse.ArgumentParser(description="Monitor Telegram channels for news")
    parser.add_argument(
        "--config",
        default="config.yaml",
        help="Path to the YAML configuration file",
    )
    args = parser.parse_args()
    config = load_config(args.config)
    asyncio.run(monitor_telegram(config))


if __name__ == "__main__":
    main()