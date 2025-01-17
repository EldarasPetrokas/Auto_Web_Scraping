from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import logging
from logging.handlers import RotatingFileHandler

# Configure logging with rotation
log_handler = RotatingFileHandler(
    "web_scrapers.log", maxBytes=10 * 1024 * 1024, backupCount=5  # 10MB per file, keep 5 backups
)
logging.basicConfig(
    level=logging.INFO,  # Adjust to WARNING for even fewer logs
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        log_handler,  # Rotate logs
        logging.StreamHandler()  # Console logs
    ]
)


def fetch_otomoto_ads(driver, urls):
    """
    Fetch ads from multiple Otomoto URLs and return their details.

    Args:
        driver: Selenium WebDriver instance.
        urls: List of URLs to scrape.

    Returns:
        list: A list of dictionaries containing ad details.
    """

    all_ads = []

    for url in urls:

        logging.info(f"Starting to scrape URL: {url}")

        try:
            driver.get(url)

            # Wait for the main container with ads to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='search-results']"))
            )

            # Parse the page source with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Select the ad containers
            ad_containers = soup.select("div[data-testid='search-results'] article")

            # Extract ad details
            for ad in ad_containers:
                try:
                    # Extract link
                    link_tag = ad.find("a", href=True)
                    link = link_tag["href"] if link_tag else "N/A"

                    # Extract name
                    name_tag = ad.select_one("h2.e1n1d04s0 a")
                    name = name_tag.text.strip() if name_tag else "N/A"

                    # Extract year
                    year_tag = ad.select_one("dd[data-parameter='year']")
                    year = year_tag.text.strip() if year_tag else "N/A"

                    # Extract price
                    price_element = ad.select_one("div[class='ooa-2p9dfw e6r213i0'] h3")
                    price = f"{price_element.text.strip()} PLN" if price_element else "N/A"

                    # Include only ads with complete details
                    if name != "N/A" and year != "N/A" and price != "N/A":
                        all_ads.append({
                            'link': f"https://www.otomoto.pl{link}" if link.startswith("/") else link,
                            'name': name,
                            'year': year,
                            'price': price
                        })
                except Exception as ad_error:
                    logging.warning(f"Error processing Otomoto ad: {ad_error}")
                    continue  # Skip problematic ads
        except Exception as page_error:
            logging.error(f"Error scraping Otomoto page: {page_error}")
            continue  # Skip problematic pages

    logging.info(f"Scraping complete. Total ads fetched: {len(all_ads)}")
    return all_ads
