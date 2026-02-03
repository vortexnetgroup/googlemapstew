from googlemapstew_plugin.browser_control import initialize_browser, searchgmaps
import time

def run_test_searchgmaps():
    print("Starting test for searchgmaps function...")
    driver = None
    try:
        driver = initialize_browser()
        if driver:
            searchgmaps(driver, "McDonald's") # Using McDonald's for a more consistent test case
            print("Searchgmaps test completed.")
        else:
            print("Failed to initialize browser.")
    except Exception as e:
        print(f"An error occurred during the test: {e}")
    finally:
        # The searchgmaps function already closes the browser, so no need to close here.
        pass

if __name__ == "__main__":
    run_test_searchgmaps()