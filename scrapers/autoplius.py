import logging
from logging.handlers import RotatingFileHandler
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

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

def fetch_autoplius_ads(driver, urls):
    """
    Fetch ads from multiple Autoplius URLs and all available pages for each URL.

    Returns:
        list: A list of dictionaries containing ad details.
    """

    all_ads = []

    for base_url in urls:
        current_url = base_url  # Start with the base URL
        logging.info(f"Starting to scrape URL: {base_url}")

        while True:
            try:
                driver.get(current_url)

                # Wait for the ads to load (reduce timeout to 5 seconds)
                WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "auto-lists"))
                )

                # Parse the page source with BeautifulSoup
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                # Select ad containers
                ad_links = soup.select('div.auto-lists.lt a')  # Using CSS selectors

                if not ad_links:
                    logging.info("No ads found on this page. Stopping pagination.")
                    break

                # Extract ad details
                for ad in ad_links:
                    try:
                        link = ad['href'] if ad.has_attr('href') else "N/A"
                        name = ad.find('div', class_='announcement-title').text.strip() if ad.find(
                            'div', class_='announcement-title') else "N/A"
                        year = ad.find('div', class_='announcement-title-parameters').find(
                            'span').text.strip() if ad.find(
                            'div', class_='announcement-title-parameters') else "N/A"
                        price = ad.find('div', class_='announcement-pricing-info').find(
                            'strong').text.strip() if ad.find(
                            'div', class_='announcement-pricing-info') else "N/A"

                        # Exclude ads with "N/A" for name, year, or price
                        if name != "N/A" and year != "N/A" and price != "N/A":
                            all_ads.append({
                                'link': f"https://autoplius.lt{link}" if link.startswith('/') else link,  # Ensure full URL
                                'name': name,
                                'year': year,
                                'price': price
                            })
                    except Exception:
                        continue  # Skip problematic ads

                # Find the "Next page" button
                next_button = soup.select_one('a.next')
                if next_button and 'href' in next_button.attrs:
                    current_url = f"https://autoplius.lt{next_button['href']}"  # Update the URL for the next page
                else:
                    break
            except Exception as page_error:
                logging.error(f"Error scraping {current_url}: {page_error}")
                break

    logging.info(f"Scraping complete. Total ads fetched: {len(all_ads)}")
    return all_ads
