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

##### Scrape ebay for phones:

scraper.scrape_phones('Apple', 5000)
scraper.scrape_phones('Samsung', 5000)

##### Expected Results:

- brand_data.csv file with all scraped data in main directory 