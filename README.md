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
- Google Chrome browser
- ChromeDriver (compatible with your Chrome version)

## Installation
Clone the repository:
git clone https://github.com/EldarasPetrokas/Auto_Web_Scraping.git
cd dynamic-car-ads-scraper
   
## Install dependencies
pip install -r requirements.txt
Configure your config.json file:

## Add your Telegram bot token and chat ID.
Include the URLs for the websites you want to scrape.
{
    "telegram_bot_token": "YOUR_TELEGRAM_BOT_TOKEN",
    "telegram_chat_id": "YOUR_TELEGRAM_CHAT_ID",
    "ss_urls": [
        "https://www.ss.com/en/transport/cars/toyota/land-cruiser/today/sell/",
        "https://www.ss.com/lv/transport/cars/toyota/hilux/today/sell/"
    ],
  
}

## Start the scraper
python main.py
Usage

## Run the scraper continuously: To run the scraper in a loop with a 30-second interval, modify main.py to include
import time
while True:
    try:
        main()
        time.sleep(30)
    except KeyboardInterrupt:
        break
.