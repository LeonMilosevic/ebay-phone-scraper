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

Install prerequisite from requirements.txt

Import class:

- from scraper.scraper import Scraper

##### Scrape ebay for phones:

scraper = Scraper('Apple', 5000, 'new')\
scraper.scrape_phones()

##### Expected Results:

- brand_condition_data.csv file with all scraped data in main directory 