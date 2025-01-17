import asyncio
import time
import os
import json
from scrapers.autoplius import fetch_autoplius_ads
from scrapers.auto24 import fetch_auto24_ads
from scrapers.blocket import fetch_blocket_ads
from scrapers.otomoto import fetch_otomoto_ads
from scrapers.autogidas import fetch_autogidas_ads
from scrapers.SS import fetch_ss_ads
from database.database import init_db, save_to_database
from telegram_bot.bot import send_to_telegram
from scrapers.chromium_driver import get_chrome_driver


def load_config():
    """Loads configuration from a JSON file."""
    config_file = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_file, "r") as file:
        return json.load(file)


def main():

    while True:

        config = load_config()

        # Step 1: Initialize the database
        print("Initializing the database...")
        init_db()  # Ensure the database is initialized
        print("Database initialized.")

        # Step 2: Fetch ads from all sources and measure time
        print("Fetching ads from all sources...")
        start_time = time.time()  # Start the timer

        driver = get_chrome_driver()

        ads = fetch_autoplius_ads(driver, config["autoplius_urls"])  # Fetch Autoplius ads

        ads.extend(fetch_auto24_ads(driver, config["auto24_urls"]))  # Combine results from Auto24

        ads.extend(fetch_otomoto_ads(driver, config["otomoto_urls"]))  # Combine results from Otomoto

        ads.extend(fetch_autogidas_ads(driver, config["autogidas_urls"]))  # Combine results from Autogidas

        ads.extend(fetch_ss_ads(driver, config["ss_urls"]))  # Combine results from SS

        driver.quit()

        ads.extend(fetch_blocket_ads(config["blocket_urls"]))

        end_time = time.time()  # End the timer

        print(f"Total number of ads fetched: {len(ads)}")
        print(f"Scraping completed in {end_time - start_time:.2f} seconds.")  # Print the elapsed time

        # Step 3: Save ads to the database
        save_to_database(ads)

        # Step 4: Send new ads to Telegram
        asyncio.run(send_to_telegram())  # Run the async function in an event loop

        time.sleep(30)


if __name__ == "__main__":
    main()
