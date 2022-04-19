import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

base_url = "https://www.goodreads.com"
url = "https://www.goodreads.com/shelf/show/"
genres = ['nonfiction', 'fiction', 'fantasy', 'sciencefiction', 'classics', 'philosophy', 'science', 'poetry']

def get_book_links(genre):
    page = requests.get(url + genre)
    soup = BeautifulSoup(page.content, 'html.parser')
    divs = soup.find_all("div", {"class": "elementList"})
    links = [re.findall("(?<=href=\").*.*(?=\" title)", string) for string in [str(div.find('a')) for div in divs]]
    flatten = [item for sublist in links for item in sublist]
    links_of_books = []
    for i in range(len(flatten)):
        links_of_books.append(base_url + flatten[i])
    return links_of_books

def get_avg_rating(soup):
    try:
        rating_value = soup.find('span', {'itemprop': 'ratingValue'}).text.strip()
        return rating_value
    except:
        KeyError("Tag not found")


def get_author(soup):
    try:
        author_name = soup.find('span', {"itemprop": "name"}).text.strip()
        return author_name
    except:
        KeyError("Tag not found")

def get_title(soup):
    try:
        title = soup.find('h1', {'itemprop': "name"}).text.strip()
        return title
    except:
        KeyError("Tag not found")


def get_description(soup):
    try:
        description_text = list(soup.find("div", {"id": "description", "class": "readable stacked"}))[3].text.strip()
        return description_text
    except:
        KeyError("Tag not found")

def get_number_of_pages(soup):
    try:
        num_of_pages = soup.find("span", {"itemprop": "numberOfPages"}).text.strip()
        return num_of_pages
    except:
        KeyError("Tag not found")

def main(genre):
    titles = []
    authors = []
    descriptions = []
    avg_rating = []
    number_of_pages = []

    for item in get_book_links(genre):
        page = requests.get(item)
        soup = BeautifulSoup(page.content, 'html.parser')
        titles.append(get_title(soup))
        authors.append(get_author(soup))
        descriptions.append(get_description(soup))
        avg_rating.append(get_avg_rating(soup))
        number_of_pages.append(get_number_of_pages(soup))

    df = pd.DataFrame(list(zip(titles, authors, descriptions, avg_rating, number_of_pages)),columns=['Titles', 'Authors', 'Descriptions', 'Avg Rating', 'Number of Pages'])

    return df

for genre in genres:
    main(genre).to_csv('{}_books.csv'.format(genre), index=False, sep=',')