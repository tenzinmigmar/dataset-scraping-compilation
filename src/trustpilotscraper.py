import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

class FileTypeNotSupportedError(ValueError):
    """
    Raises an exception if the passed file type is not .json or .csv
    """
    pass

class TrustPilotScraper:
    __BASE_URL = "https://ca.trustpilot.com/review/"

    def __init__(self, review_site, page_number=""):
        self.__page = requests.get(TrustPilotScraper.__BASE_URL + review_site + page_number)
        self.__soup = BeautifulSoup(self.__page.content, "html.parser")
        self.review_titles = self.get_review_titles()
        self.review_dates = self.get_review_dates()
        self.reviews = self.get_reviews()
        self.star_ratings = self.get_star_ratings()

    def get_review_titles(self):
        return [review_title.get_text() for review_title in self.__soup.find_all(attrs={"name": "review-title"})]

    def get_review_dates(self):
        return [review_date.get_text() for review_date in self.__soup.find_all("time")]

    def get_reviews(self):
        return [review.get_text() for review in self.__soup.find_all("p", attrs={"data-service-review-text-typography": "true"})]

    def get_star_ratings(self):
        return [star_rating.get('alt') for star_rating in self.__soup.find_all('img', alt=re.compile('Rated'))]

    def write_to_file(self, file_type, file_name):
        df = pd.DataFrame(list(zip(self.review_titles, self.review_dates, self.reviews, self.star_ratings)), columns=['Review Titles', 'Review Dates', 'Reviews', 'Rating (Out of 5 Stars)'])
        if file_type.casefold() == "csv":
            df.to_csv(file_name + ".csv", index=False, sep=',')
        elif file_type.casefold() == "json":
            df.to_json(f'{file_name}.json', orient='records', lines=True)
        elif file_type.casefold() == "txt":
            with open(f'{file_name}.txt', 'w') as f:
                f.write(df)
        else:
            raise FileTypeNotSupportedError(f"{file_type} is not supported! Use .json or .csv file types!")

