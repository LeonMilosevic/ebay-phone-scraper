# E-BAY PHONE SCRAPER

A package to help you scrape only sold, used and new phone's from ebay in Europe region 

### Introduction
Package will help you scrape phones based on model

### Technologies used
- Python
- UserAgent
- Beautiful Soup
- Psycopg2
- Heroku
- Pandas

### How to use it?

Install prerequisites:

- pip install fake-useragent,
- pip install beautifulsoup4,
- pip install psycopg2,

Import packages:

- from ebay import dbmanipulator
- from ebay import scraper

Connect to your heroku postgres database:

db_connection = dbmanipulator.connect_to_db(
    database=your_database, 
    user=your_user,
    password=your_password,
    port=your_port,
    host=your_host)

###### push dataframe to database

dbmanipulator.execute_values(db_connection, dataframe, table_name)

###### pass a db query and create a csv file
dbmanipulator.execute_query_expot_csv(db_connection, query)

##### Scrape ebay:

scraper.scrape_ebay_buynow('dress', 3000, 1)

##### expected results...