"""Tests for the Google Maps scraper."""

from bs4 import BeautifulSoup

from googlemapstew import GoogleMapsScraper

# Sample HTML from Wendy's Google Maps page
SAMPLE_HTML = """
<div class="bJzME tTVLSc">
    <div class="m6QErb WNBkOb XiKgde " aria-label="Wendy's">
        <div class="tAiQdd">
            <div class="lMbq3e">
                <div>
                    <h1 class="DUwDvf lfPIob"><span class="a5H0ec"></span>Wendy's</h1>
                </div>
                <div class="LBgpqf">
                    <div class="skqShb">
                        <div class="fontBodyMedium dmRWX">
                            <div class="F7nice">
                                <span><span aria-hidden="true">3.9</span></span>
                                <span><span role="img" aria-label="1,107 reviews">(1,107)</span></span>
                            </div>
                            <span><span class="mgr77e"><span><span role="img" aria-label="Cheap$">$</span></span></span></span>
                        </div>
                        <div class="fontBodyMedium">
                            <button class="DkEaL">Fast food restaurant</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <button class="CsEnBe" data-item-id="address">
            <div class="Io6YTe">3801 Blake Rd SW, Albuquerque, NM 87121</div>
        </button>
        <button class="CsEnBe" data-item-id="phone:tel:+15058732233">
            <div class="Io6YTe">(505) 873-2233</div>
        </button>
        <button class="CsEnBe" data-item-id="oh">
            <div class="Io6YTe"><span style="color: rgba(25,134,57,1.00);">Open</span> · Closes 1 AM</div>
        </button>
        <a class="CsEnBe" data-item-id="authority" href="https://locations.wendys.com/united-states/nm/albuquerque/3801-blake-road-sw">
            <div class="Io6YTe">locations.wendys.com</div>
        </a>
        <button class="XJ8h0e waIsr">
            <div class="PYvSYb">Fast-food burger chain serving sides such as chili & baked potatoes.</div>
        </button>
    </div>
</div>
"""


def test_scraper_initialization():
    """Test that the scraper can be initialized."""
    scraper = GoogleMapsScraper()
    assert scraper is not None
    assert scraper.BASE_URL == "https://www.google.com/maps"


def test_parse_html():
    """Test parsing of HTML content."""
    scraper = GoogleMapsScraper()
    result = scraper.parse_html(SAMPLE_HTML)

    assert result is not None
    assert result["name"] == "Wendy's"
    assert result["rating"] == 3.9
    assert result["review_count"] == 1107
    assert result["price_level"] == "$"
    assert result["category"] == "Fast food restaurant"
    assert result["address"] == "3801 Blake Rd SW, Albuquerque, NM 87121"
    assert result["phone"] == "(505) 873-2233"
    assert result["website"] == "https://locations.wendys.com/united-states/nm/albuquerque/3801-blake-road-sw"
    assert result["description"] == "Fast-food burger chain serving sides such as chili & baked potatoes."


def test_extract_name():
    """Test name extraction."""
    scraper = GoogleMapsScraper()
    soup = BeautifulSoup(SAMPLE_HTML, "html.parser")
    name = scraper._extract_name(soup)
    assert name == "Wendy's"


def test_extract_rating():
    """Test rating extraction."""
    scraper = GoogleMapsScraper()
    soup = BeautifulSoup(SAMPLE_HTML, "html.parser")
    rating = scraper._extract_rating(soup)
    assert rating == 3.9


def test_extract_review_count():
    """Test review count extraction."""
    scraper = GoogleMapsScraper()
    soup = BeautifulSoup(SAMPLE_HTML, "html.parser")
    count = scraper._extract_review_count(soup)
    assert count == 1107


def test_extract_price_level():
    """Test price level extraction."""
    scraper = GoogleMapsScraper()
    soup = BeautifulSoup(SAMPLE_HTML, "html.parser")
    price = scraper._extract_price_level(soup)
    assert price == "$"


def test_extract_address():
    """Test address extraction."""
    scraper = GoogleMapsScraper()
    soup = BeautifulSoup(SAMPLE_HTML, "html.parser")
    address = scraper._extract_address(soup)
    assert address == "3801 Blake Rd SW, Albuquerque, NM 87121"


def test_extract_phone():
    """Test phone extraction."""
    scraper = GoogleMapsScraper()
    soup = BeautifulSoup(SAMPLE_HTML, "html.parser")
    phone = scraper._extract_phone(soup)
    assert phone == "(505) 873-2233"


def test_extract_website():
    """Test website extraction."""
    scraper = GoogleMapsScraper()
    soup = BeautifulSoup(SAMPLE_HTML, "html.parser")
    website = scraper._extract_website(soup)
    assert "locations.wendys.com" in website


def test_extract_description():
    """Test description extraction."""
    scraper = GoogleMapsScraper()
    soup = BeautifulSoup(SAMPLE_HTML, "html.parser")
    desc = scraper._extract_description(soup)
    assert "Fast-food burger chain" in desc


def test_extract_category():
    """Test category extraction."""
    scraper = GoogleMapsScraper()
    soup = BeautifulSoup(SAMPLE_HTML, "html.parser")
    category = scraper._extract_category(soup)
    assert category == "Fast food restaurant"


def test_empty_html():
    """Test that empty HTML returns None values."""
    scraper = GoogleMapsScraper()
    result = scraper.parse_html("")
    assert result["name"] is None
    assert result["rating"] is None
    assert result["address"] is None