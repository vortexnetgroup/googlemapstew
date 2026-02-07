import unittest
from unittest.mock import patch, MagicMock
from googlemapstew_plugin.search import search_restaurants
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import time

class TestSearchRestaurants(unittest.TestCase):

    # The HTML snippet provided by the user, simplified for relevant elements
    MOCK_GOOGLE_MAPS_HTML = """
    <div class="m6QErb DxyBCb kA9KIf dS8AEf XiKgde ecceSd " id="156__uuXHif18" style="position: relative;" tabindex="-1">
        <div role="article" class="Nv2PK tH5CWc THOPZb " aria-label="Long John Silver's">
            <div class="bfdHYd Ppzolf OFBs3e">
                <div class="lI9IFe">
                    <div class="y7PRA">
                        <div class="Lui3Od T7Wufd">
                            <div class="Z8fK3b">
                                <div class="UaQhfb fontBodyMedium">
                                    <div class="NrDZNb">
                                        <div class="qBF1Pd fontHeadlineSmall ">Long John Silver's</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div role="article" class="Nv2PK tH5CWc THOPZb " aria-label="John Brooks Supermarket">
            <div class="bfdHYd Ppzolf OFBs3e">
                <div class="lI9IFe">
                    <div class="y7PRA">
                        <div class="Lui3Od T7Wufd">
                            <div class="Z8fK3b">
                                <div class="UaQhfb fontBodyMedium">
                                    <div class="NrDZNb">
                                        <div class="qBF1Pd fontHeadlineSmall ">John Brooks Supermarket</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div role="article" class="Nv2PK Q2HXcd THOPZb " aria-label="John J Mahoney Realtor">
            <div class="bfdHYd Ppzolf OFBs3e">
                <div class="lI9IFe">
                    <div class="y7PRA">
                        <div class="Lui3Od T7Wufd">
                            <div class="Z8fK3b">
                                <div class="UaQhfb fontBodyMedium">
                                    <div class="NrDZNb">
                                        <div class="qBF1Pd fontHeadlineSmall ">John J Mahoney Realtor</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div role="article" class="Nv2PK tH5CWc THOPZb " aria-label="Jimmy John's">
            <div class="bfdHYd Ppzolf OFBs3e">
                <div class="lI9IFe">
                    <div class="y7PRA">
                        <div class="Lui3Od T7Wufd">
                            <div class="Z8fK3b">
                                <div class="UaQhfb fontBodyMedium">
                                    <div class="NrDZNb">
                                        <div class="qBF1Pd fontHeadlineSmall ">Jimmy John's</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div role="article" class="Nv2PK tH5CWc THOPZb " aria-label="St John's Thrift Shop">
            <div class="bfdHYd Ppzolf OFBs3e">
                <div class="lI9IFe">
                    <div class="y7PRA">
                        <div class="Lui3Od T7Wufd">
                            <div class="Z8fK3b">
                                <div class="UaQhfb fontBodyMedium">
                                    <div class="NrDZNb">
                                        <div class="qBF1Pd fontHeadlineSmall ">St John's Thrift Shop</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div role="article" class="Nv2PK tH5CWc THOPZb " aria-label="Cathedral of St John">
            <div class="bfdHYd Ppzolf OFBs3e">
                <div class="lI9IFe">
                    <div class="y7PRA">
                        <div class="Lui3Od T7Wufd">
                            <div class="Z8fK3b">
                                <div class="UaQhfb fontBodyMedium">
                                    <div class="NrDZNb">
                                        <div class="qBF1Pd fontHeadlineSmall ">Cathedral of St John</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div role="article" class="Nv2PK tH5CWc THOPZb " aria-label="Papa Johns Pizza">
            <div class="bfdHYd Ppzolf OFBs3e">
                <div class="lI9IFe">
                    <div class="y7PRA">
                        <div class="Lui3Od T7Wufd">
                            <div class="Z8fK3b">
                                <div class="UaQhfb fontBodyMedium">
                                    <div class="NrDZNb">
                                        <div class="qBF1Pd fontHeadlineSmall ">Papa Johns Pizza</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div role="article" class="Nv2PK tH5CWc THOPZb " aria-label="Long John Silver's">
            <div class="bfdHYd Ppzolf OFBs3e">
                <div class="lI9IFe">
                    <div class="y7PRA">
                        <div class="Lui3Od T7Wufd">
                            <div class="Z8fK3b">
                                <div class="UaQhfb fontBodyMedium">
                                    <div class="NrDZNb">
                                        <div class="qBF1Pd fontHeadlineSmall ">Long John Silver's</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """

    @patch('googlemapstew_plugin.browser_control.initialize_browser')
    @patch('googlemapstew_plugin.browser_control.close_browser')
    @patch('googlemapstew_plugin.browser_control.perform_gmaps_search')
    def test_search_restaurants_success(self, mock_initialize_browser, mock_close_browser, mock_perform_gmaps_search):
        mock_driver = MagicMock()
        mock_initialize_browser.return_value = mock_driver
        mock_perform_gmaps_search.return_value = True

        # Simulate find_elements for the result containers
        # We need to parse the MOCK_GOOGLE_MAPS_HTML to create mock WebElement objects
        # that behave like real Selenium elements.
        
        # This is a bit intricate. We'll create mock elements that can find their children.
        
        # Helper to create a mock WebElement
        def create_mock_element(tag_name, text=None, class_name=None, role=None):
            element = MagicMock(spec=WebElement)
            element.tag_name = tag_name
            element.text = text if text is not None else ""
            
            # Mock find_element for the restaurant name
            def mock_find_element(by, value):
                if by == By.CSS_SELECTOR and value == 'div.qBF1Pd.fontHeadlineSmall':
                    name_mock = MagicMock(spec=WebElement)
                    name_mock.text = text
                    return name_mock
                raise Exception(f"Unexpected find_element call: {by}, {value}")
            
            element.find_element.side_effect = mock_find_element
            return element

        expected_names = [
            "Long John Silver's",
            "John Brooks Supermarket",
            "John J Mahoney Realtor", # This is not a restaurant, but it's in the example HTML structure
            "Jimmy John's",
            "St John's Thrift Shop", # This is not a restaurant, but it's in the example HTML structure
            "Cathedral of St John", # This is not a restaurant, but it's in the example HTML structure
            "Papa Johns Pizza",
            "Long John Silver's"
        ]

        # Manually create mock result containers with their respective name elements
        mock_result_elements = []
        for name in expected_names:
            mock_name_element = create_mock_element('div', text=name, class_name='qBF1Pd fontHeadlineSmall')
            mock_container = create_mock_element('div', role='article')
            mock_container.find_element.return_value = mock_name_element
            mock_result_elements.append(mock_container)

        mock_driver.find_elements.return_value = mock_result_elements

        query = "restaurants in test city"
        result = search_restaurants(query)

        mock_initialize_browser.assert_called_once()
        mock_perform_gmaps_search.assert_called_once_with(mock_driver, query)
        mock_close_browser.assert_called_once_with(mock_driver)

        # We assert that the extracted names match our expected list
        self.assertEqual(result, expected_names)

    @patch('googlemapstew_plugin.browser_control.initialize_browser')
    @patch('googlemapstew_plugin.browser_control.close_browser')
    @patch('googlemapstew_plugin.browser_control.perform_gmaps_search')
    def test_search_restaurants_no_results(self, mock_initialize_browser, mock_close_browser, mock_perform_gmaps_search):
        mock_driver = MagicMock()
        mock_initialize_browser.return_value = mock_driver
        mock_perform_gmaps_search.return_value = True # Search itself is successful

        # No result containers found
        mock_driver.find_elements.return_value = [] 

        query = "nonexistent place"
        result = search_restaurants(query)

        mock_initialize_browser.assert_called_once()
        mock_perform_gmaps_search.assert_called_once_with(mock_driver, query)
        mock_close_browser.assert_called_once_with(mock_driver)
        self.assertEqual(result, [])

    @patch('googlemapstew_plugin.browser_control.initialize_browser')
    @patch('googlemapstew_plugin.browser_control.close_browser')
    @patch('googlemapstew_plugin.browser_control.perform_gmaps_search')
    def test_search_restaurants_search_failure(self, mock_initialize_browser, mock_close_browser, mock_perform_gmaps_search):
        mock_driver = MagicMock()
        mock_initialize_browser.return_value = mock_driver
        mock_perform_gmaps_search.return_value = False # Search failed

        query = "failing query"
        result = search_restaurants(query)

        mock_initialize_browser.assert_called_once()
        mock_perform_gmaps_search.assert_called_once_with(mock_driver, query)
        mock_close_browser.assert_called_once_with(mock_driver)
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
