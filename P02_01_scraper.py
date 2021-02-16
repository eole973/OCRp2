import requests
from bs4 import BeautifulSoup
import os
import pandas as pd


def extract_data(book_ref):
    universal_product_code = book_ref.find_all('td')[0].text
    title = book_ref.find('h1').text
    price_including_tax = book_ref.find_all('td')[2].text.replace('Â', '')
    price_excluding_tax = book_ref.find_all('td')[3].text.replace('Â', '')
    number_available = book_ref.find_all('td')[5].text.replace('In stock (', '').replace(' available)', '')
    product_description = str(book_ref.find_all('p')[3].text)
    category = book_ref.find_all('a')[3].text
    reviews_rating = book_ref.find('p', class_='star-rating')['class'][1]
    image_url = book_ref.find_all('img')[0]['src'].replace('../../', 'http://books.toscrape.com/')
    data_row = {'product_page_url': product_page_url, 'universal_product_code': universal_product_code,
                'title': title, 'price_including_tax': price_including_tax,
                'price_excluding_tax': price_excluding_tax,
                'number_available': number_available, 'product_description': product_description,
                'category': category, 'reviews_rating': reviews_rating, 'image_url': image_url}
    return data_row


# create directory
try:
    os.mkdir('CSV')
except OSError:
    pass
data = []

for i in range(1, 51):
    url = "http://books.toscrape.com/catalogue/page-"+str(i)+".html"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # iterate in all book ref page
        for j in range(53, 93, 2):

            link = "http://books.toscrape.com/catalogue/" + soup.find_all('a')[j]['href']

            answer = requests.get(link)

            if answer.status_code == 200:
                soup_book = BeautifulSoup(answer.text, 'html.parser')
                # extract item requested
                product_page_url = link

                data.append(extract_data(soup_book))

# save item in csv file
df = pd.DataFrame(data, index=None,  columns=['product_page_url', 'universal_product_code',
                                              'title', 'price_including_tax',
                                              'price_excluding_tax', 'number_available',
                                              'product_description', 'category', 'reviews_rating',
                                              'image_url'])
df.to_csv('./CSV/extract_all.csv', encoding='utf-8', header=True, index=False)


def extract_data(book_ref):
    universal_product_code = book_ref.find_all('td')[0].text
    title = book_ref.find('h1').text
    price_including_tax = book_ref.find_all('td')[2].text.replace('Â', '')
    price_excluding_tax = book_ref.find_all('td')[3].text.replace('Â', '')
    number_available = book_ref.find_all('td')[5].text.replace('In stock (', '').replace(' available)', '')
    product_description = str(book_ref.find_all('p')[3].text)
    category = book_ref.find_all('a')[3].text
    reviews_rating = book_ref.find('p', class_='star-rating')['class'][1]
    image_url = book_ref.find_all('img')[0]['src'].replace('../../', 'http://books.toscrape.com/')
    data_row = {'product_page_url': product_page_url, 'universal_product_code': universal_product_code,
                'title': title, 'price_including_tax': price_including_tax,
                'price_excluding_tax': price_excluding_tax,
                'number_available': number_available, 'product_description': product_description,
                'category': category, 'reviews_rating': reviews_rating, 'image_url': image_url}
    return data_row
