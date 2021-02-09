# E-BAY PHONE SCRAPER

A package to help you scrape only sold, used and new phone's from ebay in Europe region 

### Introduction
Package will help you scrape phones based on provided brand

### Technologies used
- Python
- UserAgent
- Beautiful Soup
- Requests
- Pandas
- Numpy

### How to use it?

Install prerequisites:

- pip install fake-useragent,
- pip install beautifulsoup4,
- pip install requests,
- pip install pandas

Import packages:

- from scraper import scraper

##### Brand id's required for ebay url:
- Apple: 319682,
- LG: 353985,
- Huawei: 349965,
- Samsung: 352130

##### Scrape ebay for phones:

scraper.scrape_phones('Apple', 5000, 319682)\
scraper.scrape_phones('Samsung', 5000, 352130)

##### Expected Results:

- brand_data.csv file with all scraped data in main directory 