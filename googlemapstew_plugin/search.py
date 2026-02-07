from selenium.webdriver.common.by import By
from .browser_control import initialize_browser, close_browser, perform_gmaps_search, get_page_html
from selenium.webdriver.remote.webelement import WebElement
import time

def search_restaurants(query: str) -> list[str]:
    """
    Searches Google Maps for restaurants based on the query and returns a list of restaurant names.
    """
    driver = None
    restaurant_names = []
    try:
        driver = initialize_browser()
        if perform_gmaps_search(driver, query):
            print(f"Search for '{query}' successful. Extracting restaurant names...")
            # Wait for results to load
            time.sleep(3) 

            # Find all potential result containers
            # The user specified to avoid class IDs as they can change.
            # Using 'role="article"' to identify individual place listings.
            result_containers = driver.find_elements(By.CSS_SELECTOR, 'div[role="article"]')

            if result_containers:
                for container in result_containers:
                    try:
                        # Within each container, find the restaurant name
                        # Based on the provided HTML, the restaurant name is within a div with these classes.
                        name_element: WebElement = container.find_element(By.CSS_SELECTOR, 'div.qBF1Pd.fontHeadlineSmall')
                        if name_element:
                            restaurant_names.append(name_element.text)
                    except Exception as e:
                        print(f"Could not extract name from a result container: {e}")
            else:
                print("No result containers found with role='article'.")
        else:
            print(f"Failed to perform search for '{query}'.")

    except Exception as e:
        print(f"An error occurred during restaurant search: {e}")
    finally:
        if driver:
            close_browser(driver)
    return restaurant_names
