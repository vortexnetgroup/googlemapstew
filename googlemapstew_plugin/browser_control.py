from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def initialize_browser():
    """
    Initializes a headless Chrome browser, installs the necessary Chrome driver,
    navigates to Google Maps, and returns the WebDriver instance.
    """
    # Setup Chrome options
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")  # Run Chrome in headless mode
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

    # Wait until the search input field is present and clickable
    search_input_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "UGojuc"))
    )

    print("Browser initialized and navigated to Google Maps.")

    return driver

def search(driver, query):
    """
    Performs a search on Google Maps using the provided query.
    Clicks the search textbox, types the query, presses Enter,
    waits for results, and then prints the names of the places found.
    """
    try:
        print("Attempting to find search input...")
        # Find the search input element
        search_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "UGojuc"))
        )
        print("Search input found.")

        # Click the search input to ensure it's active
        search_input.click()
        print("Search input clicked.")

        # Type the query into the search input
        search_input.send_keys(query)
        print(f"Typed query: {query}")

        # Simulate pressing Enter to submit the search
        search_input.send_keys(Keys.ENTER)
        print("Enter key pressed.")

        print(f"Searching for: {query}")

        # Wait for the results to load.
        # Looking for a div with role="article" and class "Nv2PK" which appears in the results.
        print("Waiting for search results to load...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='article'].Nv2PK"))
        )
        print("Search results loaded.")

        # Wait for 3 seconds as requested
        time.sleep(3)

        # Find all place name elements
        place_name_elements = driver.find_elements(By.CSS_SELECTOR, "div.qBF1Pd.fontHeadlineSmall")

        if place_name_elements:
            print("\nFound places:")
            for i, element in enumerate(place_name_elements):
                print(f"{i+1}. {element.text}")
        else:
            print("\nNo places found for the given query.")

    except Exception as e:
        print(f"An error occurred during search: {e}")

def close_browser(driver):
    """
    Closes the provided WebDriver instance.
    """
    if driver:
        driver.quit()
        print("Browser closed.")
