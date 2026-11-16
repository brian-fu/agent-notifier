"""Small Telegram Bot API client for one-way phone notifications."""

import argparse
import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parent / ".env")


def telegram(method: str, payload: dict) -> dict | list:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

    request = Request(
        f"https://api.telegram.org/bot{token}/{method}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urlopen(request, timeout=15) as response:
            data = json.load(response)
    except HTTPError as error:
        try:
            description = json.load(error).get("description", "Request rejected")
        except (ValueError, OSError):
            description = "Request rejected"
        raise RuntimeError(f"Telegram HTTP {error.code}: {description}") from None
    except URLError:
        raise RuntimeError("Could not connect to Telegram") from None

    if not data.get("ok"):
        raise RuntimeError(data.get("description", "Telegram rejected the request"))
    return data["result"]


def get_chat_id() -> int:
    """Find the most recent private /start message sent to this bot."""
    updates = telegram("getUpdates", {"limit": 100})
    for update in reversed(updates):
        message = update.get("message") or {}
        chat = message.get("chat") or {}
        if chat.get("type") == "private" and message.get("text", "").startswith("/start"):
            return chat["id"]
    raise RuntimeError("No /start found. Send /start to your bot and try again.")


def send_message(text: str) -> None:
    """Send one message to the single chat configured by the owner."""
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    if not chat_id:
        raise RuntimeError("TELEGRAM_CHAT_ID is not set")
    if not text.strip() or len(text) > 4096:
        raise ValueError("Message must contain 1 to 4096 characters")
    telegram("sendMessage", {"chat_id": chat_id, "text": text})


def main() -> None:
    parser = argparse.ArgumentParser(description="Send a Telegram phone notification")
    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("chat-id", help="Find your private chat ID after /start")
    send = subcommands.add_parser("send", help="Send a test message")
    send.add_argument("text")
    args = parser.parse_args()
    try:
        if args.command == "chat-id":
            print(get_chat_id())
        else:
            send_message(args.text)
            print("Sent")
    except (RuntimeError, ValueError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
