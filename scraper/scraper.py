from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import pandas as pd
import numpy as np

def check_brandId(brand: str) -> int:
    brandId: int
    if brand == "Apple":
        brandId = 319682
    elif brand == "LG":
        brandId = 353985
    elif brand == "Huawei":
        brandId = 349965
    elif brand == "Samsung":
        brandId = 352130
    else:
        raise ValueError("Function only supports Apple, LG, Huawei or Samsung brand")

    return brandId

def calculate_number_of_pages(number_of_items: int) -> int:
    return int(round(number_of_items / 48)) 
   

def get_phones_url(number_of_pages: int, brand: str, brandId: int, user_agent: UserAgent) -> list:
    urls = []
    
    for page_number in range(number_of_pages):
        url = f"https://www.ebay.com/b/{brand}-Cell-Phones-Smartphones/9355/bn_{brandId}?LH_ItemCondition=1000|3000&LH_PrefLoc=5&LH_Sold=1&rt=nc&_pgn={page_number}"
        page = requests.get(url, headers={"User-Agent": user_agent.google})
        soup = BeautifulSoup(page.content, "html.parser")

        urls.extend([links.get('href', np.nan) for links in soup.find_all('a', class_="s-item__link")])

    return urls

def scrape_phones(brand: str, number_of_items: int) -> pd.DataFrame:
    brandId = check_brandId(brand)
    number_of_pages = calculate_number_of_pages(number_of_items)
    user_agent = UserAgent()

    phone_model, phone_ram, phone_storage, phone_processor, phone_camera, phone_price = ([] for i in range(6))
    
    single_phone_urls = get_phones_url(number_of_pages, brand, brandId, user_agent)

    for single_phone_url in single_phone_urls:
        url = single_phone_url
        page = requests.get(url, headers={"User-Agent": user_agent.google})
        soup = BeautifulSoup(page.content, "html.parser")

        temp_price = np.nan
        temp_model = np.nan
        temp_ram = np.nan
        temp_storage = np.nan
        temp_processor = np.nan
        temp_camera = np.nan

        if soup.find(class_="display-price"):
            temp_price = souop.find(class_="display-price").get_text()
        
        for item in soup.find_all('div', class_='s-name'):

            if item.get_text() == "Model":
                temp_model = item.next_sibling.get_text()

            if item.get_text() == "RAM":
                print(item.next_sibling.get_text())

            if item.get_text() == "Storage Capacity":
                print(item.next_sibling.get_text())

            if item.get_text() == "Processor":
                print(item.next_sibling.get_text())

            if item.get_text() == "Camera Resolution":
                print(item.next_sibling.get_text())
        
        phone_price.append(temp_price)
        phone_model.append(temp_model)
        phone_ram.append(temp_ram)
        phone_storage.append(temp_storage)
        phone_processor.append(temp_processor)
        phone_camera.append(temp_camera)

scrape_phones("Apple", 48)