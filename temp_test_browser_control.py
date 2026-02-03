from googlemapstew_plugin.browser_control import initialize_browser, close_browser, search
import time

if __name__ == "__main__":
    driver = None
    try:
        driver = initialize_browser()
        search(driver, "restaurants in New York")
        time.sleep(5) # Give some time to see the browser before closing if not headless
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if driver:
            close_browser(driver)