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

def fetch_auto24_ads(driver, urls):
    """
    Fetch ads from multiple Auto24 URLs and all available pages for each URL.

    Returns:
        list: A list of dictionaries containing ad details.
    """

    all_ads = []

    for base_url in urls:

        logging.info(f"Starting to scrape URL: {base_url}")

        try:
            driver.get(base_url)

            # Wait for the ads to load (reduce timeout to 5 seconds)
            WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "result-row"))
            )

            # Parse the page source with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Select ad containers once
            ad_links = soup.select('div.result-row a.main')  # Using CSS selectors

            for ad in ad_links:
                try:
                    # Extract link
                    link = ad['href'] if ad.has_attr('href') else "N/A"
                    if "/rent/" in link:  # Exclude rental ads
                        continue

                    # Extract name
                    brand = ad.find('span').text.strip()
                    model = ad.find('span', class_='model').text.strip()
                    name = f"{brand} {model}"

                    # Extract price
                    price = ad.find_next('span', class_='price').text.strip()

                    # Extract year
                    year = ad.find_next('span', class_='year').text.strip()

                    # Append the ad to the list
                    if name and price and year:
                        all_ads.append({
                            'link': f"https://eng.auto24.ee{link}" if link.startswith('/') else link,
                            'name': name,
                            'year': year,
                            'price': price
                        })
                except Exception as ad_error:
                    logging.warning(f"Error processing Auto24 ad: {ad_error}")
                    continue  # Skip problematic ads
        except Exception as page_error:
            logging.error(f"Error scraping Auto24 page: {page_error}")
            continue # Skip problematic pages

    logging.info(f"Scraping complete. Total ads fetched: {len(all_ads)}")
    return all_ads
