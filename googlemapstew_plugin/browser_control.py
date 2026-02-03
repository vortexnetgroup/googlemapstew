from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def initialize_browser():
    """
    Initializes a headless Chrome browser, installs the necessary Chrome driver,
    navigates to Google Maps, and returns the WebDriver instance.
    """
    # Setup Chrome options for headless mode
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080") # Set a default window size

    # Auto-download and setup the Chrome driver
    driver_path = ChromeDriverManager().install()
    service = ChromeService(executable_path=driver_path)

    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Navigate to Google Maps
    driver.get("https://www.google.com/maps")

    print("Browser initialized and navigated to Google Maps.")

    return driver

def close_browser(driver):
    """
    Closes the provided WebDriver instance.
    """
    if driver:
        driver.quit()
        print("Browser closed.")
