from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

def get_chrome_driver():
    """
    Initialize and return a configured Chrome WebDriver instance with custom Chromium settings.
    """
    chromium_binary_path = os.getenv("CHROMIUM_BINARY_PATH", "/opt/homebrew/bin/chromium")
    chromedriver_path = os.getenv("CHROMEDRIVER_PATH", "/Users/eldaras/Desktop/chromedriver-mac-arm64/chromedriver")

    service = Service(chromedriver_path)

    # Set Chrome options to optimize performance
    chrome_options = Options()
    chrome_options.binary_location = chromium_binary_path
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-cache")
    chrome_options.add_argument("--disable-application-cache")
    chrome_options.add_argument("--disk-cache-size=0")
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-logging")  # Suppress logs
    chrome_options.add_argument("--no-sandbox")  # Recommended for performance

    # Preferences to disable images and JavaScript
    prefs = {
        "profile.managed_default_content_settings.images": 2,  # Disable images
        "profile.default_content_setting_values.javascript": 2,  # Disable JavaScript
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # Set a custom user agent
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/96.0.4664.110 Safari/537.36"
    )

    # Return the configured WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver
