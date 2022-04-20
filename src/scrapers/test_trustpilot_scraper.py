import pytest
from trustpilot_scraper import TrustPilotScraper

def test_review_titles():
    url_test_1 = "instacart.com"
    scraper = TrustPilotScraper(url_test_1, 5)
    assert len(scraper.data["Review Titles"]) != 0
    url_test_2 = "www.airbnb.com"
    scraper2 = TrustPilotScraper(url_test_2, 7)
    assert len(scraper2.data["Review Titles"]) != 0
    url_test_3 = "www.hellofresh.ca"
    scraper3 = TrustPilotScraper(url_test_3, 7)
    assert len(scraper3.data["Review Titles"]) != 0

def test_review_dates():
    url_test = "instacart.com"
    scraper = TrustPilotScraper(url_test, 2)
    assert len(scraper.data["Review Dates"]) != 0
    assert "hours" not in scraper.data["Review Dates"]
    assert "days" not in scraper.data["Review Dates"]
    assert "day" not in scraper.data["Review Dates"]

def test_reviews():
    url_test = "instacart.com"
    scraper = TrustPilotScraper(url_test, 2)
    assert len(scraper.data["Reviews"]) != 0

def test_star_ratings():
    url_test = "instacart.com"
    scraper = TrustPilotScraper(url_test, 2)
    assert len(scraper.data["Star Ratings"]) != 0
    assert all(isinstance(x, int) for x in scraper.data["Star Ratings"])

