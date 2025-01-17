from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def test_chrome_driver():
    service = Service("/usr/bin/chromedriver")
    options = Options()
    options.binary_location = "/usr/bin/chromium-browser"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://example.com")
    print(driver.title)
    driver.quit()


test_chrome_driver()
