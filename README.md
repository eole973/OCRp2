# OC Scraper
extract book item to: "books.toscrape.com

`P2_01_scraper.py` will extract book's data as in CSV file 
which be created in /CSV directory .

`P2_02_cat_scraper.py` will extract book's data by category and create CSV file for each in /CSV directory.

book data :
* product_page_url 
* universal_product_code (upc)
* title
* price_including_tax 
* price_excluding_tax
* number_available
* product_description
* category
* review_rating
* image_url

`P2_03_img_scarper.py` will extract all book cover and create an /image dir.

### installation
```
$ python -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

##### execute script 
```
$ python P2_0*.py 
```
##### quit
at the end ``` $ deactivate``` 
will exit virtual environment
