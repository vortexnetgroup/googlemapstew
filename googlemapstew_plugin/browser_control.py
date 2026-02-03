from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

def searchgmaps(driver, query):
    """
    Performs a search on Google Maps for a given query.
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
        # Wait for search results to load using explicit wait
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[role="article"].Nv2PK.THOPZb.CpccDe'))
        )

        # Find all article elements, each representing a search result
        article_elements = driver.find_elements(By.CSS_SELECTOR, 'div[role="article"].Nv2PK.THOPZb.CpccDe')

        if article_elements:
            print("\nFound places:")
            for i, article_element in enumerate(article_elements):
                place_name = "N/A"
                status = "N/A"
                address = "N/A"

                try:
                    # Extract place name
                    name_element = article_element.find_element(By.CSS_SELECTOR, 'div.qBF1Pd.fontHeadlineSmall')
                    place_name = name_element.text
                except:
                    pass # Name not found for this article

                # Find all 'W4Efsd' divs within the current article, which contain various details
                detail_divs = article_element.find_elements(By.CSS_SELECTOR, 'div.W4Efsd')

                for detail_div in detail_divs:
                    # Check for open/closed status
                    if "Open now" in detail_div.text:
                        status = "Open now"
                    elif "Closed" in detail_div.text:
                        status = detail_div.text.strip()
                    elif "Opens" in detail_div.text:
                        status = detail_div.text.strip()

                    # Heuristic for address:
                    # Look for span elements that are children of W4Efsd.
                    # Address often contains a comma, digits, and is not a rating, status, or simple category.
                    spans_in_detail_div = detail_div.find_elements(By.TAG_NAME, 'span')
                    for span in spans_in_detail_div:
                        span_text = span.text.strip()
                        if "," in span_text and \
                           "star" not in span_text and "Reviews" not in span_text and \
                           "Open" not in span_text and "Closed" not in span_text and \
                           not span_text.isdigit() and len(span_text) > 5 and \
                           "hotel" not in span_text.lower() and \
                           "restaurant" not in span_text.lower() and \
                           "food" not in span_text.lower() and \
                           "brewpub" not in span_text.lower() and \
                           "ferry" not in span_text.lower() and \
                           "hardware" not in span_text.lower():
                            address = span_text
                            break

                print(f"{i+1}. Name: {place_name}")
                print(f"   Status: {status}")
                print(f"   Address: {address}")

        else:
            print("\nNo places found on the page.")

    except Exception as e:
        print(f"An error occurred during search: {e}")
    finally:
        close_browser(driver)
