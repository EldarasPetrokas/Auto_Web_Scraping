from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import logging
from logging.handlers import RotatingFileHandler
import time
import os

# Configure logging with rotation
log_handler = RotatingFileHandler(
    "web_scrapers.log", maxBytes=10 * 1024 * 1024, backupCount=5  # 10MB per file, keep 5 backups
)
logging.basicConfig(
    level=logging.INFO,  # Only log warnings and errors
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        log_handler,  # Rotate logs
        logging.StreamHandler()  # Console logs
    ]
)


def fetch_blocket_ads(urls):
    """
    Fetch the first 40 ads from Blocket.se for each URL.

    Returns:
        list: A list of dictionaries containing ad details.
    """

    # Use environment variables for paths
    chromium_binary_path = os.getenv("CHROMIUM_BINARY_PATH", "/opt/homebrew/bin/chromium")
    chromedriver_path = os.getenv("CHROMEDRIVER_PATH", "/Users/eldaras/Desktop/chromedriver-mac-arm64/chromedriver")

    service = Service(chromedriver_path)

    # Set Chrome options to optimize performance
    chrome_options = Options()
    chrome_options.binary_location = chromium_binary_path
    chrome_options.add_argument("--headless")  # Set to "--headless=new" if supported for newer Chromium
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-cache")  # Disable cache
    chrome_options.add_argument("--disable-application-cache")
    chrome_options.add_argument("--disk-cache-size=0")
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")  # Recommended for performance
    prefs = {"profile.managed_default_content_settings.images": 2}  # Disable images
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    all_ads = []

    for base_url in urls:

        logging.info(f"Starting to scrape URL: {base_url}")

        try:
            driver.get(base_url)

            # Wait for the ads to load
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "list"))
                )
                time.sleep(2)  # Ensure the page fully loads
            except Exception as load_error:
                logging.warning(f"Failed to load ads for URL: {base_url}. Error: {load_error}")
                continue

            # Parse the page source with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract ad details
            ads = soup.select("a.animate-fadein")  # Ensure 40 ads are scraped
            for ad in ads:
                try:
                    link = ad['href'] if ad.has_attr('href') else "N/A"
                    title_element = ad.find("h2")
                    name = title_element.text.strip() if title_element else "N/A"
                    price_element = ad.find("div", {"data-cy": "price"})
                    price = price_element.text.strip() if price_element else "N/A"
                    year_element = ad.find("div", string=lambda text: text and text.isdigit() and len(text) == 4)
                    year = year_element.text.strip() if year_element else "N/A"

                    if name != "N/A" and price != "N/A" and year != "N/A":
                        all_ads.append({
                            'link': f"https://www.blocket.se{link}" if link.startswith('/') else link,
                            'name': name,
                            'year': year,
                            'price': price
                        })
                except Exception as ad_error:
                    logging.warning(f"Error processing Blocket ad: {ad_error}")
                    continue

        except Exception as page_error:
            logging.error(f"Error scraping Blocket page {base_url}: {page_error}")
            continue

    logging.info(f"Scraping complete. Total ads fetched: {len(all_ads)}")
    driver.quit()
    return all_ads
