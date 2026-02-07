from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

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

def perform_gmaps_search(driver, query):
    """
    Performs a search on Google Maps for a given query.
    Returns True if search is successful, False otherwise.
    """
    try:
        # Wait for the search input field to be present using its 'name' attribute
        search_input = driver.find_element(By.NAME, "q")
        search_input.send_keys(query)
        print(f"Typed '{query}' into the search box.")
        time.sleep(2) # Give some time for suggestions to load, if any

        # Find and click the search button
        search_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Search']")
        search_button.click()
        print("Clicked the search button.")
        time.sleep(5) # Wait for search results to load
        return True
    except Exception as e:
        print(f"An error occurred during search: {e}")
        return False

def get_page_html(driver):
    """
    Returns the full HTML source of the current page.
    """
    return driver.page_source
