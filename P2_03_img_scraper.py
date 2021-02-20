import requests  # to get image from the web
import shutil  # to save it locally
from bs4 import BeautifulSoup
import os

# create directory
try:
    os.mkdir('image')
except OSError:
    pass

# iterate in all page
for i in range(1, 51):
    url = "http://books.toscrape.com/catalogue/page-" + str(i) + ".html"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for j in range(53, 93, 2):
            link = "http://books.toscrape.com/catalogue/" + soup.find_all('a')[j]['href']

            answer = requests.get(link)

            if answer.status_code == 200:
                soup_book = BeautifulSoup(answer.text, 'html.parser')
                image_url = 'http://books.toscrape.com/' + soup_book.find_all('img')[0]['src']
                filename = soup_book.find('h1').text.replace('/', ' ')

                # Open the url image, set stream to True, this will return the stream content.

                r = requests.get(image_url, stream=True)

                # Check if the image was retrieved successfully

                if r.status_code == 200:
                    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                    r.raw.decode_content = True
                    # Open a local file with wb permission.
                    with open('./image/' + filename, 'wb') as f:
                        shutil.copyfileobj(r.raw, f)
