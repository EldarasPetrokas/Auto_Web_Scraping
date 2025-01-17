import asyncio
import json
import os
from telegram import Bot
from database.database import get_unsent_ads, mark_as_sent

# Dynamically resolve the path to config.json
CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")


def load_config():
    """Load configuration from the config.json file."""
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)


async def send_to_telegram():
    """Send unsent ads to Telegram and mark them as sent."""
    config = load_config()
    bot_token = config.get("telegram_bot_token")
    chat_id = config.get("telegram_chat_id")

    if not bot_token or not chat_id:
        print("Telegram bot token or chat ID is missing in the configuration.")
        return

    bot = Bot(token=bot_token)

    # Fetch unsent ads
    unsent_ads = get_unsent_ads()

    if not unsent_ads:
        print("No new ads to send to Telegram.")
        return

    print(f"Sending {len(unsent_ads)} new ads to Telegram...")

    # Send each ad to Telegram
    for index, ad in enumerate(unsent_ads, start=1):
        link, name, year, price = ad
        message = f"Name: {name}\nYear: {year}\nPrice: {price}\nLink: {link}"
        try:
            await bot.send_message(chat_id=chat_id, text=message)
            mark_as_sent(link)  # Mark the ad as sent to Telegram
            print(f"Sent ad to Telegram: {name}")

            # Introduce a delay after every 10 messages
            if index % 10 == 0:
                print("Pausing for 5 seconds to avoid Telegram rate limits...")
                await asyncio.sleep(5)

        except Exception as e:
            print(f"Failed to send message for ad: {name}, Error: {e}")
            continue
