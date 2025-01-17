from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urlparse
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


def extract_name_from_url(url):
    """
    Extract the name of the car from the base URL.

    Args:
        urls (str): The base URL of the page being scraped.

    Returns:
        str: The extracted name of the car.
    """
    try:
        path_segments = urlparse(url).path.split("/")
        if "cars" in path_segments:
            car_index = path_segments.index("cars") + 1
            name_segments = path_segments[car_index:car_index + 2]
            name = " ".join(segment.replace("-", " ").title() for segment in name_segments)
            return name
        return "N/A"
    except Exception as e:
        print(f"Error extracting name from URL: {e}")
        return "N/A"


def fetch_ss_ads(driver, urls):
    """
    Fetch ads from multiple SS.com URLs and return their details.

    Args:
        driver: Selenium WebDriver instance.

    Returns:
        list: A list of dictionaries containing ad details.
        :param driver:
        :param urls:
    """

    all_ads = []
    seen_ads = set()  # Track unique ads by (year, price, link)

    for url in urls:

        logging.info(f"Starting to scrape URL: {url}")

        try:

            driver.get(url)

            # Extract name from the base URL
            name = extract_name_from_url(url)

            # Wait for the main container with ads to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table#page_main tbody"))
            )

            # Parse the page source with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Select rows with ads (excluding headers or unnecessary rows)
            ad_rows = soup.select("table#page_main tr:has(td.msg2)")

            for ad in ad_rows:
                try:
                    # Skip header rows or rows that are not actual ads
                    if 'header' in ad.get('class', []):
                        continue

                    # Extract year
                    year_tag = ad.select_one("td.msga2-o.pp6:nth-of-type(4)")
                    year = year_tag.text.strip() if year_tag else "N/A"

                    # Extract price
                    price_tag = ad.select_one("td.msga2-o.pp6:nth-of-type(7)")
                    price = price_tag.text.strip() if price_tag else "N/A"

                    # Extract link
                    link_tag = ad.select_one("td.msg2 a[href]")
                    link = f"https://www.ss.com{link_tag['href']}" if link_tag else "N/A"

                    # Ensure unique ads by year, price, and link
                    ad_identifier = (year, price, link)
                    if ad_identifier in seen_ads:
                        continue  # Skip duplicate ad

                    seen_ads.add(ad_identifier)

                    # Add to list if all fields are valid
                    if year != "N/A" and price != "N/A" and link != "N/A":
                        all_ads.append({
                            'link': link,
                            'name': name,
                            'year': year,
                            'price': price,
                        })
                except Exception as ad_error:
                    logging.warning(f"Error processing SS.com ad: {ad_error}")
                    continue  # Skip problematic ads

        except Exception as page_error:
            logging.error(f"Error scraping Otomoto page: {page_error}")
            continue  # Skip problematic pages

    logging.info(f"Scraping complete. Total ads fetched: {len(all_ads)}")
    return all_ads
