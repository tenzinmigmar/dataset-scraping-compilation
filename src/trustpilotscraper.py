import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import csv

class FileTypeNotSupportedError(ValueError):
    """
    Raises if the passed file type is not .json or .csv
    """
    pass

class UnsuccessfulRequestError(Exception):
    """
    Raises if the request code != 200
    """

class TrustPilotScraper:
    __BASE_URL = "https://ca.trustpilot.com/review/"

    def __init__(self, review_site, page_number):
        self.review_site = review_site
        self.page_number = page_number
        self.data = {"Review Titles": [], "Review Dates": [], "Reviews": [], "Star Ratings": []}
        self.results = self.get_results()

    def get_page(self, current_page):
        self.__page = requests.get(TrustPilotScraper.__BASE_URL + self.review_site + current_page)
        self.__soup = BeautifulSoup(self.__page.content, "html.parser")
        self.data["Review Titles"].extend([review_title.get_text() for review_title in self.__soup.find_all(attrs={"name": "review-title"})])
        self.data["Review Dates"].extend([review_date.get_text() for review_date in self.__soup.find_all("time")])
        self.data["Reviews"].extend([review.get_text() for review in self.__soup.find_all("p", attrs={"data-service-review-text-typography": "true"})])
        self.data["Star Ratings"].extend([star_rating.get('alt') for star_rating in self.__soup.find_all('img', alt=re.compile('Rated'))])

    def get_results(self):
        for i in range(self.page_number):
            if i == 0:
                self.get_page("")
            else:
                self.get_page(f"?page={i}")

    def total_reviews(self):
        return len(self.data["Reviews"])
