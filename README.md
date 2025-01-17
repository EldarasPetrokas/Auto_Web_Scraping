# Dynamic Car Ads Scraper

Dynamic Car Ads Scraper is a Python-based project designed to scrape car advertisements from various websites and send notifications for new ads via Telegram. This tool helps you monitor new car ads in real-time and manage them efficiently using a SQLite database.

## Features
- Scrapes ads from multiple websites including:
  - SS.com
  - AutoPlius
  - Auto24
  - Blocket
  - OtoMoto
  - AutoGidas
- Sends notifications for new ads to a Telegram bot.
- Maintains a SQLite database to store and manage ads.
- Automatically skips duplicate ads and deletes old ads.

## Requirements
- Python 3.8 or higher
- Chromium browser (Can be done with Google Chrome but it will significantly slower)
- ChromeDriver (compatible with your Chrome version)

## Installation
- Clone the repository:
- git clone https://github.com/EldarasPetrokas/Auto_Web_Scraping.git

   
## Install dependencies
- pip install -r requirements.txt

## Configure your config.json file:
- Add your Telegram bot token and chat ID.
- Include the URLs for the websites you want to scrape, and Telegram bot and chat info
"telegram_bot_token": "YOUR_TELEGRAM_BOT_TOKEN",
"telegram_chat_id": "YOUR_TELEGRAM_CHAT_ID",
    "ss_urls": [
        "https://www.ss.com/en/transport/cars/toyota/land-cruiser/today/sell/",
        "https://www.ss.com/lv/transport/cars/toyota/hilux/today/sell/"
    ],
- All of this can be done with flask frontend just run flask_app.py and open local server

## Start the scraper python main.py
- Scraper runs continuously in a loop with a 30-second interval, modify main.py time.sleep() if you want to edit the loop interval.
