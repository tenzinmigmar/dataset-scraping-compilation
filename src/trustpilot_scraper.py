import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import time
import csv

class UnsuccessfulRequestError(Exception):
    """
    Raises if the request code != 200
    """
    pass

class TooManyPagesRequestedError(Exception):
    """
    Raises if more than 50 pages are requested
    """

class TrustPilotScraper:
    __BASE_URL = "https://ca.trustpilot.com/review/"

    def __init__(self, review_site, page_number):
        self.__review_site = review_site
        if page_number <= 20:
            self.page_number = page_number
        else:
            raise TooManyPagesRequestedError("The maximum pages you can request is 50!")
        self.data = {"Review Titles": [], "Review Dates": [], "Reviews": [], "Star Ratings": []}
        self.results = self.get_results()

    def get_page(self, current_page):
        r = requests.get(TrustPilotScraper.__BASE_URL + self.__review_site + current_page)
        if r.status_code != 200:
            raise UnsuccessfulRequestError(f"A {r.status_code} was issued.")
        self.__soup = BeautifulSoup(r.content, "html.parser")

        self.data["Review Titles"].extend([review_title.get_text() for review_title
        in self.__soup.find_all(attrs={"name": "review-title"})])
        self.data["Review Dates"].extend([review_date.get_text() for review_date in self.__soup.find_all("time")])
        for i, review_date in enumerate(self.data["Review Dates"]):
            value = int(re.search(r'\d', review_date).group(0))
            if "hours" in review_date:
                new_date = datetime.now() - timedelta(hours=value)
                self.data["Review Dates"][i] = new_date.strftime("%B %d, %Y")
            elif "days" in review_date:
                new_date = datetime.now() - timedelta(hours=24*value)
                self.data["Review Dates"][i] = new_date.strftime("%B %d, %Y")

        self.data["Reviews"].extend([review.get_text() for review in self.__soup.find_all("p",
        attrs={"data-service-review-text-typography": "true"})])
        self.data["Star Ratings"].extend([int(re.search(r'\d', star_rating.get('alt')).group(0))
        for star_rating in self.__soup.find_all('img', alt=re.compile('Rated'))])

    def get_results(self):
        for i in range(self.page_number):
            if i == 0:
                self.get_page("")
            else:
                self.get_page(f"?page={i}")
            time.sleep(10)

    @property
    def total_reviews(self):
        return len(self.data["Reviews"])

    @property
    def avg_rating(self):
        avg_rating = 0
        for rating in self.data["Star Ratings"]:
            avg_rating += int(re.search(r'\d', rating).group(0))
        avg_rating /= len(self.data["Star Ratings"])
        return avg_rating

    def write_to_csv(self, file_name):
        keys = sorted(self.data.keys())
        with open(f"{file_name}.csv", "w") as f:
            w = csv.w(f, delimiter=",")
            w.writerow(keys)
            w.writerows(zip(*[self.data[key] for key in keys]))