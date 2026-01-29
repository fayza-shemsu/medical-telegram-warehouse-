import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto

# -------------------------
# Environment & Config
# -------------------------

load_dotenv()

API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")

CHANNELS = [
    "lobelia4cosmetics",
    "tikvahpharma",
    "CheMedTelegramChannel"  # replace with actual username
]

RAW_DATA_DIR = "data/raw/telegram_messages"
IMAGE_DIR = "data/raw/images"
LOG_DIR = "logs"

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

# -------------------------
# Logging Configuration
# -------------------------

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "scraper.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------------
# Helper Functions
# -------------------------

def save_json(data, date_str, channel_name):
    date_path = os.path.join(RAW_DATA_DIR, date_str)
    os.makedirs(date_path, exist_ok=True)

    file_path = os.path.join(date_path, f"{channel_name}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    logging.info(f"Saved {len(data)} messages for {channel_name} on {date_str}")


def download_image(client, message, channel_name):
    channel_image_dir = os.path.join(IMAGE_DIR, channel_name)
    os.makedirs(channel_image_dir, exist_ok=True)

    image_path = os.path.join(channel_image_dir, f"{message.id}.jpg")
    client.download_media(message.media, image_path)

    return image_path


# -------------------------
# Main Scraping Logic
# -------------------------

async def scrape_channel(client, channel_name):
    logging.info(f"Started scraping channel: {channel_name}")

    messages_by_date = {}

    async for message in client.iter_messages(channel_name):
        if not message.date:
            continue

        date_str = message.date.strftime("%Y-%m-%d")

        if date_str not in messages_by_date:
            messages_by_date[date_str] = []

        message_data = {
            "message_id": message.id,
            "channel_name": channel_name,
            "message_date": message.date.isoformat(),
            "message_text": message.text,
            "views": message.views,
            "forwards": message.forwards,
            "has_media": message.media is not None,
            "image_path": None
        }

        if isinstance(message.media, MessageMediaPhoto):
            try:
                image_path = download_image(client, message, channel_name)
                message_data["image_path"] = image_path
            except Exception as e:
                logging.error(f"Failed to download image {message.id}: {e}")

        messages_by_date[date_str].append(message_data)

    for date_str, msgs in messages_by_date.items():
        save_json(msgs, date_str, channel_name)

    logging.info(f"Finished scraping channel: {channel_name}")


# -------------------------
# Entry Point
# -------------------------

async def main():
    async with TelegramClient("telegram_scraper", API_ID, API_HASH) as client:
        for channel in CHANNELS:
            try:
                await scrape_channel(client, channel)
            except Exception as e:
                logging.error(f"Error scraping {channel}: {e}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
