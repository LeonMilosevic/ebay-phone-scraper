# E-BAY PHONE SCRAPER

A package to help you scrape only sold, used and new phone's from ebay in Europe region 

### Introduction
Package will help you scrape phones based on provided brand

### How to use it?

1. Install the scraper

```python
pip install git+https://github.com/LeonMilosevic/ebay-phone-scraper
```

2. Install prerequisites from requirements.txt

3. Import class:
```python
from scraper.scraper import Scraper
```
4. Scrape ebay for phones:

```python
scraper = Scraper('Apple', 5000, 'new')
scraper.scrape_phones()
```
##### Expected Results:

- brand_condition_data.csv file with all scraped data in main directory 
