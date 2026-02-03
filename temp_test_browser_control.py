from googlemapstew_plugin.browser_control import initialize_browser, close_browser
import time

def test_browser_initialization():
    driver = None
    try:
        print("Attempting to initialize browser...")
        driver = initialize_browser()
        print("Browser initialized successfully. Current URL:", driver.current_url)
        # Give it a moment to ensure Google Maps loads fully
        time.sleep(5)
        print("Test successful: Browser opened headless and navigated to Google Maps.")
    except Exception as e:
        print(f"Test failed: An error occurred - {e}")
    finally:
        if driver:
            print("Attempting to close browser...")
            close_browser(driver)
            print("Browser closed.")
        else:
            print("No driver to close as initialization failed.")

if __name__ == "__main__":
    test_browser_initialization()
