from bs4 import BeautifulSoup
import requests
import numpy as np


# Get maximum page range
def get_max_pagination():
    url = "https://scrapethissite.com/pages/forms/"

    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    pagination = soup.find('ul', class_='pagination')

    li_pagination = pagination.find_all('li')

    pages = []

    for i in li_pagination:
        number = i.get_text()
        number = number.strip()
        try:
            # Checking if the result is a number
            float(number)
            pages.append(number)
        except ValueError:
            pass

    n_pages = np.array(pages, dtype=int)

    n_pages = np.max(n_pages)

    return n_pages


# Get column names for pandas
def get_columns_name():
    url = "https://scrapethissite.com/pages/forms/"

    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    t_headers = soup.find_all('th')

    result = []

    for i in t_headers:
        result.append(i.text.strip())

    return result
