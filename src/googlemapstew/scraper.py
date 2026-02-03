"""Google Maps scraper module."""

from bs4 import BeautifulSoup
from typing import Optional, Dict, Any
import re


class GoogleMapsScraper:
    """Basic scraper for extracting information from Google Maps."""

    BASE_URL = "https://www.google.com/maps"

    def __init__(self):
        """Initialize the scraper."""
        self._cached_html: Optional[str] = None

    def _extract_rating(self, soup: BeautifulSoup) -> Optional[float]:
        """Extract rating from the page."""
        # Try multiple selectors for rating
        selectors = [
            "span[aria-hidden]",
            ".F7nice span[aria-hidden]",
        ]
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(strip=True)
                # Try to extract float (rating format like "3.9")
                match = re.search(r"\d+\.\d+", text)
                if match:
                    return float(match.group())
        return None

    def _extract_review_count(self, soup: BeautifulSoup) -> Optional[int]:
        """Extract number of reviews from the page."""
        selectors = [
            "span[role='img'][aria-label*='review']",
            ".F7nice span[role='img']",
        ]
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(strip=True)
                # Extract number like "(1,107)"
                match = re.search(r"[\d,]+", text)
                if match:
                    return int(match.group().replace(",", ""))
        return None

    def _extract_price_level(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract price level from the page."""
        selectors = [
            "span[role='img'][aria-label*='$']",
            ".mgr77e span[role='img']",
        ]
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                label = element.get("aria-label", "")
                # Look for price level text like "Cheap$" or just "$$$"
                if "$" in label:
                    # Extract the dollar signs
                    dollars = "".join(c for c in label if c == "$")
                    if dollars:
                        return dollars
        return None

    def _extract_address(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract address from the page."""
        selectors = [
            "button[data-item-id='address'] .Io6YTe",
            ".Io6YTe.kR99db",
        ]
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(strip=True)
                if text and len(text) > 5:  # Basic validation
                    return text
        return None

    def _extract_phone(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract phone number from the page."""
        selectors = [
            "button[data-item-id^='phone'] .Io6YTe",
        ]
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(strip=True)
                # Validate phone format
                if re.search(r"[\d\-\(\)\s]{10,}", text):
                    return text
        return None

    def _extract_hours(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract hours information from the page."""
        selectors = [
            "button[data-item-id='oh'] .Io6YTe",
            ".Io6YTe",
        ]
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(strip=True)
                # Look for hours-related keywords
                if any(keyword in text.lower() for keyword in ["open", "close", "am", "pm", "hour"]):
                    return text
        return None

    def _extract_website(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract website from the page."""
        selectors = [
            "a[data-item-id='authority']",
            "a[data-item-id='menu']",
        ]
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                href = element.get("href", "")
                if href and href.startswith("http"):
                    return href
        return None

    def _extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract description/about text from the page."""
        selectors = [
            ".PYvSYb",
            "button[aria-label*='About'] .Io6YTe",
        ]
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(strip=True)
                if text and len(text) > 10:
                    return text
        return None

    def _extract_name(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract place name from the page."""
        selectors = [
            "h1.DUwDvf",
            "h1.lfPIob",
            "h1",
        ]
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(strip=True)
                if text:
                    return text
        return None

    def _extract_category(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract category/type from the page."""
        selectors = [
            "button[jsaction*='category']",
            ".DkEaL",
        ]
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(strip=True)
                if text and len(text) > 3:
                    return text
        return None

    def parse_html(self, html: str) -> Dict[str, Any]:
        """
        Parse Google Maps HTML content and extract place information.

        Args:
            html: Raw HTML content from Google Maps page

        Returns:
            dict: Extracted place information
        """
        soup = BeautifulSoup(html, "html.parser")

        return {
            "name": self._extract_name(soup),
            "rating": self._extract_rating(soup),
            "review_count": self._extract_review_count(soup),
            "price_level": self._extract_price_level(soup),
            "category": self._extract_category(soup),
            "address": self._extract_address(soup),
            "phone": self._extract_phone(soup),
            "hours": self._extract_hours(soup),
            "website": self._extract_website(soup),
            "description": self._extract_description(soup),
        }

    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """
        Parse Google Maps HTML from a file.

        Args:
            file_path: Path to HTML file

        Returns:
            dict: Extracted place information
        """
        with open(file_path, "r", encoding="utf-8") as f:
            html = f.read()
        return self.parse_html(html)