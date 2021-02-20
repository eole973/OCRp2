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

url = "http://books.toscrape.com/"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    # iterate in all book ref page

    for j in range(3, 53):
        cat_link = "http://books.toscrape.com/" + soup.find_all('a')[j]['href']
        link = requests.get(cat_link)
        filename = soup.find_all('a')[j].text.strip()
        data = []

        if link.status_code == 200:
            soup_cat = BeautifulSoup(link.content, 'html.parser')

            for k in range(54, 94, 2):
                try:
                    book_link = soup_cat.find_all('a')[k]['href'].replace('../../../', 'http://books.toscrape.com/catalogue/')
                except(IndexError):
                    continue

                answer = requests.get(book_link)

                if answer.status_code == 200:
                    soup_book = BeautifulSoup(answer.content, 'html.parser')
                    # extract item requested
                    product_page_url = book_link
                    data.append(extract_data(soup_book))

            for l in range(2, 7):
                cat_page = cat_link.replace('index.html', 'page-' + str(l) + '.html')
                answer_cat = requests.get(cat_page)
                if answer_cat.status_code == 200:
                    soup_book_page = BeautifulSoup(answer_cat.content, 'html.parser')
                    for r in range(54, 94,2):
                        try:
                            book_cat_link = soup_cat.find_all('a')[r]['href'].replace('../../../', 'http://books.toscrape.com/catalogue/')
                        except(IndexError):
                            continue

                        answer_cat_book = requests.get(book_cat_link)
                        if answer_cat_book.status_code == 200:
                            soup_cat_book = BeautifulSoup(answer_cat_book.content, 'html.parser')
                            # extract item requested
                            product_page_url = book_cat_link
                            data.append(extract_data(soup_cat_book))
                else:
                    continue

            # save item in csv category file
        df = pd.DataFrame(data, index=None, columns=['product_page_url', 'universal_product_code',
                                                     'title', 'price_including_tax',
                                                     'price_excluding_tax', 'number_available',
                                                     'product_description', 'category',
                                                     'reviews_rating', 'image_url'])
        df.to_csv('./CSV/' + filename + '.csv', encoding='utf-8', index=False, header=True)
